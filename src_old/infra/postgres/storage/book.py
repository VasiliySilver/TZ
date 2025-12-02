from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.infra.postgres.models import Book
from src.infra.postgres.models.author import Author
from src.infra.postgres.storage.base_storage import PostgresStorage
from src.modules.books.schemas import BookCreateRequest


class BookStorage(PostgresStorage[Book]):
    async def create_book(self, book_data: BookCreateRequest) -> Book:
        authors_indb = await self._db.execute(
            select(Author).where(Author.id.in_(book_data.authors))
        )
        authors = authors_indb.scalars().all()
        book = Book(
            title=book_data.title,
            pages=book_data.pages,
            genre=book_data.genre,
            publication_year=book_data.publication_year,
            authors=authors
        )

        self._db.add(book)
        await self._db.flush()
        await self._db.refresh(book, ["authors"])

        return book

    async def read_books(self) -> Sequence[Book]:
        result = await self._db.execute(
            select(Book).options(selectinload(Book.authors))
        )
        return result.scalars().all()
