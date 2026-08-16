from ..repositories.logs_repository import LogsRepository
from ..repositories.subject_repository import SubjectRepository
from ..repositories.slots_repository import SlotRepository
from ..repositories.timetable_repository import TimeTableRepository
from ..models.models import Status, Type, DayOfWeek, Logs
from datetime import time, date


class SubjectService:
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

    def get_subject_by_code(self, code: str):
        # Logic to retrieve a subject by its code
        return self.subject_repository.get_subject_by_code(code)

    def get_subject_by_id(self, subject_id: int):
        # Logic to retrieve a subject by its ID
        return self.subject_repository.get_subject_by_id(subject_id)

    def get_subjects_by_user_id(self, user_id: int):
        # Logic to retrieve subjects associated with a user
        return self.subject_repository.get_subjects_by_user_id(user_id)

    def create_subject(self, name: str, code: str):
        # Logic to create a new subject
        return self.subject_repository.create_subject(name, code)

    def get_all_subjects(self):
        # Logic to retrieve all subjects
        return self.subject_repository.get_all_subjects()

    def delete_subject(self, subject_id: int):
        # Logic to delete a subject by its ID
        return self.subject_repository.delete_subject(subject_id)

    def update_subject(
        self, subject_id: int, name: str | None = None, code: str | None = None
    ):
        # Logic to update a subject's details
        return self.subject_repository.update_subject(subject_id, name, code)
