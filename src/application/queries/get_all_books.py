from dataclasses import dataclass
from typing import List

from src.domain.entities.book import Book
from src.domain.repositories.book_repository import IBookRepository


@dataclass
class GetAllBooksQuery:
    """Query to get all books"""
    pass


class GetAllBooksHandler:
    """Handler for GetAllBooksQuery"""
    
    def __init__(self, book_repository: IBookRepository):
        self._book_repo = book_repository
    
    async def handle(self, query: GetAllBooksQuery) -> List[Book]:
        """
        Handle the get all books query.
        
        Args:
            query: GetAllBooksQuery
            
        Returns:
            List of Book entities
        """
        return await self._book_repo.get_all()