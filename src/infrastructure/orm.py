from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.auth.roles import Role
from src.domain.models import Article, Category, User


class Base(DeclarativeBase):
    pass


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(String(length=225), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(225), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    role: Mapped[str] = mapped_column(
        String(10), nullable=False, default=Role.READER.value
    )
    articles: Mapped[list["ArticleORM"]] = relationship(back_populates="author")

    @classmethod
    def from_entity(cls, user: User) -> "UserORM":
        data = user.model_dump()
        data["role"] = str(user.role)
        return cls(**data)

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            role=Role.from_str(self.role),
            created_at=self.created_at,
        )


class CategoryORM(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    @classmethod
    def from_entity(cls, category: Category) -> "CategoryORM":
        return cls(**category.model_dump())

    def to_entity(self) -> Category:
        return Category(
            id=self.id,
            title=self.title,
            created_at=self.created_at,
        )


class ArticleORM(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=225), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(length=225), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    category: Mapped["CategoryORM"] = relationship()
    author: Mapped["UserORM"] = relationship(back_populates="articles")

    @classmethod
    def from_entity(cls, article: Article) -> "ArticleORM":
        return cls(**article.model_dump(exclude_none=True))

    def to_entity(self) -> Article:
        return Article(
            id=self.id,
            title=self.title,
            content=self.content,
            author_id=self.author_id,
            category_id=self.category_id,
            image_url=self.image_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_deleted=self.is_deleted,
        )


class ArticleDeletedORM(Base):
    __tablename__ = "article_deleted"
    __table_args__ = {"info": {"is_deprecated": True}}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=225))
    content: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(length=225))
    deleted_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    @classmethod
    def from_entity(cls, article: Article) -> "ArticleDeletedORM":
        return cls(**article.model_dump())

    def to_entity(self) -> Article:
        return Article(
            id=self.id,
            title=self.title,
            content=self.content,
            image_url=self.image_url,
            created_at=self.deleted_at,
            updated_at=self.deleted_at,
            is_deleted=True,
            author_id=None,  # type: ignore
            category_id=None,  # type: ignore
        )
