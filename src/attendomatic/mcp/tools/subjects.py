from ..dependencies import get_subject_service, get_user_service
from fastmcp.dependencies import CurrentRequest
from starlette.requests import Request
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def _serialize_subject(subject):
    """Convert a Subject model instance into a serializable dictionary."""
    return {
        "id": subject.id,
        "name": subject.name,
        "code": subject.code,
    }


def _validate_id(value: int, field_name: str):
    """Validate that a value is a positive integer."""
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")


def _validate_text(value: str, field_name: str):
    """Validate that a text value is a non-empty string."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be blank")

    return value.strip()


def _get_current_user(request: Request):
    """Extract the authenticated user from request.state."""
    user = getattr(request.state, "user", None)
    if not user:
        raise Exception("Unauthorized: Authentication required")
    return user


def _require_admin(request: Request):
    """Ensure that the authenticated user has administrator privileges."""
    user = _get_current_user(request)
    if not user.is_admin:
        raise Exception("Unauthorized: Admin access required")
    return user


def _get_subject_or_raise(subject_service, subject_id: int):
    """Retrieve a subject by ID or raise an exception if it does not exist."""
    _validate_id(subject_id, "subject_id")
    subject = subject_service.get_subject_by_id(subject_id)

    if not subject:
        raise Exception("Subject not found")

    return subject


def create_subject(
    name: str,
    code: str,
    request: Request = CurrentRequest(),
):
    """
    Create a new subject.

    Use this tool when the user wants to add a new subject to the system.

    Args:
        name: The name of the subject.
        code: The subject code.

    Returns:
        The newly created subject with its ID, name, and code.
    """
    _require_admin(request)

    name = _validate_text(name, "name")
    code = _validate_text(code, "code")

    with get_subject_service() as subject_service:
        subject = subject_service.create_subject(name, code)

    if not subject:
        raise Exception("Failed to create subject")

    return _serialize_subject(subject)


def get_subject_by_id(subject_id: int):
    """
    Get a subject using its unique ID.

    Use this tool when the subject ID is known and the user wants details
    about that specific subject.

    Args:
        subject_id: The ID of the subject.

    Returns:
        The subject with its ID, name, and code.
    """
    with get_subject_service() as subject_service:
        subject = _get_subject_or_raise(subject_service, subject_id)

    return _serialize_subject(subject)


def get_subject_by_code(code: str):
    """
    Get a subject using its subject code.

    Use this tool when the subject code is known and the user wants details
    about that specific subject.

    Args:
        code: The subject code.

    Returns:
        The subject with its ID, name, and code.
    """
    code = _validate_text(code, "code")

    with get_subject_service() as subject_service:
        subject = subject_service.get_subject_by_code(code)

    if not subject:
        raise Exception("Subject not found")

    return _serialize_subject(subject)


def get_my_subjects(request: Request = CurrentRequest()):
    """
    Get all subjects associated with the currently authenticated user.

    Use this tool when the user wants to view their own subjects or subjects
    associated with their account. The current user is determined automatically.

    Returns:
        A list of subjects associated with the current user.
    """
    user = _get_current_user(request)

    with get_subject_service() as subject_service:
        subjects = subject_service.get_subjects_by_user_id(user.id)

    return [_serialize_subject(subject) for subject in subjects]


async def get_all_subjects(request: Request = CurrentRequest()):
    """
    Get all subjects available in the system.

    Use this tool when the user wants to view or browse all available subjects.

    Returns:
        A list of all subjects with their ID, name, and code.
    """
    user = getattr(request.state, "user", None)

    logger.info(
        f"UserID: {user.id if user else 'None'}\n"
        f"UserEmail: {user.email if user else 'None'}\n"
        f"User Scalekit ID: {user.uid if user else 'None'}\n"
        f"Is Admin: {user.is_admin if user else 'None'}"
    )

    with get_subject_service() as subject_service:
        subjects = subject_service.get_all_subjects()

    return [_serialize_subject(subject) for subject in subjects]


def update_subject(
    subject_id: int,
    name: str | None = None,
    code: str | None = None,
    request: Request = CurrentRequest(),
):
    """
    Update an existing subject.

    Use this tool when the user wants to change the name, code, or both
    for an existing subject.

    Args:
        subject_id: The ID of the subject to update.
        name: The new subject name. Leave empty to keep the current name.
        code: The new subject code. Leave empty to keep the current code.

    Returns:
        The updated subject with its ID, name, and code.
    """
    _require_admin(request)

    _validate_id(subject_id, "subject_id")

    if name is None and code is None:
        raise ValueError("At least one of name or code must be provided")

    if name is not None:
        name = _validate_text(name, "name")

    if code is not None:
        code = _validate_text(code, "code")

    with get_subject_service() as subject_service:
        _get_subject_or_raise(subject_service, subject_id)
        subject = subject_service.update_subject(subject_id, name, code)

    if not subject:
        raise Exception("Failed to update subject")

    return _serialize_subject(subject)


def delete_subject(
    subject_id: int,
    request: Request = CurrentRequest(),
):
    """
    Delete an existing subject.

    Use this tool when the user explicitly wants to permanently remove
    a subject from the system.

    Args:
        subject_id: The ID of the subject to delete.

    Returns:
        A confirmation message after the subject is successfully deleted.
    """
    _require_admin(request)

    with get_subject_service() as subject_service:
        _get_subject_or_raise(subject_service, subject_id)

        if not subject_service.delete_subject(subject_id):
            raise Exception("Failed to delete subject")

    return {"message": "Subject deleted successfully"}
