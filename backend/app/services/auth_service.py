from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import user_repository
from app.schemas.user import LoginRequest, TokenResponse, UserCreate


class AuthService:
    def register(self, data: UserCreate) -> str:
        existing_user = user_repository.find_by_email(data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        password_hash = hash_password(data.password)

        try:
            return user_repository.create(
                email=data.email,
                password_hash=password_hash,
            )
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

    def login(self, data: LoginRequest) -> TokenResponse:
        user = user_repository.find_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(
            data.password,
            user["password_hash"],
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is inactive.",
            )

        user_id = str(user["_id"])

        return TokenResponse(
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(user_id),
        )


auth_service = AuthService()