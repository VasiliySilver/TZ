"""
Unit tests for AuthorRepository
"""
from uuid import uuid4

import pytest

from src.domain.entities.author import Author
from src.infrastructure.database.repositories.author_repository import AuthorRepository


@pytest.mark.asyncio
class TestAuthorRepository:
    """Test cases for AuthorRepository"""
    
    async def test_add_author(self, test_session):
        """Test adding a new author"""
        # Arrange
        repo = AuthorRepository(test_session)
        author = Author(id=uuid4(), name="New Author")
        
        # Act
        created_author = await repo.add(author)
        
        # Assert
        assert created_author.id == author.id
        assert created_author.name == "New Author"
    
    async def test_get_by_id_existing(self, test_session, sample_author_model):
        """Test getting an existing author by ID"""
        # Arrange
        repo = AuthorRepository(test_session)
        
        # Act
        author = await repo.get_by_id(sample_author_model.id)
        
        # Assert
        assert author is not None
        assert author.id == sample_author_model.id
        assert author.name == sample_author_model.name
    
    async def test_get_by_id_non_existing(self, test_session):
        """Test getting a non-existing author by ID"""
        # Arrange
        repo = AuthorRepository(test_session)
        non_existing_id = uuid4()
        
        # Act
        author = await repo.get_by_id(non_existing_id)
        
        # Assert
        assert author is None
    
    async def test_get_by_ids(self, test_session, sample_author_model):
        """Test getting multiple authors by IDs"""
        # Arrange
        repo = AuthorRepository(test_session)
        author2 = Author(id=uuid4(), name="Second Author")
        await repo.add(author2)
        
        # Act
        authors = await repo.get_by_ids([sample_author_model.id, author2.id])
        
        # Assert
        assert len(authors) == 2
        author_ids = [a.id for a in authors]
        assert sample_author_model.id in author_ids
        assert author2.id in author_ids
    
    async def test_get_all(self, test_session, sample_author_model):
        """Test getting all authors"""
        # Arrange
        repo = AuthorRepository(test_session)
        
        # Act
        authors = await repo.get_all()
        
        # Assert
        assert len(authors) >= 1
        assert any(author.id == sample_author_model.id for author in authors)