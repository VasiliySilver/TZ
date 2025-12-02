"""
Unit tests for UpdateBookHandler with mocks
"""
from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from src.application.commands.update_book import UpdateBookCommand, UpdateBookHandler
from src.domain.entities.book import Book
from src.domain.entities.author import Author


@pytest.mark.asyncio
class TestUpdateBookHandler:
    """Test cases for UpdateBookHandler"""
    
    async def test_update_book_success(self):
        """Test successful book update"""
        # Arrange
        mock_book_repo = AsyncMock()
        mock_author_repo = AsyncMock()
        mock_event_publisher = AsyncMock()
        
        book_id = uuid4()
        author_id = uuid4()
        author = Author(id=author_id, name="Test Author")
        
        existing_book = Book(
            id=book_id,
            title="Old Title",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            authors=[author]
        )
        
        updated_book = Book(
            id=book_id,
            title="Updated Title",
            pages=150,
            genre="Mystery",
            publication_year=2025,
            authors=[author]
        )
        
        mock_book_repo.get_by_id.return_value = existing_book
        mock_author_repo.get_by_ids.return_value = [author]
        mock_book_repo.update.return_value = updated_book
        
        handler = UpdateBookHandler(mock_book_repo, mock_author_repo, mock_event_publisher)
        command = UpdateBookCommand(
            book_id=book_id,
            title="Updated Title",
            pages=150,
            genre="Mystery",
            publication_year=2025,
            author_ids=[author_id]
        )
        
        # Act
        result = await handler.handle(command)
        
        # Assert
        assert result.title == "Updated Title"
        assert result.pages == 150
        
        mock_book_repo.get_by_id.assert_called_once_with(book_id)
        mock_author_repo.get_by_ids.assert_called_once_with([author_id])
        mock_book_repo.update.assert_called_once()
        mock_event_publisher.publish.assert_called_once()
    
    async def test_update_non_existing_book(self):
        """Test updating a book that doesn't exist"""
        # Arrange
        mock_book_repo = AsyncMock()
        mock_author_repo = AsyncMock()
        
        book_id = uuid4()
        author_id = uuid4()
        
        mock_book_repo.get_by_id.return_value = None  # Book not found
        
        handler = UpdateBookHandler(mock_book_repo, mock_author_repo)
        command = UpdateBookCommand(
            book_id=book_id,
            title="Updated Title",
            pages=150,
            genre="Mystery",
            publication_year=2025,
            author_ids=[author_id]
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            await handler.handle(command)
        
        mock_book_repo.update.assert_not_called()
    
    async def test_update_book_authors_not_found(self):
        """Test updating a book with non-existing authors"""
        # Arrange
        mock_book_repo = AsyncMock()
        mock_author_repo = AsyncMock()
        
        book_id = uuid4()
        author_id = uuid4()
        old_author = Author(id=uuid4(), name="Old Author")
        
        existing_book = Book(
            id=book_id,
            title="Old Title",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            authors=[old_author]  # Existing book has an author
        )
        
        mock_book_repo.get_by_id.return_value = existing_book
        mock_author_repo.get_by_ids.return_value = []  # No authors found for update
        
        handler = UpdateBookHandler(mock_book_repo, mock_author_repo)
        command = UpdateBookCommand(
            book_id=book_id,
            title="Updated Title",
            pages=150,
            genre="Mystery",
            publication_year=2025,
            author_ids=[author_id]
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Some authors do not exist"):
            await handler.handle(command)
        
        mock_book_repo.update.assert_not_called()