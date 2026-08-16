from pydantic import BaseModel


class CreateSubjectRequest(BaseModel):
    name: str
    code: str
    user_email: str  # Only allow admin users to create subjects, so we need the email of the user making the request


class DeleteSubjectRequest(BaseModel):
    subject_id: int
    user_email: str  # Only allow admin users to delete subjects, so we need the email of the user making the request


class UpdateSubjectRequest(BaseModel):
    subject_id: int
    name: str | None = None
    code: str | None = None
    user_email: str  # Only allow admin users to modify subjects, so we need the email of the user making the request
