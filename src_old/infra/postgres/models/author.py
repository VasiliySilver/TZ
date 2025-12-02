from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UUID as PGUUID, text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.postgres.models.base import Base


if TYPE_CHECKING:
    from src.infra.postgres.models import Book


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(100))

    books: Mapped[List["Book"]] = relationship(
        "Book",
        secondary="book_author",
        back_populates="authors"
    )
