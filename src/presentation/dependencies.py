from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.session import get_session
from src.infrastructure.database.unit_of_work import UnitOfWork
from src.application.services.book_service import BookService
from src.application.services.author_service import AuthorService


async def get_uow(
    session: AsyncSession = Depends(get_session)
) -> AsyncGenerator[UnitOfWork, None]:
    """
    Dependency to get Unit of Work.
    
    Usage:
        @router.post("/books")
        async def create_book(uow: UnitOfWork = Depends(get_uow)):
            ...
    """
    uow = UnitOfWork(session)
    try:
        yield uow
    finally:
        await uow.close()


async def get_book_service(
    uow: UnitOfWork = Depends(get_uow)
) -> BookService:
    """
    Dependency to get BookService.
    
    Usage:
        @router.post("/books")
        async def create_book(service: BookService = Depends(get_book_service)):
            ...
    """
    return BookService(uow)


async def get_author_service(
    uow: UnitOfWork = Depends(get_uow)
) -> AuthorService:
    """
    Dependency to get AuthorService.
    
    Usage:
        @router.get("/authors")
        async def get_authors(service: AuthorService = Depends(get_author_service)):
            ...
    """
    return AuthorService(uow)