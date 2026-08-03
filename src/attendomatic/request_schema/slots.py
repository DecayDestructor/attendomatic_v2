from pydantic import BaseModel
from ..models.models import Type


class GetAllSlots(BaseModel):
    subject_id: int | None = None
    day_of_week: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    type: Type | None = None


class GetSingleSlot(BaseModel):
    subject_id: int | None = None
    day_of_week: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    type: Type | None = None


class GetSlotById(BaseModel):
    slot_id: int
