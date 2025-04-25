from datetime import datetime

from fastapi import APIRouter, Depends, Query, status

from src.application.ports.uow import UnitOfWork
from src.auth.dependencies import get_current_user
from src.domain.models import Article
from src.infrastructure.uow.sqlalchemy import get_uow
from src.schemas.article import ArticleIn, ArticleOut

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ArticleOut)
async def create_article(
    dto: ArticleIn,
    uow: UnitOfWork = Depends(get_uow),
    user=Depends(get_current_user),
):
    article = Article.create(
        title=dto.title,
        content=dto.content,
        image_url=dto.image_url,
        category_id=dto.category_id,
        author_id=user.id,
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
):
    offset = (page - 1) * size
    items, total = await uow.articles.list(
        search=search, category_id=category_id, offset=offset, limit=size
    )
    return items


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    await uow.articles.soft_delete(article_id, datetime.utcnow())
    await uow.commit()
