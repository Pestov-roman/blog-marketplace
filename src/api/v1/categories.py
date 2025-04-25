from fastapi import APIRouter, Depends, status

from src.application.ports.uow import UnitOfWork
from src.domain.models import Category
from src.infrastructure.uow.sqlalchemy import get_uow
from src.schemas.category import CategoryIn, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryOut,
)
async def create_category(
    dto: CategoryIn,
    uow: UnitOfWork = Depends(get_uow),
):
    category = Category.create(dto.title)
    await uow.categories.add(category)
    await uow.commit()
    return category
