from dataclasses import dataclass
from uuid import UUID, uuid4
from typing import List

from src.domain.entities.book import Book
from src.domain.entities.author import Author
from src.domain.repositories.book_repository import IBookRepository
from src.domain.repositories.author_repository import IAuthorRepository
from src.domain.events.book_events import BookCreatedEvent
from src.infrastructure.messaging.publisher import EventPublisher


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
        author_repository: IAuthorRepository,
        event_publisher: EventPublisher | None = None
    ):
        self._book_repo = book_repository
        self._author_repo = author_repository
        self._event_publisher = event_publisher
    
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
        
        # Publish BookCreatedEvent
        if self._event_publisher:
            event = BookCreatedEvent(
                book_id=created_book.id,
                title=created_book.title,
                author_ids=command.author_ids
            )
            await self._event_publisher.publish(
                routing_key="book.created",
                event_data={
                    "book_id": str(event.book_id),
                    "title": event.title,
                    "author_ids": [str(aid) for aid in event.author_ids],
                    "occurred_at": event.occurred_at.isoformat()
                }
            )
        
        return created_book