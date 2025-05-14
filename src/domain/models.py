from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from passlib.hash import bcrypt
from pydantic import BaseModel, Field

from src.auth.roles import Role


class User(BaseModel):
    id: UUID
    email: str
    hashed_password: str
    role: Role
    created_at: datetime = Field(default_factory=lambda: datetime.now())

    @classmethod
    def create(
        cls, email: str, password: str, role: Role | str = Role.READER
    ) -> "User":
        if isinstance(role, str):
            role = Role.from_str(role)
        return cls(
            id=uuid4(),
            email=email,
            hashed_password=bcrypt.hash(password),
            role=role,
        )


class Category(BaseModel):
    id: int | None
    title: str = Field(alias="name")
    created_at: datetime = Field(default_factory=lambda: datetime.now())

    model_config = {"populate_by_name": True}

    @classmethod
    def create(cls, title: str) -> "Category":
        return cls(id=None, title=title.strip())


class Article(BaseModel):
    id: int | None
    title: str
    content: str
    author_id: UUID
    category_id: int | None
    image_url: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    is_deleted: bool = False

    model_config = {"from_attributes": True}

    @classmethod
    def create(
        cls,
        *,
        title: str,
        content: str,
        author_id: UUID,
        category_id: int | None = None,
        image_url: str | None = None,
    ) -> "Article":
        now = datetime.now()
        return cls(
            id=None,
            title=title.strip(),
            content=content,
            author_id=author_id,
            category_id=category_id,
            image_url=image_url,
            created_at=now,
            updated_at=now,
            is_deleted=False,
        )


__all__ = ["User", "Category", "Article", "Role"]
