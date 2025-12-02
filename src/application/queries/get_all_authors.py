from dataclasses import dataclass
from typing import List

from src.domain.entities.author import Author
from src.domain.repositories.author_repository import IAuthorRepository


@dataclass
class GetAllAuthorsQuery:
    """Query to get all authors"""
    pass


class GetAllAuthorsHandler:
    """Handler for GetAllAuthorsQuery"""
    
    def __init__(self, author_repository: IAuthorRepository):
        self._author_repo = author_repository
    
    async def handle(self, query: GetAllAuthorsQuery) -> List[Author]:
        """
        Handle the get all authors query.
        
        Args:
            query: GetAllAuthorsQuery
            
        Returns:
            List of Author entities
        """
        return await self._author_repo.get_all()