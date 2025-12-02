from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.author import Author


class IAuthorRepository(ABC):
    """Interface for Author repository"""
    
    @abstractmethod
    async def add(self, author: Author) -> Author:
        """Add a new author"""
        pass
    
    @abstractmethod
    async def get_by_id(self, author_id: UUID) -> Optional[Author]:
        """Get author by ID"""
        pass
    
    @abstractmethod
    async def get_by_ids(self, author_ids: List[UUID]) -> List[Author]:
        """Get multiple authors by IDs"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Author]:
        """Get all authors"""
        pass