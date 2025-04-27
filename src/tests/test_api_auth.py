import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_and_protected_endpoint(client: AsyncClient, session):
    from src.domain.models import User
    from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW

    uow = SQLAlchemyUoW(session)
    async with uow:
        await uow.users.add(User.create(email="admin@site.com", password="secret"))

    resp = await client.post(
        "/auth/login",
        data={"username": "admin@site.com", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    resp = await client.get("/categories", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
