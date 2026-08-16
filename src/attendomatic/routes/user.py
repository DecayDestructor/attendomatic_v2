from ..dependencies import get_user_service
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/user/{user_id}")
async def get_user_by_id(user_id: int, user_service=Depends(get_user_service)):
    user = user_service.get_user_by_id(user_id)
    if user:
        return user
    else:
        return {"error": "User not found"}


@router.get("/user/email/{email}")
async def get_user_by_email(email: str, user_service=Depends(get_user_service)):
    user = user_service.get_user_by_email(email)
    if user:
        return user
    else:
        return {"error": "User not found"}


@router.get("/user/uid/{uid}")
async def get_user_by_uid(uid: str, user_service=Depends(get_user_service)):
    user = user_service.get_user_by_uid(uid)
    if user:
        return user
    else:
        return {"error": "User not found"}
