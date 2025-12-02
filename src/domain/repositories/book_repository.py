from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.book import Book


class IBookRepository(ABC):
    """Interface for Book repository"""
    
    @abstractmethod
    async def add(self, book: Book) -> Book:
        """Add a new book"""
        pass
    
    @abstractmethod
    async def get_by_id(self, book_id: UUID) -> Optional[Book]:
        """Get book by ID"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Book]:
        """Get all books"""
        pass
    
    @abstractmethod
    async def update(self, book: Book) -> Book:
        """Update existing book"""
        pass
    
    @abstractmethod
    async def delete(self, book_id: UUID) -> None:
        """Delete book by ID"""
        pass