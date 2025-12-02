from typing import List
from src.domain.entities.book import Book
from src.domain.entities.author import Author
from src.infrastructure.database.models import BookModel, AuthorModel


class AuthorMapper:
    """Mapper between Author entity and AuthorModel"""
    
    @staticmethod
    def to_entity(model: AuthorModel) -> Author:
        """Convert AuthorModel to Author entity"""
        return Author(
            id=model.id,
            name=model.name
        )
    
    @staticmethod
    def to_model(entity: Author) -> AuthorModel:
        """Convert Author entity to AuthorModel"""
        return AuthorModel(
            id=entity.id,
            name=entity.name
        )
    
    @staticmethod
    def to_entities(models: List[AuthorModel]) -> List[Author]:
        """Convert list of AuthorModel to list of Author entities"""
        return [AuthorMapper.to_entity(model) for model in models]


class BookMapper:
    """Mapper between Book entity and BookModel"""
    
    @staticmethod
    def to_entity(model: BookModel) -> Book:
        """Convert BookModel to Book entity"""
        authors = AuthorMapper.to_entities(model.authors)
        return Book(
            id=model.id,
            title=model.title,
            pages=model.pages,
            genre=model.genre,
            publication_year=model.publication_year,
            authors=authors
        )
    
    @staticmethod
    def to_model(entity: Book, author_models: List[AuthorModel]) -> BookModel:
        """
        Convert Book entity to BookModel.
        Note: author_models must be fetched from DB first
        """
        return BookModel(
            id=entity.id,
            title=entity.title,
            pages=entity.pages,
            genre=entity.genre,
            publication_year=entity.publication_year,
            authors=author_models
        )
    
    @staticmethod
    def to_entities(models: List[BookModel]) -> List[Book]:
        """Convert list of BookModel to list of Book entities"""
        return [BookMapper.to_entity(model) for model in models]