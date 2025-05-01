from typing import Any, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.uow import UnitOfWork
from src.infrastructure.db import get_session
from src.infrastructure.repositories.sqlalchemy import (
    SQLArticleRepo,
    SQLCategoryRepo,
    SQLUserRepo,
)


class SQLAlchemyUoW(UnitOfWork):
    users: SQLUserRepo
    categories: SQLCategoryRepo
    articles: SQLArticleRepo

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = SQLUserRepo(session)
        self.categories = SQLCategoryRepo(session)
        self.articles = SQLArticleRepo(session)

    async def __aenter__(self) -> "SQLAlchemyUoW":
        if hasattr(self.session, "__anext__"):
            self.session = await self.session.__anext__()
            self.users = SQLUserRepo(self.session)
            self.categories = SQLCategoryRepo(self.session)
            self.articles = SQLArticleRepo(self.session)
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any
    ) -> None:
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


async def get_uow(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[UnitOfWork]:
    async with SQLAlchemyUoW(session) as uow:
        yield uow
