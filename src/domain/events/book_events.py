from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import List


@dataclass
class DomainEvent:
    """Base domain event"""
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BookCreatedEvent:
    """Event raised when a book is created"""
    book_id: UUID
    title: str
    author_ids: List[UUID]
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BookUpdatedEvent:
    """Event raised when a book is updated"""
    book_id: UUID
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BookDeletedEvent:
    """Event raised when a book is deleted"""
    book_id: UUID
    occurred_at: datetime = field(default_factory=datetime.utcnow)