from dataclasses import dataclass
from uuid import UUID

from src.domain.repositories.book_repository import IBookRepository
from src.domain.events.book_events import BookDeletedEvent
from src.infrastructure.messaging.publisher import EventPublisher


@dataclass
class DeleteBookCommand:
    """Command to delete a book"""
    book_id: UUID


class DeleteBookHandler:
    """Handler for DeleteBookCommand"""
    
    def __init__(
        self,
        book_repository: IBookRepository,
        event_publisher: EventPublisher | None = None
    ):
        self._book_repo = book_repository
        self._event_publisher = event_publisher
    
    async def handle(self, command: DeleteBookCommand) -> None:
        """
        Handle the delete book command.
        
        Args:
            command: DeleteBookCommand with book_id
            
        Raises:
            ValueError: If book doesn't exist
        """
        # Check if book exists
        existing_book = await self._book_repo.get_by_id(command.book_id)
        if existing_book is None:
            raise ValueError(f"Book with id {command.book_id} not found")
        
        # Delete from repository
        await self._book_repo.delete(command.book_id)
        
        # Publish BookDeletedEvent
        if self._event_publisher:
            event = BookDeletedEvent(book_id=command.book_id)
            await self._event_publisher.publish(
                routing_key="book.deleted",
                event_data={
                    "book_id": str(event.book_id),
                    "occurred_at": event.occurred_at.isoformat()
                }
            )