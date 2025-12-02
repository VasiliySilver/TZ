"""
Script to seed initial data (authors) into the database.
Run: poetry run python scripts/seed_data.py
"""
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.database.session import get_async_session
from src.infrastructure.database.models import AuthorModel


async def seed_authors():
    """Add initial authors to the database"""
    authors_data = [
        {"name": "F. Scott Fitzgerald"},
        {"name": "George Orwell"},
        {"name": "Jane Austen"},
        {"name": "Mark Twain"},
        {"name": "Ernest Hemingway"},
    ]
    
    async with get_async_session() as session:
        for author_data in authors_data:
            # Check if author already exists
            author = AuthorModel(**author_data)
            session.add(author)
        
        print(f"✅ Added {len(authors_data)} authors to the database")


if __name__ == "__main__":
    asyncio.run(seed_authors())