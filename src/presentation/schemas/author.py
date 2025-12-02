from uuid import UUID
from pydantic import BaseModel


class AuthorResponse(BaseModel):
    """Response schema for an author"""
    id: UUID
    name: str
    
    model_config = {"from_attributes": True}