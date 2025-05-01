import pytest

from src.domain.models import User


@pytest.mark.asyncio
async def test_user_repo_crud(session):
    from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW

    uow = SQLAlchemyUoW(session)
    user = User.create(email="dev@example.com", password="x")
    await uow.users.add(user)
    await uow.commit()

    fetched = await uow.users.by_email("dev@example.com")
    assert fetched.email == user.email


@pytest.mark.asyncio
async def test_article_save_and_soft_delete(session):
    from src.auth.roles import Role
    from src.domain.models import Article, Category, User
    from src.infrastructure.uow.sqlalchemy import SQLAlchemyUoW

    uow = SQLAlchemyUoW(session)

    cat = Category.create(title="tech")
    usr = User.create(email="a@b.c", password="x", role=Role.AUTHOR)

    await uow.categories.add(cat)
    await uow.users.add(usr)
    await uow.commit()

    art = Article.create(
        title="HDR",
        content="...",
        author_id=usr.id,
        category_id=cat.id,
    )

    await uow.articles.add(art)
    await uow.commit()

    found = await uow.articles.get(art.id)
    assert found is not None
    assert found.title == art.title
    assert found.category_id == cat.id

    await uow.articles.soft_delete(art.id)
    await uow.commit()

    found = await uow.articles.by_id(art.id)
    assert found is not None
    assert found.is_deleted is True
