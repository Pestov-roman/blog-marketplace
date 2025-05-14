import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_and_protected_endpoint(client: AsyncClient, session):
    from src.auth.roles import Role
    from src.domain.models import User
    from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW

    uow = SQLAlchemyUoW(session)
    user = User.create(email="admin@site.com", password="secret", role=Role.ADMIN)
    await uow.users.add(user)
    await uow.commit()

    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@site.com", "password": "secret"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    resp = await client.get("/api/v1/categories", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
