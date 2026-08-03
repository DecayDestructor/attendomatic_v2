from ..repositories.logs_repository import LogsRepository
from ..repositories.subject_repository import SubjectRepository
from ..repositories.slots_repository import SlotRepository
from ..repositories.timetable_repository import TimeTableRepository
from ..models.models import Status, Type, DayOfWeek, Logs
from datetime import time, date


class SlotService:
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

    def get_slots(
        self,
        subject_id: int | None = None,
        day_of_week: DayOfWeek | None = None,
        start_time: time | None = None,
        end_time: time | None = None,
        type: Type | None = None,
    ):
        # Logic to retrieve slots based on the provided filters
        return self.slots_repository.get_all_slots(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            type=type,
        )

    def get_single_slot(
        self,
        subject_id: int | None = None,
        day_of_week: DayOfWeek | None = None,
        start_time: time | None = None,
        end_time: time | None = None,
        type: Type | None = None,
    ):
        # Logic to retrieve a single slot based on the provided filters
        return self.slots_repository.get_slot(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            type=type,
        )

    def create_slot(
        self,
        subject_id: int,
        day_of_week: DayOfWeek,
        start_time: time,
        end_time: time,
        type: Type,
    ):
        # Logic to create a new slot
        return self.slots_repository.create_slot(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            type=type,
        )

    def get_slot_by_id(self, slot_id: int):
        # Logic to retrieve a slot by its ID
        return self.slots_repository.get_slot_by_id(slot_id)
