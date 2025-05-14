from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.uow import UnitOfWork
from src.infrastructure.db import get_session
from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW


async def get_uow(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[UnitOfWork]:
    async with SQLAlchemyUoW(session) as uow:
        yield uow
