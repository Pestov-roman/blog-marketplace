from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(slots=True, frozen=True)
class User:
    id: UUID
    email: str
    hashed_password: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(cls, email: str, hashed_password: str) -> "User":
        return cls(id=uuid4(), email=email.lower(), hashed_password=hashed_password)


@dataclass(slots=True)
class Category:
    id: int | None
    title: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(cls, title: str) -> "Category":
        return cls(id=None, title=title.strip())


class Article:
    id: int | None
    title: str
    content: str
    author_id: UUID
    category_id: int
    image_url: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_deleted: bool = False

    @classmethod
    def create(
        cls,
        *,
        title: str,
        content: str,
        author_id: UUID,
        category_id: int,
        image_url: str | None = None,
    ) -> "Article":
        now = datetime.utcnow()
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


__all__ = [
    "User",
    "Category",
    "Article",
]
