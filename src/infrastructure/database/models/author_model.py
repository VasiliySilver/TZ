from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from src.infrastructure.database.models.base import Base


if TYPE_CHECKING:
    from src.infrastructure.database.models.book_model import BookModel

class AuthorModel(Base):
    """SQLAlchemy model for Author"""
    __tablename__ = "authors"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationship to books (many-to-many)
    books: Mapped[list["BookModel"]] = relationship(
        "BookModel",
        secondary="book_author",
        back_populates="authors",
        lazy="selectin"  # Eager loading to avoid N+1
    )

    def __repr__(self) -> str:
        return f"<AuthorModel(id={self.id}, name={self.name})>"