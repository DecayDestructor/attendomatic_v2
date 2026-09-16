from sqlmodel import Session, select
from ..models.models import Slot, DayOfWeek, Type
from datetime import time


class SlotRepository:
    def __init__(self, session: Session):
        self.session = session

    def _build_query(
        self,
        subject_id: int | None = None,
        day_of_week: DayOfWeek | None = None,
        start_time: time | None = None,
        end_time: time | None = None,
        type: Type | None = None,
    ):
        statement = select(Slot)

        if subject_id is not None:
            statement = statement.where(Slot.subject_id == subject_id)

        if day_of_week is not None:
            statement = statement.where(Slot.day == day_of_week)

        if start_time is not None:
            statement = statement.where(Slot.start_time >= start_time)

        if end_time is not None:
            statement = statement.where(Slot.end_time <= end_time)

        if type is not None:
            statement = statement.where(Slot.type == type)

        return statement

    def get_slot_by_id(self, slot_id: int):
        return self.session.get(Slot, slot_id)

    def get_slot(
        self,
        subject_id: int | None = None,
        day_of_week: DayOfWeek | None = None,
        start_time: time | None = None,
        end_time: time | None = None,
        type: Type | None = None,
    ):
        statement = self._build_query(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            type=type,
        )
        return self.session.exec(statement).first()

    def get_all_slots(
        self,
        subject_id: int | None = None,
        day_of_week: DayOfWeek | None = None,
        start_time: time | None = None,
        end_time: time | None = None,
        type: Type | None = None,
    ):
        statement = self._build_query(
            subject_id=subject_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            type=type,
        )
        return self.session.exec(statement).all()

    def create_slot(self, slot: Slot):
        self.session.add(slot)
        self.session.commit()
        self.session.refresh(slot)
        return slot

    def get_slot_by_id(self, slot_id: int):
        return self.session.get(Slot, slot_id)

    def delete_slot(self, slot_id: int):
        slot = self.get_slot_by_id(slot_id)
        if slot:
            self.session.delete(slot)
            self.session.commit()
            return True
        return False
