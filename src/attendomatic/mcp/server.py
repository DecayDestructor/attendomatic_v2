import json
import os

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp import FastMCP
import uvicorn

from ..config import get_settings
from .auth import AuthMiddleware
from .tools.subjects import (
    create_subject,
    delete_subject,
    get_all_subjects,
    get_subject_by_code,
    get_subject_by_id,
    get_my_subjects,
    update_subject,
)
from .tools.slots import (
    get_single_slot,
    get_slots,
    create_slot,
    get_slot_by_id,
)

from .tools.timetable import (
    get_timetable,
    add_slot_to_timetable,
    get_timetable_by_id,
)
from .tools.attendance import mark_attendance, get_attendance

mcp = FastMCP("Attendomatic")

for tool in (
    create_subject,
    delete_subject,
    get_all_subjects,
    get_subject_by_code,
    get_subject_by_id,
    get_my_subjects,
    update_subject,
    get_single_slot,
    get_slots,
    create_slot,
    get_slot_by_id,
    get_timetable,
    add_slot_to_timetable,
    get_timetable_by_id,
    mark_attendance,
    get_attendance,
):
    mcp.tool(tool)


@mcp.custom_route(
    "/.well-known/oauth-protected-resource",
    methods=["GET"],
    include_in_schema=False,
)
async def protected_resource_metadata(request: Request):
    try:
        metadata = json.loads(get_settings().metadata_json_response)
    except (json.JSONDecodeError, TypeError):
        return JSONResponse(
            {"error": "METADATA_JSON_RESPONSE must contain valid JSON"},
            status_code=500,
        )

    if not isinstance(metadata, dict):
        return JSONResponse(
            {"error": "METADATA_JSON_RESPONSE must contain a JSON object"},
            status_code=500,
        )

    return JSONResponse(metadata)


from contextlib import asynccontextmanager

mcp_app = mcp.http_app(path="/mcp", transport="streamable-http")


@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    from ..models.main import create_db_and_tables

    create_db_and_tables()
    async with mcp_app.lifespan(app):
        yield


app = FastAPI(lifespan=combined_lifespan)
app.add_middleware(AuthMiddleware)
app.mount("/", mcp_app)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
    )
