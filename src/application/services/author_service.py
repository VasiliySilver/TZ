from typing import List

from src.domain.entities.author import Author
from src.application.queries.get_all_authors import GetAllAuthorsQuery, GetAllAuthorsHandler
from src.infrastructure.database.unit_of_work import UnitOfWork


class AuthorService:
    """
    Application service for managing authors.
    """
    
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
        self._get_all_handler = GetAllAuthorsHandler(uow.authors)
    
    async def get_all_authors(self) -> List[Author]:
        """
        Get all authors.
        
        Returns:
            List of Author entities
        """
        query = GetAllAuthorsQuery()
        return await self._get_all_handler.handle(query)