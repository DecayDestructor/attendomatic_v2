from pydantic import BaseModel


class GetUserByIdRequest(BaseModel):
    user_id: int


class GetUserByEmailRequest(BaseModel):
    email: str


class GetUserByUidRequest(BaseModel):
    uid: str


class GetUserResponse(BaseModel):
    user_id: int
    email: str
    uid: str
    name: str
