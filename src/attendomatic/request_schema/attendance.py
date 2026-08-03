from pydantic import BaseModel
from datetime import date, time
from ..models.models import Type, Status


class AttendanceRequest(BaseModel):
    student_id: int
    subject_code: str
    type: Type
    status: Status
    is_regular: bool
    class_end_time: time
    class_date: date


class AttendanceQuery(BaseModel):
    student_id: int
    status: Status | None = None
    type: Type | None = None
    is_regular: bool | None = None
    start_date: date | None = None
    end_date: date | None = None
    subject_id: int | None = None
