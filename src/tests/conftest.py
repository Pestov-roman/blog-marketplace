import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.main import app as real_app
from src.infrastructure.celery_app import celery_app
from src.infrastructure.orm import Base
from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW, get_uow
from src.settings import settings


@pytest.fixture(scope="session")
def async_session_maker(
    _engine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def _engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(async_session_maker) -> AsyncSession:
    async with async_session_maker() as session:
        async with session.begin():
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
            await session.commit()
        yield session


@pytest.fixture
def app(session: AsyncSession) -> FastAPI:
    test_uow = SQLAlchemyUoW(session)
    real_app.dependency_overrides[get_uow] = lambda: test_uow
    return real_app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[TestClient, None]:
    async with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def _monkeypatch_s3(monkeypatch):
    if not hasattr(settings, "s3_bucket"):
        settings.s3_bucket = "test-bucket"

    class _Dummy:
        def put_object(self, **kw): ...
        def list_buckets(self):
            return {"Buckets": [{"Name": settings.s3_bucket}]}

        def create_bucket(self, **kw): ...

    monkeypatch.setattr("src.utils.s3._get_client", lambda: _Dummy())


@pytest.fixture(autouse=True)
def _monkeypatch_jwt(monkeypatch):
    monkeypatch.setattr("src.settings.base.settings.jwt_secret_key", "test_secret_key")


@pytest.fixture(autouse=True, scope="session")
def _force_celery_eager():
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True
    yield
    celery_app.conf.task_always_eager = False
