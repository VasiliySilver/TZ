"""
Unit tests for DeleteBookHandler with mocks
"""
from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from src.application.commands.delete_book import DeleteBookCommand, DeleteBookHandler
from src.domain.entities.book import Book
from src.domain.entities.author import Author


@pytest.mark.asyncio
class TestDeleteBookHandler:
    """Test cases for DeleteBookHandler"""
    
    async def test_delete_book_success(self):
        """Test successful book deletion"""
        # Arrange
        mock_book_repo = AsyncMock()
        mock_event_publisher = AsyncMock()
        
        book_id = uuid4()
        existing_book = Book(
            id=book_id,
            title="Test Book",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            authors=[Author(id=uuid4(), name="Test Author")]
        )
        
        mock_book_repo.get_by_id.return_value = existing_book
        
        handler = DeleteBookHandler(mock_book_repo, mock_event_publisher)
        command = DeleteBookCommand(book_id=book_id)
        
        # Act
        await handler.handle(command)
        
        # Assert
        mock_book_repo.get_by_id.assert_called_once_with(book_id)
        mock_book_repo.delete.assert_called_once_with(book_id)
        mock_event_publisher.publish.assert_called_once()
        
        # Check event
        call_args = mock_event_publisher.publish.call_args
        assert call_args[1]['routing_key'] == "book.deleted"
    
    async def test_delete_non_existing_book(self):
        """Test deleting a book that doesn't exist"""
        # Arrange
        mock_book_repo = AsyncMock()
        
        book_id = uuid4()
        mock_book_repo.get_by_id.return_value = None  # Book not found
        
        handler = DeleteBookHandler(mock_book_repo)
        command = DeleteBookCommand(book_id=book_id)
        
        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            await handler.handle(command)
        
        mock_book_repo.delete.assert_not_called()