from typing import TYPE_CHECKING

from uuid import UUID
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from src.infrastructure.database.models.base import Base


if TYPE_CHECKING:
    from src.infrastructure.database.models.author_model import AuthorModel


class BookModel(Base):
    """SQLAlchemy model for Book"""
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default="gen_random_uuid()"
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship to authors (many-to-many)
    authors: Mapped[list["AuthorModel"]] = relationship(
        "AuthorModel",
        secondary="book_author",
        back_populates="books",
        lazy="selectin"  # Eager loading to avoid N+1
    )

    def __repr__(self) -> str:
        return f"<BookModel(id={self.id}, title={self.title})>"