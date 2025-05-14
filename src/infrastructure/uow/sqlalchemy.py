from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.uow import UnitOfWork
from src.infrastructure.repositories.sqlalchemy import (
    ArticleRepo,
    CategoryRepo,
    UserRepo,
)


class SQLAlchemyUoW(UnitOfWork):
    users: UserRepo
    categories: CategoryRepo
    articles: ArticleRepo

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepo(session)
        self.categories = CategoryRepo(session)
        self.articles = ArticleRepo(session)

    async def __aenter__(self) -> "SQLAlchemyUoW":
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
