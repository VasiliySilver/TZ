from dataclasses import dataclass
from uuid import UUID

from src.domain.repositories.book_repository import IBookRepository
from src.domain.events.book_events import BookDeletedEvent


@dataclass
class DeleteBookCommand:
    """Command to delete a book"""
    book_id: UUID


class DeleteBookHandler:
    """Handler for DeleteBookCommand"""
    
    def __init__(self, book_repository: IBookRepository):
        self._book_repo = book_repository
    
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
        
        # TODO: Publish BookDeletedEvent