from typing import Any, Callable, TypedDict
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

from src.application.ports.uow import UnitOfWork
from src.auth.jwt import verify_token
from src.auth.roles import Role
from src.domain.models import User
from src.infrastructure.uow.sqlalchemy import get_uow

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
header_scheme = HTTPBearer(auto_error=False)


class UserWithRole(TypedDict):
    instance: User
    role: Role


async def _extract_token(
    request: Request,
    header: HTTPAuthorizationCredentials | None = Depends(header_scheme),
) -> str:
    if token := request.cookies.get("access_token"):
        return token
    if header:
        return header.credentials
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
    )


async def get_current_user(
    token: str = Depends(_extract_token),
    uow: UnitOfWork = Depends(get_uow),
) -> UserWithRole:
    if not (payload := verify_token(token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    role: Role = Role.from_str(payload["role"])
    user = await uow.users.by_id(UUID(payload["sub"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return {"instance": user, "role": role}


def require_roles(*roles: Role) -> Callable[..., Any]:
    def _checker(user: UserWithRole = Depends(get_current_user)) -> User:
        user_role = user["role"]
        if not isinstance(user_role, Role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid role type",
            )
        if user_role not in roles:
            role_values = [r.value for r in roles]
            user_role_value = user_role.value
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {role_values}, but got {user_role_value}",
            )
        return user["instance"]

    return _checker
