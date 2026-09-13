from contextlib import contextmanager

from sqlmodel import Session

from attendomatic.services.attendance_service import AttendanceService
from attendomatic.services.slots_service import SlotService
from attendomatic.services.timetable_service import TimeTableService

from ..repositories.logs_repository import LogsRepository
from ..repositories.slots_repository import SlotRepository
from ..repositories.subject_repository import SubjectRepository
from ..repositories.timetable_repository import TimeTableRepository
from ..repositories.user_repository import UserRepository
from ..services.subject_service import SubjectService
from ..services.user_service import UserService


@contextmanager
def get_subject_service():
    from ..models.main import get_engine

    with Session(get_engine()) as session:
        yield SubjectService(
            logs_repository=LogsRepository(session),
            subject_repository=SubjectRepository(session),
            slots_repository=SlotRepository(session),
            timetable_repository=TimeTableRepository(session),
        )


@contextmanager
def get_user_service():
    from ..models.main import get_engine

    with Session(get_engine()) as session:
        yield UserService(
            logs_repository=LogsRepository(session),
            subject_repository=SubjectRepository(session),
            slots_repository=SlotRepository(session),
            timetable_repository=TimeTableRepository(session),
            user_repository=UserRepository(session),
        )


@contextmanager
def get_slot_service():
    from ..models.main import get_engine

    with Session(get_engine()) as session:
        yield SlotService(
            logs_repository=LogsRepository(session),
            subject_repository=SubjectRepository(session),
            slots_repository=SlotRepository(session),
            timetable_repository=TimeTableRepository(session),
        )


@contextmanager
def get_attendance_service():
    from ..models.main import get_engine

    with Session(get_engine()) as session:
        yield AttendanceService(
            logs_repository=LogsRepository(session),
            subject_repository=SubjectRepository(session),
            slots_repository=SlotRepository(session),
            timetable_repository=TimeTableRepository(session),
        )


@contextmanager
def get_timetable_service():
    from ..models.main import get_engine

    with Session(get_engine()) as session:
        yield TimeTableService(
            logs_repository=LogsRepository(session),
            subject_repository=SubjectRepository(session),
            slots_repository=SlotRepository(session),
            timetable_repository=TimeTableRepository(session),
        )
