from pydantic import BaseModel


class GetTimetableRequest(BaseModel):
    user_id: int


class CreateTimetableRequest(BaseModel):
    user_id: int
    slot_id: int


class GetTimetableByIdRequest(BaseModel):
    timetable_id: int
