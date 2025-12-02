from uuid import UUID
from typing import List, Optional

from src.domain.entities.book import Book
from src.application.commands.create_book import CreateBookCommand, CreateBookHandler
from src.application.commands.update_book import UpdateBookCommand, UpdateBookHandler
from src.application.commands.delete_book import DeleteBookCommand, DeleteBookHandler
from src.application.queries.get_all_books import GetAllBooksQuery, GetAllBooksHandler
from src.application.queries.get_book_by_id import GetBookByIdQuery, GetBookByIdHandler
from src.infrastructure.database.unit_of_work import UnitOfWork


class BookService:
    """
    Application service for managing books.
    Orchestrates commands and queries through handlers.
    """
    
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
        
        # Initialize command handlers
        self._create_handler = CreateBookHandler(uow.books, uow.authors)
        self._update_handler = UpdateBookHandler(uow.books, uow.authors)
        self._delete_handler = DeleteBookHandler(uow.books)
        
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
        """
        Create a new book.
        
        Args:
            title: Book title
            pages: Number of pages
            genre: Book genre
            publication_year: Year of publication
            author_ids: List of author UUIDs
            
        Returns:
            Created Book entity
            
        Raises:
            ValueError: If validation fails or authors don't exist
        """
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
        """
        Update an existing book.
        
        Args:
            book_id: Book UUID
            title: Updated book title
            pages: Updated number of pages
            genre: Updated book genre
            publication_year: Updated year of publication
            author_ids: Updated list of author UUIDs
            
        Returns:
            Updated Book entity
            
        Raises:
            ValueError: If book not found or validation fails
        """
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
        """
        Delete a book.
        
        Args:
            book_id: Book UUID
            
        Raises:
            ValueError: If book not found
        """
        command = DeleteBookCommand(book_id=book_id)
        await self._delete_handler.handle(command)
        await self._uow.commit()
    
    async def get_all_books(self) -> List[Book]:
        """
        Get all books.
        
        Returns:
            List of Book entities
        """
        query = GetAllBooksQuery()
        return await self._get_all_handler.handle(query)
    
    async def get_book_by_id(self, book_id: UUID) -> Optional[Book]:
        """
        Get a book by ID.
        
        Args:
            book_id: Book UUID
            
        Returns:
            Book entity or None if not found
        """
        query = GetBookByIdQuery(book_id=book_id)
        return await self._get_by_id_handler.handle(query)