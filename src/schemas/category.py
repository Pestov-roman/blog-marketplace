from datetime import datetime

from pydantic import BaseModel, Field


class CategoryIn(BaseModel):
    """DTO при создании категории (из запроса)."""

    title: str = Field(min_length=2, max_length=100, examples=["Tech"])


class CategoryOut(BaseModel):
    """DTO для ответа API."""

    id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}
