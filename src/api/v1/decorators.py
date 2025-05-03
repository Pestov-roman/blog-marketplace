from typing import Callable, cast

from fastapi import Depends, HTTPException, status

from src.auth.dependencies import UserWithRole, get_current_user
from src.domain.models import Role, User


def _normalise(role: Role | str) -> str:
    return role.value if isinstance(role, Role) else str(role)


def require_roles(*allowed: Role | str) -> Callable[..., User]:
    allowed_norm = {_normalise(r) for r in allowed}

    async def _checker(user: UserWithRole = Depends(get_current_user)) -> User:
        user_role = user["role"]
        if not isinstance(user_role, Role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid role type",
            )
        if _normalise(user_role) not in allowed_norm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )
        return user["instance"]

    return cast(Callable[..., User], Depends(_checker))
