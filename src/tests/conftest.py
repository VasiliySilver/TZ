"""
Pytest configuration and shared fixtures.
"""
import asyncio
from typing import AsyncGenerator, Generator
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.infrastructure.database.models import Base
from src.infrastructure.database.models import BookModel, AuthorModel
from src.domain.entities.book import Book
from src.domain.entities.author import Author


# Test database URL - use PostgreSQL for consistency
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session


@pytest.fixture
def sample_author() -> Author:
    """Create a sample author entity."""
    return Author(
        id=uuid4(),
        name="Test Author"
    )


@pytest.fixture
def sample_book(sample_author: Author) -> Book:
    """Create a sample book entity."""
    return Book(
        id=uuid4(),
        title="Test Book",
        pages=100,
        genre="Fiction",
        publication_year=2024,
        authors=[sample_author]
    )


@pytest_asyncio.fixture
async def sample_author_model(test_session: AsyncSession) -> AuthorModel:
    """Create a sample author in the database."""
    author = AuthorModel(name="Test Author")
    test_session.add(author)
    await test_session.commit()
    await test_session.refresh(author)
    return author


@pytest_asyncio.fixture
async def sample_book_model(
    test_session: AsyncSession,
    sample_author_model: AuthorModel
) -> BookModel:
    """Create a sample book in the database."""
    book = BookModel(
        title="Test Book",
        pages=100,
        genre="Fiction",
        publication_year=2024,
        authors=[sample_author_model]
    )
    test_session.add(book)
    await test_session.commit()
    await test_session.refresh(book)
    return book