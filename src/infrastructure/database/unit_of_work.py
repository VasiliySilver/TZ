from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.repositories import BookRepository, AuthorRepository


class UnitOfWork:
    """
    Unit of Work pattern implementation.
    Manages database session and provides access to repositories.
    Ensures all operations within a context are part of the same transaction.
    """
    
    def __init__(self, session: AsyncSession):
        self._session = session
        self.books = BookRepository(session)
        self.authors = AuthorRepository(session)
    
    async def commit(self) -> None:
        """Commit the current transaction"""
        await self._session.commit()
    
    async def rollback(self) -> None:
        """Rollback the current transaction"""
        await self._session.rollback()
    
    async def close(self) -> None:
        """Close the session"""
        await self._session.close()