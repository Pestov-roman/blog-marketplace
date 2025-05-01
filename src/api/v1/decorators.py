from typing import Iterable

from fastapi import Depends, HTTPException, status

from src.auth.dependencies import get_current_user
from src.domain.models import Role


def _normalise(role) -> str:
    return role.value if isinstance(role, Role) else str(role)


def require_roles(*allowed: Iterable[Role | str]) -> Depends:
    allowed_norm = {_normalise(r) for r in allowed}

    async def _checker(user=Depends(get_current_user)):
        user_role = _normalise(user.role)
        if user_role not in allowed_norm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

    return Depends(_checker)
