from fastapi import APIRouter, status

from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserCreate,
)
from app.services.auth_service import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserCreate):
    user_id = auth_service.register(data)

    return {
        "message": "Account created successfully.",
        "user_id": user_id,
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(data: LoginRequest):
    return auth_service.login(data)