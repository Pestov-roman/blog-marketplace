import pytest
from domain.models import User
from infrastructure.orm import Base
from infrastructure.repositories.sqlalchemy import SQLUserRepo
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest.fixture
async def session():
    eng = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(
        eng,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest.mark.asyncio
async def test_user_add_and_get(session: AsyncSession):
    repo = SQLUserRepo(session)
    user = User(
        email="test@test.com",
        password="test",
    )
    await repo.add(user)
    await session.commit()

    fetched = await repo.by_email("test@test.com")
    assert fetched and fetched.email == "test@test.com"
