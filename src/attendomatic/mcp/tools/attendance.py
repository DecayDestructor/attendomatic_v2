# attendance_tools.py

from ..dependencies import get_attendance_service, get_subject_service
from fastmcp.dependencies import CurrentRequest
from starlette.requests import Request
from ...models.models import Status, Type
from datetime import time, date


def _get_current_user(request: Request):
    """Extract the authenticated user from the request."""
    user = getattr(request.state, "user", None)

    if not user:
        raise Exception("Unauthorized: Authentication required")

    return user


def mark_attendance(
    subj: str,
    type: Type,
    status: Status,
    is_regular: bool,
    class_end_time: time,
    class_date: date,
    request: Request = CurrentRequest(),
):
    """
    Record attendance for a class.

    Use this tool when the user wants to mark themselves present, absent,
    or cancelled for a class. Before recording attendance for a regular
    scheduled class, use timetable and slot information when necessary to
    identify the correct subject, class type, end time, and date.

    Args:
        subj: The name or identifier of the subject.
        type: The class type, such as Lecture, Lab, or Tutorial.
        status: The attendance status, such as Present, Absent, or Cancelled.
        is_regular: Whether this is a regular timetable class or an extra class.
        class_end_time: The time when the class ends.
        class_date: The date on which the class takes place.

    Returns:
        The recorded attendance entry.
    """
    user = _get_current_user(request)

    with get_attendance_service() as attendance_service:
        return attendance_service.mark_attendance(
            user_id=user.id,
            subj=subj,
            type=type,
            status=status,
            is_regular=is_regular,
            class_end_time=class_end_time,
            class_date=class_date,
        )


def get_attendance(
    status: Status | None = None,
    type: Type | None = None,
    is_regular: bool | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    subject_id: int | None = None,
    request: Request = CurrentRequest(),
):
    """
    Get attendance records for the current user.

    Use this tool when the user wants to view, check, or analyze their
    attendance history. Results can be filtered by attendance status,
    class type, regular or extra classes, subject, or date range.

    Args:
        status: Filter by attendance status.
        type: Filter by class type.
        is_regular: Filter by regular or extra classes.
        start_date: Include attendance records from this date onwards.
        end_date: Include attendance records up to this date.
        subject_id: Filter attendance records by subject ID.

    Returns:
        A list of attendance records matching the provided filters.
    """
    user = _get_current_user(request)

    with get_subject_service() as subject_service:
        subjects = subject_service.get_all_subjects()
        if not subjects:
            raise ValueError("No subjects found")

    with get_attendance_service() as attendance_service:
        attendances = attendance_service.get_attendance(
            user_id=user.id,
            status=status,
            type=type,
            is_regular=is_regular,
            start_date=start_date,
            end_date=end_date,
            subject_id=subject_id,
        )

    # Map subject_id to subject name
    subject_map = {subject.id: subject.name for subject in subjects}
    for attendance in attendances:
        attendance.subject_name = subject_map.get(
            attendance.subject_id, "Unknown Subject"
        )

    return attendances
