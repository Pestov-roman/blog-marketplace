import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_article(client: AsyncClient, session):
    from src.auth.roles import Role
    from src.domain.models import Category, User
    from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW

    uow = SQLAlchemyUoW(session)
    author = User.create(email="a@b.c", password="pwd", role=Role.AUTHOR)
    category = Category.create(title="python")

    await uow.users.add(author)
    await uow.categories.add(category)
    await uow.commit()

    token = (
        await client.post(
            "/auth/login",
            json={"email": "a@b.c", "password": "pwd"},
        )
    ).json()["access_token"]

    article_data = {
        "title": "Test Article",
        "content": "Test Content",
        "category_id": category.id,
        "image_url": "https://example.com/image.jpg",
    }

    resp = await client.post(
        "/articles",
        json=article_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    article_id = resp.json()["id"]

    resp = await client.get(f"/articles/{article_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == article_data["title"]
