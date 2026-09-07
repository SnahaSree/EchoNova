from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token
from app.repositories.user_repository import user_repository


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(bearer_scheme),
    ],
) -> dict:
    token = credentials.credentials

    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        )

    user = user_repository.find_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found.",
        )

    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user

def require_role(required_role: str):
    def role_checker(
        current_user: dict = Depends(get_current_user),
    ) -> dict:
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return role_checker