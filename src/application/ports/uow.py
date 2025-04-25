from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.application.ports import (
    ArticleRepository,
    CategoryRepository,
    UserRepository,
)


@runtime_checkable
class UnitOfWork(Protocol):
    users: UserRepository
    categories: CategoryRepository
    articles: ArticleRepository

    async def __aenter__(self) -> "UnitOfWork": ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
