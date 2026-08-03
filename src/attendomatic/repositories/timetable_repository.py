from sqlmodel import Session, select
from ..models.models import Slot, Subject, TimeTable


class TimeTableRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_timetable_by_id(self, timetable_id: int):
        return self.session.get(TimeTable, timetable_id)

    def get_timetables_by_user_id(self, user_id: int):
        # join with slots and subjects to get the complete timetable for the user
        statement = (
            select(TimeTable, Slot, Subject)
            .join(Slot, TimeTable.slot_id == Slot.id)
            .join(Subject, Slot.subject_id == Subject.id)
            .where(TimeTable.user_id == user_id)
        )
        return self.session.exec(statement).all()

    def create_timetable(self, user_id: int, slot_id: int):
        timetable = TimeTable(user_id=user_id, slot_id=slot_id)
        self.session.add(timetable)
        self.session.commit()
        self.session.refresh(timetable)
        return timetable
