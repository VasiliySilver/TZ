"""
Unit tests for CreateBookHandler with mocks
"""
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.commands.create_book import CreateBookCommand, CreateBookHandler
from src.domain.entities.book import Book
from src.domain.entities.author import Author


@pytest.mark.asyncio
class TestCreateBookHandler:
    """Test cases for CreateBookHandler"""
    
    async def test_create_book_success(self):
        """Test successful book creation"""
        # Arrange
        mock_book_repo = AsyncMock()
        mock_author_repo = AsyncMock()
        mock_event_publisher = AsyncMock()
        
        author_id = uuid4()
        author = Author(id=author_id, name="Test Author")
        
        # Mock author repository to return existing authors
        mock_author_repo.get_by_ids.return_value = [author]
        
        # Mock book repository to return created book
        created_book = Book(
            id=uuid4(),
            title="Test Book",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            authors=[author]
        )
        mock_book_repo.add.return_value = created_book
        
        handler = CreateBookHandler(mock_book_repo, mock_author_repo, mock_event_publisher)
        command = CreateBookCommand(
            title="Test Book",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            author_ids=[author_id]
        )
        
        # Act
        result = await handler.handle(command)
        
        # Assert
        assert result.title == "Test Book"
        assert result.pages == 100
        assert len(result.authors) == 1
        
        # Verify mock calls
        mock_author_repo.get_by_ids.assert_called_once_with([author_id])
        mock_book_repo.add.assert_called_once()
        mock_event_publisher.publish.assert_called_once()
        
        # Check event data
        call_args = mock_event_publisher.publish.call_args
        assert call_args[1]['routing_key'] == "book.created"
        assert "book_id" in call_args[1]['event_data']
        assert call_args[1]['event_data']['title'] == "Test Book"
    
    async def test_create_book_authors_not_found(self):
        """Test book creation when some authors don't exist"""
        # Arrange
        mock_book_repo = AsyncMock()
        mock_author_repo = AsyncMock()
        
        author_id = uuid4()
        
        # Mock author repository to return fewer authors than requested
        mock_author_repo.get_by_ids.return_value = []  # No authors found
        
        handler = CreateBookHandler(mock_book_repo, mock_author_repo)
        command = CreateBookCommand(
            title="Test Book",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            author_ids=[author_id]
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Some authors do not exist"):
            await handler.handle(command)
        
        # Verify book was not added
        mock_book_repo.add.assert_not_called()
    
    async def test_create_book_without_event_publisher(self):
        """Test book creation without event publisher (no events)"""
        # Arrange
        mock_book_repo = AsyncMock()
        mock_author_repo = AsyncMock()
        
        author_id = uuid4()
        author = Author(id=author_id, name="Test Author")
        
        mock_author_repo.get_by_ids.return_value = [author]
        created_book = Book(
            id=uuid4(),
            title="Test Book",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            authors=[author]
        )
        mock_book_repo.add.return_value = created_book
        
        # No event publisher
        handler = CreateBookHandler(mock_book_repo, mock_author_repo, event_publisher=None)
        command = CreateBookCommand(
            title="Test Book",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            author_ids=[author_id]
        )
        
        # Act
        result = await handler.handle(command)
        
        # Assert
        assert result.title == "Test Book"
        mock_book_repo.add.assert_called_once()