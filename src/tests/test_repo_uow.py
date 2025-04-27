from uuid import uuid4

import pytest

from src.domain.models import Article, Category, User
from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW


@pytest.mark.asyncio
async def test_user_repo_crud(session):
    uow = SQLAlchemyUoW(session)
    user = User(id=uuid4(), email="dev@example.com", hashed_password="x")
    async with uow:
        await uow.users.add(user)

    async with uow:
        fetched = await uow.users.by_email("dev@example.com")
        assert fetched == user


@pytest.mark.asyncio
async def test_article_save_and_soft_delete(session):
    uow = SQLAlchemyUoW(session)

    cat = Category(id=uuid4(), name="tech")
    usr = User(id=uuid4(), email="a@b.c", hashed_password="x")
    art = Article(
        id=uuid4(), title="HDR", content="...", author_id=usr.id, category_id=cat.id
    )

    async with uow:
        await uow.categories.add(cat)
        await uow.users.add(usr)
        await uow.articles.add(art)

    async with uow:
        await uow.articles.soft_delete(art.id)

    async with uow:
        assert (await uow.articles.by_id(art.id)).is_deleted is True
