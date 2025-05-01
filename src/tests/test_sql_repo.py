import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.auth.roles import Role
from src.domain.models import User
from src.infrastructure.orm import Base
from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW


@pytest.fixture
async def session():
    eng = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(
        eng,
        expire_on_commit=False,
    )

    async with session_maker() as session:
        yield session


@pytest.mark.asyncio
async def test_user_add_and_get(session: AsyncSession):
    async with SQLAlchemyUoW(session) as uow:
        user = User.create(
            email="test@test.com",
            password="test",
            role=Role.ADMIN,
        )
        await uow.users.add(user)
        await uow.commit()

        found = await uow.users.by_email("test@test.com")
        assert found is not None
        assert found.email == user.email
        assert found.role == Role.ADMIN
