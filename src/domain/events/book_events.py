from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID
from typing import List


@dataclass
class DomainEvent:
    """Base domain event"""
    occurred_at: datetime
    def __post_init__(self):
        if not hasattr(self, 'occurred_at') or self.occurred_at is None:
            self.occurred_at = datetime.now(timezone.utc)


@dataclass
class BookCreatedEvent(DomainEvent):
    """Event raised when a book is created"""
    book_id: UUID
    title: str
    author_ids: List[UUID]
    occurred_at: datetime = None


@dataclass
class BookUpdatedEvent(DomainEvent):
    """Event raised when a book is updated"""
    book_id: UUID
    occurred_at: datetime = None


@dataclass
class BookDeletedEvent(DomainEvent):
    """Event raised when a book is deleted"""
    book_id: UUID
    occurred_at: datetime = None