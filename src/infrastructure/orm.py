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

    articles: Mapped[list["ArticleORM"]] = relationship(back_populates="author")


class CategoryORM(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


class ArticleORM(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=225), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(length=225))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    category: Mapped["CategoryORM"] = relationship()
    author: Mapped["UserORM"] = relationship(back_populates="articles")


class ArticleDeletedORM(Base):
    __tablename__ = "article_deleted"
    __table_args__ = {"info": {"is_deprecated": True}}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=225))
    content: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(length=225))
    deleted_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
