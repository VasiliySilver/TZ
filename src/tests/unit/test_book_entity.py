from uuid import UUID, uuid4
import pytest
from src.domain.entities.book import Book
from src.domain.entities.author import Author


class TestBookEntity:
    def test_create_book_with_valid_data(self):
        """Тест создания книги с валидными данными"""
        book_id = uuid4()
        author_id = uuid4()
        author = Author(id=author_id, name="F. Scott Fitzgerald")
        
        book = Book(
            id=book_id,
            title="The Great Gatsby",
            pages=180,
            genre="Novel",
            publication_year=1925,
            authors=[author]
        )
        
        assert book.id == book_id
        assert book.title == "The Great Gatsby"
        assert book.pages == 180
        assert book.genre == "Novel"
        assert book.publication_year == 1925
        assert len(book.authors) == 1
        assert book.authors[0].name == "F. Scott Fitzgerald"
    
    def test_book_requires_title(self):
        """Книга должна иметь название"""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Book(
                id=uuid4(),
                title="",
                pages=180,
                genre="Novel",
                publication_year=1925,
                authors=[]
            )
    
    def test_book_requires_positive_pages(self):
        """Количество страниц должно быть положительным"""
        with pytest.raises(ValueError, match="Pages must be positive"):
            Book(
                id=uuid4(),
                title="Test Book",
                pages=-10,
                genre="Novel",
                publication_year=1925,
                authors=[]
            )
    
    def test_book_requires_at_least_one_author(self):
        """Книга должна иметь хотя бы одного автора"""
        with pytest.raises(ValueError, match="Book must have at least one author"):
            Book(
                id=uuid4(),
                title="Test Book",
                pages=100,
                genre="Novel",
                publication_year=1925,
                authors=[]
            )
    
    def test_add_author_to_book(self):
        """Тест добавления автора к книге"""
        author1 = Author(id=uuid4(), name="Author 1")
        book = Book(
            id=uuid4(),
            title="Test Book",
            pages=100,
            genre="Novel",
            publication_year=1925,
            authors=[author1]
        )
        
        author2 = Author(id=uuid4(), name="Author 2")
        book.add_author(author2)
        
        assert len(book.authors) == 2
        assert author2 in book.authors