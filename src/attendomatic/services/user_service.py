from ..repositories.logs_repository import LogsRepository
from ..repositories.subject_repository import SubjectRepository
from ..repositories.slots_repository import SlotRepository
from ..repositories.timetable_repository import TimeTableRepository
from ..models.models import Status, Type, DayOfWeek, Logs
from datetime import time, date


class UserService:
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

    def get_user_by_id(self, user_id: int):
        # Logic to retrieve a user by their ID
        return self.logs_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str):
        # Logic to retrieve a user by their email
        return self.logs_repository.get_user_by_email(email)
