from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.application.ports.uow import UnitOfWork
from src.auth.jwt import verify_token
from src.infrastructure.uow.sqlalchemy import get_uow

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: UnitOfWork = Depends(get_uow),
):
    sub = verify_token(token)
    user = await uow.users.by_id(UUID(sub))
    return user
