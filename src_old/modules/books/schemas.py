from uuid import UUID
from typing import List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    authors: list[UUID]
    publication_year: int | None = None
    pages: int
    genre: str | None = None


class BookCreateRequest(BaseModel):
    title: str
    authors: List[UUID]
    publication_year: int
    pages: int
    genre: str

class BookResponse(BookBase):
    id: UUID
    title: str
    authors: List[UUID]
    publication_year: int
    pages: int
    genre: str

    model_config = {"from_attributes": True}
