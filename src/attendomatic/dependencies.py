from fastapi import Depends
from sqlmodel import Session


def get_session():
    from sqlmodel import Session
    from .models.main import get_engine

    engine = get_engine()
    with Session(engine) as session:
        yield session


def get_attendance_service(session: Session = Depends(get_session)):
    from .services.attendance_service import AttendanceService
    from .repositories.logs_repository import LogsRepository
    from .repositories.subject_repository import SubjectRepository
    from .repositories.slots_repository import SlotRepository
    from .repositories.timetable_repository import TimeTableRepository

    logs_repository = LogsRepository(session)
    subject_repository = SubjectRepository(session)
    slots_repository = SlotRepository(session)
    timetable_repository = TimeTableRepository(session)

    return AttendanceService(
        logs_repository=logs_repository,
        subject_repository=subject_repository,
        slots_repository=slots_repository,
        timetable_repository=timetable_repository,
    )


def get_slot_service(session: Session = Depends(get_session)):
    from .services.slots_service import SlotService
    from .repositories.logs_repository import LogsRepository
    from .repositories.subject_repository import SubjectRepository
    from .repositories.slots_repository import SlotRepository
    from .repositories.timetable_repository import TimeTableRepository

    logs_repository = LogsRepository(session)
    subject_repository = SubjectRepository(session)
    slots_repository = SlotRepository(session)
    timetable_repository = TimeTableRepository(session)

    return SlotService(
        logs_repository=logs_repository,
        subject_repository=subject_repository,
        slots_repository=slots_repository,
        timetable_repository=timetable_repository,
    )


def get_subject_service(session: Session = Depends(get_session)):
    from .services.subject_service import SubjectService
    from .repositories.logs_repository import LogsRepository
    from .repositories.subject_repository import SubjectRepository
    from .repositories.slots_repository import SlotRepository
    from .repositories.timetable_repository import TimeTableRepository

    logs_repository = LogsRepository(session)
    subject_repository = SubjectRepository(session)
    slots_repository = SlotRepository(session)
    timetable_repository = TimeTableRepository(session)

    return SubjectService(
        logs_repository=logs_repository,
        subject_repository=subject_repository,
        slots_repository=slots_repository,
        timetable_repository=timetable_repository,
    )


def get_user_service(session: Session = Depends(get_session)):
    from .services.user_service import UserService
    from .repositories.logs_repository import LogsRepository
    from .repositories.subject_repository import SubjectRepository
    from .repositories.slots_repository import SlotRepository
    from .repositories.timetable_repository import TimeTableRepository

    logs_repository = LogsRepository(session)
    subject_repository = SubjectRepository(session)
    slots_repository = SlotRepository(session)
    timetable_repository = TimeTableRepository(session)

    return UserService(
        logs_repository=logs_repository,
        subject_repository=subject_repository,
        slots_repository=slots_repository,
        timetable_repository=timetable_repository,
    )
