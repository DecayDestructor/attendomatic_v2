# timetable_tools.py

from ..dependencies import get_timetable_service
from fastmcp.dependencies import CurrentRequest
from starlette.requests import Request


def _get_current_user(request: Request):
    """Extract the authenticated user from the request."""
    user = getattr(request.state, "user", None)

    if not user:
        raise Exception("Unauthorized: Authentication required")

    return user


def get_timetable(request: Request = CurrentRequest()):
    """
    Get the current user's complete timetable.

    Use this tool when the user wants to view their classes, schedule,
    or complete timetable.

    Returns:
        The timetable containing all slots assigned to the current user.
    """
    user = _get_current_user(request)

    with get_timetable_service() as timetable_service:
        return timetable_service.get_timetable(user_id=user.id)


def add_slot_to_timetable(
    slot_id: int,
    request: Request = CurrentRequest(),
):
    """
    Add an existing slot to the current user's timetable.

    Use this tool when the user wants to add a class or slot to their
    personal timetable. The slot must already exist.

    Args:
        slot_id: The ID of the slot to add to the timetable.

    Returns:
        The newly created timetable entry.
    """
    user = _get_current_user(request)

    with get_timetable_service() as timetable_service:
        return timetable_service.create_timetable(
            user_id=user.id,
            slot_id=slot_id,
        )


def get_timetable_by_id(timetable_id: int):
    """
    Get a specific timetable entry using its unique ID.

    Use this tool when the timetable entry ID is known and details about
    that specific entry are required.

    Args:
        timetable_id: The unique ID of the timetable entry.

    Returns:
        The timetable entry matching the provided ID.
    """
    with get_timetable_service() as timetable_service:
        return timetable_service.get_timetable_by_id(timetable_id=timetable_id)
