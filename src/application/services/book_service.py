from uuid import UUID
from typing import List, Optional

from src.domain.entities.book import Book
from src.application.commands.create_book import CreateBookCommand, CreateBookHandler
from src.application.commands.update_book import UpdateBookCommand, UpdateBookHandler
from src.application.commands.delete_book import DeleteBookCommand, DeleteBookHandler
from src.application.queries.get_all_books import GetAllBooksQuery, GetAllBooksHandler
from src.application.queries.get_book_by_id import GetBookByIdQuery, GetBookByIdHandler
from src.infrastructure.database.unit_of_work import UnitOfWork
from src.infrastructure.messaging.publisher import EventPublisher


class BookService:
    """
    Application service for managing books.
    Orchestrates commands and queries through handlers.
    """
    
    def __init__(self, uow: UnitOfWork, event_publisher: EventPublisher | None = None):
        self._uow = uow
        
        # Initialize command handlers with event publisher
        self._create_handler = CreateBookHandler(uow.books, uow.authors, event_publisher)
        self._update_handler = UpdateBookHandler(uow.books, uow.authors, event_publisher)
        self._delete_handler = DeleteBookHandler(uow.books, event_publisher)
        
        # Initialize query handlers
        self._get_all_handler = GetAllBooksHandler(uow.books)
        self._get_by_id_handler = GetBookByIdHandler(uow.books)
    
    async def create_book(
        self,
        title: str,
        pages: int,
        genre: str,
        publication_year: int,
        author_ids: List[UUID]
    ) -> Book:
        """Create a new book and publish event"""
        command = CreateBookCommand(
            title=title,
            pages=pages,
            genre=genre,
            publication_year=publication_year,
            author_ids=author_ids
        )
        
        book = await self._create_handler.handle(command)
        await self._uow.commit()
        return book
    
    async def update_book(
        self,
        book_id: UUID,
        title: str,
        pages: int,
        genre: str,
        publication_year: int,
        author_ids: List[UUID]
    ) -> Book:
        """Update an existing book and publish event"""
        command = UpdateBookCommand(
            book_id=book_id,
            title=title,
            pages=pages,
            genre=genre,
            publication_year=publication_year,
            author_ids=author_ids
        )
        
        book = await self._update_handler.handle(command)
        await self._uow.commit()
        return book
    
    async def delete_book(self, book_id: UUID) -> None:
        """Delete a book and publish event"""
        command = DeleteBookCommand(book_id=book_id)
        await self._delete_handler.handle(command)
        await self._uow.commit()
    
    async def get_all_books(self) -> List[Book]:
        """Get all books"""
        query = GetAllBooksQuery()
        return await self._get_all_handler.handle(query)
    
    async def get_book_by_id(self, book_id: UUID) -> Optional[Book]:
        """Get a book by ID"""
        query = GetBookByIdQuery(book_id=book_id)
        return await self._get_by_id_handler.handle(query)