import asyncio
from typing import AsyncGenerator, Generator

import pytest
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.main import app as real_app
from src.infrastructure.celery_app import celery_app
from src.infrastructure.orm import Base
from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW, get_uow
from src.settings import settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def _engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(_engine, expire_on_commit=False)
    async with async_session() as ses:
        yield ses
        await ses.rollback()


@pytest.fixture
def app(session: AsyncSession) -> FastAPI:
    test_uow = SQLAlchemyUoW(session)
    real_app.dependency_overrides[get_uow] = lambda: test_uow
    return real_app


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[TestClient, None]:
    async with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def _monkeypatch_s3(monkeypatch):
    class _Dummy:
        def put_object(self, **kw): ...
        def list_buckets(self):
            return {"Buckets": [{"Name": settings.s3_bucket}]}

        def create_bucket(self, **kw): ...

    monkeypatch.setattr("src.utils.s3._get_client", lambda: _Dummy())


@pytest.fixture(autouse=True, scope="session")
def _force_celery_eager():
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True
    yield
    celery_app.conf.task_always_eager = False
