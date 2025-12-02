from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.database.models.base import Base


# Association table for many-to-many relationship
book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("books.id"), primary_key=True),
    Column("author_id", UUID(as_uuid=True), ForeignKey("authors.id"), primary_key=True),
)