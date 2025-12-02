from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.database.config import db_config


# Create async engine
engine: AsyncEngine = create_async_engine(
    db_config.url,
    echo=True,  # Log SQL queries (set to False in production)
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
)

# Create session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session.
    
    Usage:
        async with get_async_session() as session:
            # use session
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI to inject database session.
    
    Usage in FastAPI:
        @router.get("/books")
        async def get_books(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with get_async_session() as session:
        yield session