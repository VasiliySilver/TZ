from uuid import UUID
from typing import List
from pydantic import BaseModel, Field


class BookCreateRequest(BaseModel):
    """Request schema for creating a book"""
    title: str = Field(..., min_length=1, max_length=250, description="Book title")
    pages: int = Field(..., gt=0, description="Number of pages")
    genre: str = Field(..., min_length=1, max_length=100, description="Book genre")
    publication_year: int = Field(..., ge=1000, le=9999, description="Year of publication")
    authors: List[UUID] = Field(..., min_length=1, description="List of author UUIDs")


class BookUpdateRequest(BaseModel):
    """Request schema for updating a book"""
    title: str = Field(..., min_length=1, max_length=250, description="Book title")
    pages: int = Field(..., gt=0, description="Number of pages")
    genre: str = Field(..., min_length=1, max_length=100, description="Book genre")
    publication_year: int = Field(..., ge=1000, le=9999, description="Year of publication")
    authors: List[UUID] = Field(..., min_length=1, description="List of author UUIDs")


class BookResponse(BaseModel):
    """Response schema for a book"""
    id: UUID
    title: str
    pages: int
    genre: str
    publication_year: int
    authors: List[UUID]
    
    model_config = {"from_attributes": True}