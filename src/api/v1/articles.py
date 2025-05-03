from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.application.ports.uow import UnitOfWork
from src.auth.dependencies import UserWithRole, get_current_user, require_roles
from src.auth.roles import Role
from src.domain.models import Article, User
from src.infrastructure.uow.sqlalchemy import get_uow
from src.schemas.article import ArticleIn, ArticleOut

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ArticleOut)
async def create_article(
    dto: ArticleIn,
    uow: UnitOfWork = Depends(get_uow),
    user: UserWithRole = Depends(get_current_user),
    current_user: User = Depends(require_roles(Role.AUTHOR)),
) -> Article:
    user_instance = user["instance"]
    article = Article.create(
        title=dto.title,
        content=dto.content,
        image_url=dto.image_url,
        category_id=dto.category_id,
        author_id=user_instance.id,
    )
    await uow.articles.add(article)
    await uow.commit()
    return article


@router.get("", response_model=list[ArticleOut])
async def list_articles(
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    uow: UnitOfWork = Depends(get_uow),
    current_user: User = Depends(require_roles(Role.READER)),
) -> list[Article]:
    offset = (page - 1) * size
    items, total = await uow.articles.list(
        search=search, category_id=category_id, offset=offset, limit=size
    )
    return items


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    uow: UnitOfWork = Depends(get_uow),
    current_user: User = Depends(require_roles(Role.AUTHOR, Role.ADMIN)),
) -> None:
    await uow.articles.soft_delete(article_id, datetime.utcnow())
    await uow.commit()


@router.get("/{article_id}", response_model=ArticleOut)
async def get_article(
    article_id: int,
    uow: UnitOfWork = Depends(get_uow),
) -> Article:
    art = await uow.articles.get(article_id)
    if not art:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    return art


@router.put("/{article_id}", response_model=ArticleOut)
async def update_article(
    article_id: int,
    dto: ArticleIn,
    uow: UnitOfWork = Depends(get_uow),
    user: UserWithRole = Depends(get_current_user),
    current_user: User = Depends(require_roles(Role.AUTHOR, Role.ADMIN)),
) -> Article:
    art = await uow.articles.get(article_id)
    if not art:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    user_instance = user["instance"]
    if art.author_id != user_instance.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this article",
        )
    art.title = dto.title
    art.content = dto.content
    art.image_url = dto.image_url or art.image_url
    art.category_id = dto.category_id
    await uow.articles.update(art)
    await uow.commit()
    return art
