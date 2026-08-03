from pydantic import BaseModel


class GetUserByIdRequest(BaseModel):
    user_id: int


class GetUserByEmailRequest(BaseModel):
    email: str
