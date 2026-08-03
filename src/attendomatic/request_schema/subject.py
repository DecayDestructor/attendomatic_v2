from pydantic import BaseModel


class GetSubjectByCodeRequest(BaseModel):
    subject_code: str


class GetSubjectByIdRequest(BaseModel):
    subject_id: int


class GetSubjectsByUserIdRequest(BaseModel):
    user_id: int


class CreateSubjectRequest(BaseModel):
    name: str
    code: str
