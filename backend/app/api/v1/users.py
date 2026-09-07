from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.schemas.user import UserPublic


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserPublic,
)
def get_me(
    current_user: dict = Depends(get_current_user),
):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "role": current_user["role"],
        "is_active": current_user["is_active"],
        "created_at": current_user["created_at"],
    }