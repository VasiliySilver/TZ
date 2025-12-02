from typing import List
from fastapi import APIRouter, Depends

from src.application.services.author_service import AuthorService
from src.presentation.dependencies import get_author_service
from src.presentation.schemas.author import AuthorResponse


router = APIRouter(prefix="/authors", tags=["authors"])


@router.get(
    "/",
    response_model=List[AuthorResponse],
    summary="Get all authors",
    description="Retrieve a list of all authors"
)
async def get_all_authors(
    service: AuthorService = Depends(get_author_service)
) -> List[AuthorResponse]:
    """Get all authors"""
    authors = await service.get_all_authors()
    
    return [
        AuthorResponse(id=author.id, name=author.name)
        for author in authors
    ]