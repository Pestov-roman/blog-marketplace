from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.models import Article, Category, User
from src.infrastructure.orm import ArticleORM, CategoryORM, UserORM


class SQLUserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> None:
        self.session.add(UserORM.from_entity(user))
        await self.session.flush()

    async def by_email(self, email: str) -> User | None:
        row = await self.session.scalar(select(UserORM).where(UserORM.email == email))
        return row.to_entity() if row else None

    async def by_id(self, id: UUID) -> User | None:
        row = await self.session.get(UserORM, id)
        return row.to_entity() if row else None


class SQLCategoryRepo:
    """SQLAlchemy-репозиторий категорий."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, category: Category) -> None:
        orm = CategoryORM.from_entity(category)
        self.session.add(orm)
        await self.session.flush()
        category.id = orm.id

    async def list(self) -> list[Category]:
        result = await self.session.scalars(
            select(CategoryORM).order_by(CategoryORM.created_at.desc())
        )
        rows = result.all()
        return [row.to_entity() for row in rows]

    async def get(self, cat_id: int) -> Category | None:
        row = await self.session.get(CategoryORM, cat_id)
        return row.to_entity() if row else None

    async def remove(self, cat_id: int) -> None:
        await self.session.execute(delete(CategoryORM).where(CategoryORM.id == cat_id))


class SQLArticleRepo:
    """SQLAlchemy-репозиторий статей с FTS и soft-delete."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, article: Article) -> None:
        orm = ArticleORM.from_entity(article)
        self.session.add(orm)
        await self.session.flush()
        article.id = orm.id

    async def get(self, id_: int) -> Article | None:
        stmt = (
            select(ArticleORM)
            .where(ArticleORM.id == id_)
            .options(selectinload(ArticleORM.category))
            .options(selectinload(ArticleORM.author))
        )
        result = await self.session.execute(stmt)
        article = result.scalar_one_or_none()
        return article.to_entity() if article else None

    async def list(
        self,
        *,
        search: str | None = None,
        category_id: int | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Article], int]:
        stmt = (
            select(ArticleORM)
            .options(selectinload(ArticleORM.category))
            .where(ArticleORM.is_deleted.is_(False))
        )
        if category_id:
            stmt = stmt.where(ArticleORM.category_id == category_id)
        if search:
            stmt = stmt.where(
                func.to_tsvector(
                    "russian", ArticleORM.title + " " + ArticleORM.content
                ).op("@@")(func.plainto_tsquery(search))
            )

        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = cast(int, await self.session.scalar(total_stmt))

        result = await self.session.scalars(
            stmt.order_by(ArticleORM.created_at.desc()).limit(limit).offset(offset)
        )
        rows = result.all()
        return [row.to_entity() for row in rows], total

    async def update(self, article: Article) -> None:
        await self.session.execute(
            update(ArticleORM)
            .where(ArticleORM.id == article.id)
            .values(
                title=article.title,
                content=article.content,
                image_url=article.image_url,
                category_id=article.category_id,
                updated_at=datetime.now(UTC),
            )
        )

    async def soft_delete(
        self, art_id: int, deleted_at: datetime | None = None
    ) -> None:
        if deleted_at is None:
            deleted_at = datetime.now(UTC)
        await self.session.execute(
            update(ArticleORM)
            .where(ArticleORM.id == art_id)
            .values(is_deleted=True, updated_at=deleted_at)
        )

    async def by_id(self, id: int) -> Article | None:
        return await self.get(id)
