from dataclasses import dataclass
from uuid import UUID
from typing import List

from src.domain.entities.book import Book
from src.domain.repositories.book_repository import IBookRepository
from src.domain.repositories.author_repository import IAuthorRepository
from src.domain.events.book_events import BookUpdatedEvent


@dataclass
class UpdateBookCommand:
    """Command to update an existing book"""
    book_id: UUID
    title: str
    pages: int
    genre: str
    publication_year: int
    author_ids: List[UUID]


class UpdateBookHandler:
    """Handler for UpdateBookCommand"""
    
    def __init__(
        self,
        book_repository: IBookRepository,
        author_repository: IAuthorRepository
    ):
        self._book_repo = book_repository
        self._author_repo = author_repository
    
    async def handle(self, command: UpdateBookCommand) -> Book:
        """
        Handle the update book command.
        
        Args:
            command: UpdateBookCommand with updated book data
            
        Returns:
            Updated Book entity
            
        Raises:
            ValueError: If book or authors don't exist
        """
        # Check if book exists
        existing_book = await self._book_repo.get_by_id(command.book_id)
        if existing_book is None:
            raise ValueError(f"Book with id {command.book_id} not found")
        
        # Fetch authors from database
        authors = await self._author_repo.get_by_ids(command.author_ids)
        
        if len(authors) != len(command.author_ids):
            raise ValueError("Some authors do not exist")
        
        # Create updated book entity
        updated_book = Book(
            id=command.book_id,
            title=command.title,
            pages=command.pages,
            genre=command.genre,
            publication_year=command.publication_year,
            authors=authors
        )
        
        # Update in repository
        result = await self._book_repo.update(updated_book)
        
        # TODO: Publish BookUpdatedEvent
        
        return result