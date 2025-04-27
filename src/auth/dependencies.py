from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from src.application.ports.uow import UnitOfWork
from src.auth.jwt import verify_token
from src.auth.roles import Role
from src.infrastructure.uow.sqlalchemy import get_uow

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
header_scheme = HTTPBearer(auto_error=False)


async def _extract_token(request: Request, header=Depends(header_scheme)):
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
):
    payload = verify_token(token)
    user_id = UUID(payload["sub"])
    role: Role = Role.from_str(payload["role"])
    user = await uow.users.by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return {"instance": user, "role": role}


def require_roles(*roles: Role):
    def _checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return user["instance"]

    return _checker
