from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.book import Book
from src.domain.repositories.book_repository import IBookRepository
from src.infrastructure.database.models import BookModel, AuthorModel
from src.infrastructure.database.mappers import BookMapper


class BookRepository(IBookRepository):
    """SQLAlchemy implementation of IBookRepository"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def add(self, book: Book) -> Book:
        """Add a new book"""
        # Fetch author models from database
        author_ids = [author.id for author in book.authors]
        result = await self._session.execute(
            select(AuthorModel).where(AuthorModel.id.in_(author_ids))
        )
        author_models = list(result.scalars().all())
        
        if len(author_models) != len(author_ids):
            raise ValueError("Some authors do not exist in database")
        
        # Create book model with authors
        book_model = BookMapper.to_model(book, author_models)
        self._session.add(book_model)
        await self._session.flush()
        await self._session.refresh(book_model)
        
        return BookMapper.to_entity(book_model)
    
    async def get_by_id(self, book_id: UUID) -> Optional[Book]:
        """Get book by ID"""
        result = await self._session.execute(
            select(BookModel).where(BookModel.id == book_id)
        )
        book_model = result.scalar_one_or_none()
        
        if book_model is None:
            return None
        
        return BookMapper.to_entity(book_model)
    
    async def get_all(self) -> List[Book]:
        """Get all books"""
        result = await self._session.execute(select(BookModel))
        book_models = result.scalars().all()
        return BookMapper.to_entities(list(book_models))
    
    async def update(self, book: Book) -> Book:
        """Update existing book"""
        # Fetch existing book
        result = await self._session.execute(
            select(BookModel).where(BookModel.id == book.id)
        )
        book_model = result.scalar_one_or_none()
        
        if book_model is None:
            raise ValueError(f"Book with id {book.id} not found")
        
        # Update fields
        book_model.title = book.title
        book_model.pages = book.pages
        book_model.genre = book.genre
        book_model.publication_year = book.publication_year
        
        # Update authors
        author_ids = [author.id for author in book.authors]
        result = await self._session.execute(
            select(AuthorModel).where(AuthorModel.id.in_(author_ids))
        )
        author_models = list(result.scalars().all())
        
        if len(author_models) != len(author_ids):
            raise ValueError("Some authors do not exist in database")
        
        book_model.authors = author_models
        
        await self._session.flush()
        await self._session.refresh(book_model)
        
        return BookMapper.to_entity(book_model)
    
    async def delete(self, book_id: UUID) -> None:
        """Delete book by ID"""
        result = await self._session.execute(
            select(BookModel).where(BookModel.id == book_id)
        )
        book_model = result.scalar_one_or_none()
        
        if book_model is None:
            raise ValueError(f"Book with id {book_id} not found")
        
        await self._session.delete(book_model)
        await self._session.flush()