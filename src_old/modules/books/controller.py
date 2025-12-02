from typing import Annotated, AsyncIterator, List

from fastapi import Depends

from src.infra.postgres.uow import PostgresUnitOfWorkDep
from src.modules.base.controller import BaseController
from src.modules.books.schemas import BookCreateRequest, BookResponse


class BookController(BaseController):
    async def read_books(self) -> List[BookResponse]:
        books = await self.uow.book.read_books()
        return [
            BookResponse(
                id=book.id,
                title=book.title,
                pages=book.pages,
                genre=book.genre,
                publication_year=book.publication_year,
                authors=[author.id for author in book.authors]
                
            )
            for book in books
        ]
    async def create_book(self, book_data: BookCreateRequest) -> BookResponse:
        book = await self.uow.book.create_book(book_data)
        return BookResponse(
            id=book.id,
            title=book.title,
            authors=[author.id for author in book.authors],
            publication_year=book.publication_year,
            pages=book.pages,
            genre=book.genre
        )


async def get_controller(uow: PostgresUnitOfWorkDep) -> AsyncIterator[BookController]:
    yield BookController(uow=uow)


BookControllerDep = Annotated[BookController, Depends(get_controller)]
