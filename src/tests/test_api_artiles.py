from uuid import uuid4

import pytest
from httpx import AsyncClient
from pydantic import HttpUrl


@pytest.mark.asyncio
async def test_create_and_get_article(client: AsyncClient, session):
    from src.domain.models import Category, User
    from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW

    uow = SQLAlchemyUoW(session)
    author = User.create(email="a@b.c", password="pwd")
    category = Category(id=uuid4(), name="python")

    async with uow:
        await uow.users.add(author)
        await uow.categories.add(category)

    token = (
        await client.post(
            "/auth/login",
            data={"username": author.email, "password": "pwd"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    ).json()["access_token"]

    payload = {
        "title": "pytest tips",
        "content": "useful stuff",
        "category_id": str(category.id),
        "image_url": HttpUrl("http://fake/img.png"),
    }
    resp = await client.post(
        "/articles", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201
    art_id = resp.json()["id"]

    resp = await client.get(f"/articles/{art_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "pytest tips"
