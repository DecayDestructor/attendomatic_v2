from ..repositories.logs_repository import LogsRepository
from ..repositories.subject_repository import SubjectRepository
from ..repositories.slots_repository import SlotRepository
from ..repositories.timetable_repository import TimeTableRepository
from ..models.models import Status, Type, DayOfWeek, Logs
from datetime import time, date


# This service is responsible for handling attendance-related operations and business logic.
class AttendanceService:
    def __init__(
        self,
        logs_repository: LogsRepository,
        subject_repository: SubjectRepository,
        slots_repository: SlotRepository,
        timetable_repository: TimeTableRepository,
    ):
        self.logs_repository = logs_repository
        self.subject_repository = subject_repository
        self.slots_repository = slots_repository
        self.timetable_repository = timetable_repository

    def mark_attendance(
        self,
        user_id,
        subj: str,
        type: Type,
        status: Status,
        is_regular: bool,
        class_end_time: time,
        class_date: date,
    ):

        # Check if the subject exists
        subject = self.subject_repository.get_subject_by_code(subj)
        if not subject:
            raise ValueError("Subject not found")

        # Check if the user has a timetable entry for the subject but different status
        existing_log = self.logs_repository.get_logs(
            user_id=user_id,
            subject_id=subject.id,
            type=type,
            isRegular=is_regular,
            class_end_time=class_end_time,
            start_date=class_date,
            end_date=class_date,
        )
        if existing_log:
            for existing_log in existing_log:
                if existing_log.status != status:
                    # Update the status of the existing log
                    existing_log.status = status
                    self.logs_repository.update_log(existing_log)
                    return existing_log
                else:
                    raise ValueError("Attendance already marked with the same status")
        # Logic to mark attendance for a user at an event
        log = Logs(
            user_id=user_id,
            subject_id=subject.id,
            type=type,
            status=status,
            is_regular=is_regular,
            class_end_time=class_end_time,
            class_date=class_date,
        )
        try:
            self.logs_repository.create_log(log)
        except Exception as e:
            raise ValueError(f"Faced an error while marking attendance: {e}") from e

    def get_attendance(
        self,
        user_id,
        status: Status | None = None,
        type: Type | None = None,
        is_regular: bool | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        subject_id: int | None = None,
        top_n: int | None = None,
        newest_first: bool | None = True,
    ):
        # Logic to retrieve attendance records for a user
        return self.logs_repository.get_logs(
            user_id=user_id,
            status=status,
            type=type,
            start_date=start_date,
            end_date=end_date,
            isRegular=is_regular,
            subject_id=subject_id,
            top_n=top_n,
            newest_first=newest_first,
        )
