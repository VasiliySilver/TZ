"""
Integration tests for Authors API endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthorsAPI:
    """Integration tests for /api/v1/authors endpoints"""
    
    async def test_get_all_authors_empty(self, client: AsyncClient):
        """Test getting all authors when database is empty"""
        # Act
        response = await client.get("/api/v1/authors/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_get_all_authors(self, client: AsyncClient, sample_author_model):
        """Test getting all authors"""
        # Act
        response = await client.get("/api/v1/authors/")
        
        # Assert
        assert response.status_code == 200
        authors = response.json()
        assert len(authors) >= 1
        assert any(author["id"] == str(sample_author_model.id) for author in authors)
        assert any(author["name"] == sample_author_model.name for author in authors)