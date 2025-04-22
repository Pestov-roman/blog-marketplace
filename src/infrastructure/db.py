from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.settings import settings


def create_enginge() -> AsyncEngine:
    return create_async_engine(
        settings.sqlalchemy_database_uri,
        echo=settings.debug,
        future=True,
    )


engine: AsyncEngine = create_enginge()
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    async with SessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()
