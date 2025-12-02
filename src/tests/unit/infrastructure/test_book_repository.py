"""
Unit tests for BookRepository
"""
from uuid import uuid4

import pytest

from src.domain.entities.book import Book
from src.domain.entities.author import Author
from src.infrastructure.database.repositories.book_repository import BookRepository
from src.infrastructure.database.models import BookModel, AuthorModel


@pytest.mark.asyncio
class TestBookRepository:
    """Test cases for BookRepository"""
    
    async def test_add_book(self, test_session, sample_author_model):
        """Test adding a new book"""
        # Arrange
        repo = BookRepository(test_session)
        author = Author(id=sample_author_model.id, name=sample_author_model.name)
        book = Book(
            id=uuid4(),
            title="New Book",
            pages=200,
            genre="Science Fiction",
            publication_year=2024,
            authors=[author]
        )
        
        # Act
        created_book = await repo.add(book)
        
        # Assert
        assert created_book.id == book.id
        assert created_book.title == "New Book"
        assert created_book.pages == 200
        assert len(created_book.authors) == 1
        assert created_book.authors[0].id == sample_author_model.id
    
    async def test_get_by_id_existing(self, test_session, sample_book_model):
        """Test getting an existing book by ID"""
        # Arrange
        repo = BookRepository(test_session)
        
        # Act
        book = await repo.get_by_id(sample_book_model.id)
        
        # Assert
        assert book is not None
        assert book.id == sample_book_model.id
        assert book.title == sample_book_model.title
        assert len(book.authors) > 0
    
    async def test_get_by_id_non_existing(self, test_session):
        """Test getting a non-existing book by ID"""
        # Arrange
        repo = BookRepository(test_session)
        non_existing_id = uuid4()
        
        # Act
        book = await repo.get_by_id(non_existing_id)
        
        # Assert
        assert book is None
    
    async def test_get_all(self, test_session, sample_book_model):
        """Test getting all books"""
        # Arrange
        repo = BookRepository(test_session)
        
        # Act
        books = await repo.get_all()
        
        # Assert
        assert len(books) >= 1
        assert any(book.id == sample_book_model.id for book in books)
    
    async def test_get_all_empty(self, test_session):
        """Test getting all books when database is empty"""
        # Arrange
        repo = BookRepository(test_session)
        
        # Act
        books = await repo.get_all()
        
        # Assert
        assert len(books) == 0
    
    async def test_update_book(self, test_session, sample_book_model, sample_author_model):
        """Test updating an existing book"""
        # Arrange
        repo = BookRepository(test_session)
        author = Author(id=sample_author_model.id, name=sample_author_model.name)
        updated_book = Book(
            id=sample_book_model.id,
            title="Updated Title",
            pages=150,
            genre="Mystery",
            publication_year=2025,
            authors=[author]
        )
        
        # Act
        result = await repo.update(updated_book)
        
        # Assert
        assert result.id == sample_book_model.id
        assert result.title == "Updated Title"
        assert result.pages == 150
        assert result.genre == "Mystery"
    
    async def test_update_non_existing_book(self, test_session, sample_author_model):
        """Test updating a non-existing book raises error"""
        # Arrange
        repo = BookRepository(test_session)
        author = Author(id=sample_author_model.id, name=sample_author_model.name)
        non_existing_book = Book(
            id=uuid4(),
            title="Non-existing Book",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            authors=[author]
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            await repo.update(non_existing_book)
    
    async def test_delete_book(self, test_session, sample_book_model):
        """Test deleting a book"""
        # Arrange
        repo = BookRepository(test_session)
        book_id = sample_book_model.id
        
        # Act
        await repo.delete(book_id)
        
        # Assert
        deleted_book = await repo.get_by_id(book_id)
        assert deleted_book is None
    
    async def test_delete_non_existing_book(self, test_session):
        """Test deleting a non-existing book raises error"""
        # Arrange
        repo = BookRepository(test_session)
        non_existing_id = uuid4()
        
        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            await repo.delete(non_existing_id)
    
    async def test_add_book_with_non_existing_authors(self, test_session):
        """Test adding a book with non-existing authors raises error"""
        # Arrange
        repo = BookRepository(test_session)
        fake_author = Author(id=uuid4(), name="Fake Author")
        book = Book(
            id=uuid4(),
            title="Book with Fake Author",
            pages=100,
            genre="Fiction",
            publication_year=2024,
            authors=[fake_author]
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="do not exist"):
            await repo.add(book)