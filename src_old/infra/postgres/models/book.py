from typing import List
from sqlalchemy import UUID as PGUUID, Integer, text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infra.postgres.models.author import Author
from src.infra.postgres.models.base import Base


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[PGUUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    title: Mapped[str] = mapped_column(String(250))
    pages: Mapped[Integer] = mapped_column(Integer)
    genre: Mapped[String] = mapped_column(String(100))
    publication_year: Mapped[Integer] = mapped_column(Integer)


    authors: Mapped[List["Author"]] = relationship(
        "Author",
        secondary="book_author",
        back_populates="books"
    )    


