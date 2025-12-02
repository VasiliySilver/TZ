from dataclasses import dataclass
from uuid import UUID, uuid4
from typing import List

from src.domain.entities.book import Book
from src.domain.entities.author import Author
from src.domain.repositories.book_repository import IBookRepository
from src.domain.repositories.author_repository import IAuthorRepository
from src.domain.events.book_events import BookCreatedEvent


@dataclass
class CreateBookCommand:
    """Command to create a new book"""
    title: str
    pages: int
    genre: str
    publication_year: int
    author_ids: List[UUID]


class CreateBookHandler:
    """Handler for CreateBookCommand"""
    
    def __init__(
        self,
        book_repository: IBookRepository,
        author_repository: IAuthorRepository
    ):
        self._book_repo = book_repository
        self._author_repo = author_repository
    
    async def handle(self, command: CreateBookCommand) -> Book:
        """
        Handle the create book command.
        
        Args:
            command: CreateBookCommand with book data
            
        Returns:
            Created Book entity
            
        Raises:
            ValueError: If some authors don't exist
        """
        # Fetch authors from database
        authors = await self._author_repo.get_by_ids(command.author_ids)
        
        if len(authors) != len(command.author_ids):
            raise ValueError("Some authors do not exist")
        
        # Create book entity
        book = Book(
            id=uuid4(),
            title=command.title,
            pages=command.pages,
            genre=command.genre,
            publication_year=command.publication_year,
            authors=authors
        )
        
        # Save to repository
        created_book = await self._book_repo.add(book)
        
        # TODO: Publish BookCreatedEvent
        # event = BookCreatedEvent(
        #     book_id=created_book.id,
        #     title=created_book.title,
        #     author_ids=command.author_ids
        # )
        
        return created_book