from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ArticleIn(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    content: str
    category_id: int
    image_url: str | None = None


class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    image_url: str | None
    created_at: datetime
    updated_at: datetime
    author_id: UUID
    category_id: int

    model_config = {"from_attributes": True}
