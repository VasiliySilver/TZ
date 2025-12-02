from dataclasses import dataclass
from uuid import UUID


@dataclass
class Author:
    """Domain entity representing an author"""
    id: UUID
    name: str
    
    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Author name cannot be empty")