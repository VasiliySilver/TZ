"""
Integration tests for Books API endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestBooksAPI:
    """Integration tests for /api/v1/books endpoints"""
    
    async def test_create_book_success(self, client: AsyncClient, sample_author_model):
        """Test creating a book through API"""
        # Arrange
        book_data = {
            "title": "1984",
            "pages": 328,
            "genre": "Dystopian",
            "publication_year": 1949,
            "authors": [str(sample_author_model.id)]
        }
        
        # Act
        response = await client.post("/api/v1/books/", json=book_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "1984"
        assert data["pages"] == 328
        assert data["genre"] == "Dystopian"
        assert data["publication_year"] == 1949
        assert len(data["authors"]) == 1
        assert "id" in data
    
    async def test_create_book_invalid_author(self, client: AsyncClient):
        """Test creating a book with non-existing author"""
        # Arrange
        book_data = {
            "title": "Test Book",
            "pages": 100,
            "genre": "Fiction",
            "publication_year": 2024,
            "authors": ["00000000-0000-0000-0000-000000000000"]
        }
        
        # Act
        response = await client.post("/api/v1/books/", json=book_data)
        
        # Assert
        assert response.status_code == 400
        assert "authors do not exist" in response.json()["detail"].lower()
    
    async def test_create_book_validation_error(self, client: AsyncClient, sample_author_model):
        """Test creating a book with invalid data"""
        # Arrange
        book_data = {
            "title": "",  # Empty title
            "pages": -10,  # Negative pages
            "genre": "Fiction",
            "publication_year": 2024,
            "authors": [str(sample_author_model.id)]
        }
        
        # Act
        response = await client.post("/api/v1/books/", json=book_data)
        
        # Assert
        assert response.status_code == 422
    
    async def test_get_all_books_empty(self, client: AsyncClient):
        """Test getting all books when database is empty"""
        # Act
        response = await client.get("/api/v1/books/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_get_all_books(self, client: AsyncClient, sample_book_model):
        """Test getting all books"""
        # Act
        response = await client.get("/api/v1/books/")
        
        # Assert
        assert response.status_code == 200
        books = response.json()
        assert len(books) >= 1
        assert any(book["id"] == str(sample_book_model.id) for book in books)
    
    async def test_get_book_by_id_success(self, client: AsyncClient, sample_book_model):
        """Test getting a specific book by ID"""
        # Act
        response = await client.get(f"/api/v1/books/{sample_book_model.id}")
        
        # Assert
        assert response.status_code == 200
        book = response.json()
        assert book["id"] == str(sample_book_model.id)
        assert book["title"] == sample_book_model.title
    
    async def test_get_book_by_id_not_found(self, client: AsyncClient):
        """Test getting a non-existing book"""
        # Act
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/books/{fake_id}")
        
        # Assert
        assert response.status_code == 404
    
    async def test_update_book_success(self, client: AsyncClient, sample_book_model, sample_author_model):
        """Test updating a book"""
        # Arrange
        update_data = {
            "title": "Updated Title",
            "pages": 200,
            "genre": "Mystery",
            "publication_year": 2025,
            "authors": [str(sample_author_model.id)]
        }
        
        # Act
        response = await client.put(
            f"/api/v1/books/{sample_book_model.id}",
            json=update_data
        )
        
        # Assert
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "Updated Title"
        assert book["pages"] == 200
        assert book["genre"] == "Mystery"
    
    async def test_update_book_not_found(self, client: AsyncClient, sample_author_model):
        """Test updating a non-existing book"""
        # Arrange
        fake_id = "00000000-0000-0000-0000-000000000000"
        update_data = {
            "title": "Updated Title",
            "pages": 200,
            "genre": "Mystery",
            "publication_year": 2025,
            "authors": [str(sample_author_model.id)]
        }
        
        # Act
        response = await client.put(f"/api/v1/books/{fake_id}", json=update_data)
        
        # Assert
        assert response.status_code == 400
    
    async def test_delete_book_success(self, client: AsyncClient, sample_book_model):
        """Test deleting a book"""
        # Act
        response = await client.delete(f"/api/v1/books/{sample_book_model.id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verify book is deleted
        get_response = await client.get(f"/api/v1/books/{sample_book_model.id}")
        assert get_response.status_code == 404
    
    async def test_delete_book_not_found(self, client: AsyncClient):
        """Test deleting a non-existing book"""
        # Act
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.delete(f"/api/v1/books/{fake_id}")
        
        # Assert
        assert response.status_code == 404
    
    async def test_full_crud_flow(self, client: AsyncClient, sample_author_model):
        """Test complete CRUD flow: Create → Read → Update → Delete"""
        # Create
        create_data = {
            "title": "CRUD Test Book",
            "pages": 150,
            "genre": "Test",
            "publication_year": 2024,
            "authors": [str(sample_author_model.id)]
        }
        create_response = await client.post("/api/v1/books/", json=create_data)
        assert create_response.status_code == 201
        book_id = create_response.json()["id"]
        
        # Read
        read_response = await client.get(f"/api/v1/books/{book_id}")
        assert read_response.status_code == 200
        assert read_response.json()["title"] == "CRUD Test Book"
        
        # Update
        update_data = {
            "title": "CRUD Test Book Updated",
            "pages": 200,
            "genre": "Test",
            "publication_year": 2024,
            "authors": [str(sample_author_model.id)]
        }
        update_response = await client.put(f"/api/v1/books/{book_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "CRUD Test Book Updated"
        
        # Delete
        delete_response = await client.delete(f"/api/v1/books/{book_id}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        get_response = await client.get(f"/api/v1/books/{book_id}")
        assert get_response.status_code == 404