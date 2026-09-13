from ..dependencies import get_slot_service
from fastmcp.dependencies import CurrentRequest
from starlette.requests import Request
from ...models.models import DayOfWeek, Type
from datetime import time


def _get_current_user(request: Request):
    """Extract the authenticated user from the request."""
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


def get_slots(
    subject_id: int | None = None,
    day_of_week: DayOfWeek | None = None,
    start_time: time | None = None,
    end_time: time | None = None,
    type: Type | None = None,
):
    """
    Search for class slots matching the provided filters.

    Use this tool when class slot information needs to be found using
    details such as subject, day, start time, end time, or class type.
    Any combination of filters can be provided.

    Args:
        subject_id: Filter slots by subject ID.
        day_of_week: Filter slots by day of the week.
        start_time: Filter slots by start time.
        end_time: Filter slots by end time.
        type: Filter slots by class type.

    Returns:
        A list of matching class slots.
    """
    with get_slot_service() as slot_service:
        return slot_service.get_slots(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            type=type,
        )


def get_single_slot(
    subject_id: int | None = None,
    day_of_week: DayOfWeek | None = None,
    start_time: time | None = None,
    end_time: time | None = None,
    type: Type | None = None,
):
    """
    Find a single class slot matching the provided details.

    Use this tool when one specific class slot needs to be identified
    before performing another action, such as checking a timetable or
    recording attendance.

    Args:
        subject_id: The subject ID associated with the slot.
        day_of_week: The day of the week for the slot.
        start_time: The start time of the slot.
        end_time: The end time of the slot.
        type: The type of class.

    Returns:
        The matching class slot, if one is found.
    """
    with get_slot_service() as slot_service:
        return slot_service.get_single_slot(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            type=type,
        )


def create_slot(
    subject_id: int,
    day_of_week: DayOfWeek,
    start_time: time,
    end_time: time,
    type: Type,
    request: Request = CurrentRequest(),
):
    """
    Create a new class slot.

    Use this tool when a new class slot needs to be created with a subject,
    day, start time, end time, and class type.

    Args:
        subject_id: The ID of the subject for the slot.
        day_of_week: The day on which the class occurs.
        start_time: The time when the class starts.
        end_time: The time when the class ends.
        type: The type of class, such as Lecture, Lab, or Tutorial.

    Returns:
        The newly created class slot.
    """
    _require_admin(request)

    with get_slot_service() as slot_service:
        return slot_service.create_slot(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            type=type,
        )


def get_slot_by_id(slot_id: int):
    """
    Get detailed information about a class slot using its slot ID.

    Use this tool when a slot ID is available, for example from a timetable
    entry, and the slot's subject, day, time, or class type is needed for
    another operation such as checking a schedule or recording attendance.

    Args:
        slot_id: The unique ID of the class slot.

    Returns:
        The matching class slot.
    """
    with get_slot_service() as slot_service:
        return slot_service.get_slot_by_id(slot_id)
