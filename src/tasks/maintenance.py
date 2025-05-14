from datetime import datetime, timedelta

from celery import shared_task
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.infrastructure.orm import ArticleDeletedORM
from src.settings import settings

engine = create_async_engine(settings.sqlalchemy_database_uri, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


@shared_task(name="maintenance.cleanup_deleted_articles")  # type: ignore[misc]
async def cleanup_deleted_articles(days: int = 30) -> None:
    import asyncio

    cutoff = datetime.utcnow() - timedelta(days=days)

    async def _cleanup() -> None:
        async with async_session() as s:
            await s.execute(
                delete(ArticleDeletedORM).where(ArticleDeletedORM.deleted_at < cutoff)
            )
            await s.commit()

    asyncio.run(_cleanup())
