import json
import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from scalekit import ScalekitClient
from starlette.middleware.base import BaseHTTPMiddleware

from .dependencies import get_user_service
from ..config import get_settings

settings = get_settings()


# -------------------------------------------------------------------
# Tool -> required OAuth scopes
# -------------------------------------------------------------------

TOOL_SCOPES: dict[str, list[str]] = {
    # Read-only operations — subjects
    "get_subject_by_id": ["all:read"],
    "get_subject_by_code": ["all:read"],
    "get_subjects_by_user_id": ["all:read"],
    "get_all_subjects": ["all:read"],
    # Write operations — subjects
    "create_subject": ["user:write"],
    "update_subject": ["user:write"],
    "delete_subject": ["user:write"],
    # Read-only operations — attendance
    "get_attendance": ["all:read"],
    # Write operations — attendance
    "mark_attendance": ["user:write"],
    # Read-only operations — slots
    "get_slots": ["all:read"],
    "get_single_slot": ["all:read"],
    "get_slot_by_id": ["all:read"],
    # Write operations — slots
    "create_slot": ["user:write"],
    # Read-only operations — timetable
    "get_timetable": ["all:read"],
    "get_timetable_by_id": ["all:read"],
    # Write operations — timetable
    "create_timetable": ["user:write"],
}

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Security
# -------------------------------------------------------------------

security = HTTPBearer()

scalekit_client = ScalekitClient(
    settings.scalekit_environment_url,
    settings.scalekit_client_id,
    settings.scalekit_client_secret,
)


# -------------------------------------------------------------------
# User registration / lookup
# -------------------------------------------------------------------


def get_or_register_user_by_scalekit_id(scalekit_uid: str):
    """
    Find the local user using the Scalekit `sub` (`uid`).

    If the user does not exist locally yet:
    1. Fetch the user from Scalekit.
    2. Extract their email/name.
    3. Create the local User.
    """

    with get_user_service() as user_service:

        # -----------------------------------------------------------
        # Existing local user
        # -----------------------------------------------------------

        user = user_service.get_user_by_uid(scalekit_uid)

        if user:
            logger.info(
                f"Existing local user found: " f"uid={scalekit_uid}, email={user.email}"
            )
            return user

        # -----------------------------------------------------------
        # First-time user -> fetch from Scalekit
        # -----------------------------------------------------------

        logger.info(
            f"User {scalekit_uid} not found locally. " "Registering user from Scalekit."
        )

        try:
            response = scalekit_client.users.get_user(user_id=scalekit_uid)

            if not response:
                raise Exception(f"Scalekit user not found: {scalekit_uid}")

            scalekit_user = response[0].user

        except Exception as e:
            logger.exception(f"Failed to fetch Scalekit user " f"{scalekit_uid}: {e}")
            raise Exception("Unable to retrieve user information from Scalekit")

        # -----------------------------------------------------------
        # Extract user information
        # -----------------------------------------------------------

        email = scalekit_user.email

        if not email:
            raise Exception(f"Scalekit user {scalekit_uid} has no email")

        name = getattr(scalekit_user, "name", None)

        if not name:
            name = email

        # -----------------------------------------------------------
        # Register locally
        # -----------------------------------------------------------

        user = user_service.create_user(
            name=name,
            email=email,
            uid=scalekit_uid,
        )

        if not user:
            raise Exception(
                f"Failed to create local user " f"for Scalekit user {scalekit_uid}"
            )

        logger.info(f"Registered new local user: " f"uid={scalekit_uid}, email={email}")

        return user


# -------------------------------------------------------------------
# Authentication middleware
# -------------------------------------------------------------------


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # -----------------------------------------------------------
        # OAuth metadata endpoints remain public
        # -----------------------------------------------------------

        if request.url.path.startswith("/.well-known/"):
            return await call_next(request)

        try:

            # -------------------------------------------------------
            # 1. Get Bearer token
            # -------------------------------------------------------

            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=401,
                    detail="Missing or invalid authorization header",
                )

            token = auth_header.split(" ", 1)[1].strip()

            if not token:
                raise HTTPException(
                    status_code=401,
                    detail="Missing bearer token",
                )

            # -------------------------------------------------------
            # 2. Parse MCP request body
            # -------------------------------------------------------

            request_body = await request.body()

            try:
                request_data = json.loads(request_body.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                request_data = {}

            # -------------------------------------------------------
            # 3. Validate access token
            # -------------------------------------------------------

            claims = scalekit_client.validate_access_token_and_get_claims(token=token)

            logger.info("Access token validated successfully")

            # -------------------------------------------------------
            # 4. Get Scalekit user ID (`sub`)
            # -------------------------------------------------------

            scalekit_uid = claims.get("sub")

            if not scalekit_uid:
                raise HTTPException(
                    status_code=401,
                    detail="Token does not contain a subject",
                )

            logger.info(f"Authenticated Scalekit user: " f"{scalekit_uid}")

            # Store token information
            request.state.scalekit_uid = scalekit_uid
            request.state.token_claims = claims

            # -------------------------------------------------------
            # 5. Check if MCP tool call
            # -------------------------------------------------------

            is_tool_call = request_data.get("method") == "tools/call"

            if is_tool_call:

                # ---------------------------------------------------
                # 6. Extract tool name
                # ---------------------------------------------------

                tool_name = request_data.get("params", {}).get("name")

                logger.info(f"Tool name: {tool_name}")

                if not tool_name:
                    raise HTTPException(
                        status_code=400,
                        detail="Missing MCP tool name",
                    )

                # ---------------------------------------------------
                # 7. Get required scopes
                # ---------------------------------------------------

                required_scopes = TOOL_SCOPES.get(tool_name)

                if required_scopes is None:
                    raise HTTPException(
                        status_code=403,
                        detail=(f"Tool '{tool_name}' " "is not authorized"),
                    )

                logger.info(
                    f"Required scopes for " f"'{tool_name}': " f"{required_scopes}"
                )

                # ---------------------------------------------------
                # 8. Get token scopes
                # ---------------------------------------------------

                token_scopes = set(claims.get("scopes", []))

                logger.info(f"Token scopes: " f"{sorted(token_scopes)}")

                # ---------------------------------------------------
                # 9. Verify scopes
                # ---------------------------------------------------

                missing_scopes = set(required_scopes) - token_scopes

                if missing_scopes:
                    raise HTTPException(
                        status_code=403,
                        detail=(
                            "Missing required scopes: " f"{sorted(missing_scopes)}"
                        ),
                    )

                logger.info(f"Scope check passed for " f"'{tool_name}'")

                request.state.tool_name = tool_name
                request.state.required_scopes = required_scopes

            # -------------------------------------------------------
            # 10. Get or register local user
            # -------------------------------------------------------

            user = get_or_register_user_by_scalekit_id(scalekit_uid)

            # Store local user for downstream handlers
            request.state.user = user
            request.state.user_id = user.id

            logger.info(
                f"Local user authenticated: "
                f"id={user.id}, "
                f"uid={user.uid}, "
                f"email={user.email}"
            )

        # -----------------------------------------------------------
        # Authentication / authorization errors
        # -----------------------------------------------------------

        except HTTPException as e:

            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": ("unauthorized" if e.status_code == 401 else "forbidden"),
                    "error_description": e.detail,
                },
                headers={
                    "WWW-Authenticate": (
                        f'Bearer realm="OAuth", '
                        f'resource_metadata="'
                        f'{settings.scalekit_resource_metadata_url}"'
                    )
                },
            )

        # -----------------------------------------------------------
        # Unexpected errors
        # -----------------------------------------------------------

        except Exception as e:

            logger.exception(f"Authentication failed: {e}")

            return JSONResponse(
                status_code=401,
                content={
                    "error": "unauthorized",
                    "error_description": ("Authentication failed"),
                },
            )

        return await call_next(request)
