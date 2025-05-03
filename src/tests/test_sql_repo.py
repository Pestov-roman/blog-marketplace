import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.roles import Role
from src.domain.models import User
from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW


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
