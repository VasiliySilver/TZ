from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.session import get_session
from src.infrastructure.database.unit_of_work import UnitOfWork
from src.application.services.book_service import BookService
from src.application.services.author_service import AuthorService
from src.infrastructure.messaging.publisher import get_event_publisher, EventPublisher


async def get_uow(
    session: AsyncSession = Depends(get_session)
) -> AsyncGenerator[UnitOfWork, None]:
    """Dependency to get Unit of Work"""
    uow = UnitOfWork(session)
    try:
        yield uow
    finally:
        await uow.close()


async def get_book_service(
    uow: UnitOfWork = Depends(get_uow),
    event_publisher: EventPublisher = Depends(get_event_publisher)
) -> BookService:
    """Dependency to get BookService with event publisher"""
    return BookService(uow, event_publisher)


async def get_author_service(
    uow: UnitOfWork = Depends(get_uow)
) -> AuthorService:
    """Dependency to get AuthorService"""
    return AuthorService(uow)