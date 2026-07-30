from ..repositories.logs_repository import LogsRepository
from ..repositories.subject_repository import SubjectRepository
from ..repositories.slots_repository import SlotRepository
from ..repositories.timetable_repository import TimeTableRepository
from ..models.models import Status, Type, DayOfWeek, Logs
from datetime import time, date


class TimeTableService:
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

    def get_timetable(
        self,
        user_id: int,
    ):
        # Logic to retrieve timetable for a user
        return self.timetable_repository.get_timetables_by_user_id(
            user_id=user_id,
        )

    def create_timetable(
        self,
        user_id: int,
        slot_id: int,
    ):
        # Logic to create a timetable entry for a user
        return self.timetable_repository.create_timetable(
            user_id=user_id,
            slot_id=slot_id,
        )

    def get_timetable_by_id(
        self,
        timetable_id: int,
    ):
        # Logic to retrieve a specific timetable entry by its ID
        return self.timetable_repository.get_timetable_by_id(
            timetable_id=timetable_id,
        )
