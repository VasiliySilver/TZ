from dataclasses import dataclass
from uuid import UUID
from typing import Optional

from src.domain.entities.book import Book
from src.domain.repositories.book_repository import IBookRepository


@dataclass
class GetBookByIdQuery:
    """Query to get a book by ID"""
    book_id: UUID


class GetBookByIdHandler:
    """Handler for GetBookByIdQuery"""
    
    def __init__(self, book_repository: IBookRepository):
        self._book_repo = book_repository
    
    async def handle(self, query: GetBookByIdQuery) -> Optional[Book]:
        """
        Handle the get book by id query.
        
        Args:
            query: GetBookByIdQuery with book_id
            
        Returns:
            Book entity or None if not found
        """
        return await self._book_repo.get_by_id(query.book_id)