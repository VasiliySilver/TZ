from sqlalchemy import Table, Column, ForeignKey
from src.infra.postgres.models.base import Base

book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)
