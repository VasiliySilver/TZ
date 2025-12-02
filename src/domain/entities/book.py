from dataclasses import dataclass, field
from uuid import UUID
from typing import List

from src.domain.entities.author import Author


@dataclass
class Book:
    """Domain entity representing a book"""
    id: UUID
    title: str
    pages: int
    genre: str
    publication_year: int
    authors: List[Author] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate book data"""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        
        if self.pages <= 0:
            raise ValueError("Pages must be positive")
        
        if not self.authors:
            raise ValueError("Book must have at least one author")
    
    def add_author(self, author: Author) -> None:
        """Add an author to the book"""
        if author not in self.authors:
            self.authors.append(author)
    
    def remove_author(self, author: Author) -> None:
        """Remove an author from the book"""
        if len(self.authors) <= 1:
            raise ValueError("Book must have at least one author")
        
        if author in self.authors:
            self.authors.remove(author)