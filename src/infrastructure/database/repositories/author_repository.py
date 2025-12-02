from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.author import Author
from src.domain.repositories.author_repository import IAuthorRepository
from src.infrastructure.database.models import AuthorModel
from src.infrastructure.database.mappers import AuthorMapper


class AuthorRepository(IAuthorRepository):
    """SQLAlchemy implementation of IAuthorRepository"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def add(self, author: Author) -> Author:
        """Add a new author"""
        author_model = AuthorMapper.to_model(author)
        self._session.add(author_model)
        await self._session.flush()
        await self._session.refresh(author_model)
        return AuthorMapper.to_entity(author_model)
    
    async def get_by_id(self, author_id: UUID) -> Optional[Author]:
        """Get author by ID"""
        result = await self._session.execute(
            select(AuthorModel).where(AuthorModel.id == author_id)
        )
        author_model = result.scalar_one_or_none()
        
        if author_model is None:
            return None
        
        return AuthorMapper.to_entity(author_model)
    
    async def get_by_ids(self, author_ids: List[UUID]) -> List[Author]:
        """Get multiple authors by IDs"""
        result = await self._session.execute(
            select(AuthorModel).where(AuthorModel.id.in_(author_ids))
        )
        author_models = result.scalars().all()
        return AuthorMapper.to_entities(list(author_models))
    
    async def get_all(self) -> List[Author]:
        """Get all authors"""
        result = await self._session.execute(select(AuthorModel))
        author_models = result.scalars().all()
        return AuthorMapper.to_entities(list(author_models))