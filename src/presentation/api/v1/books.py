from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.services.book_service import BookService
from src.presentation.dependencies import get_book_service
from src.presentation.schemas.book import BookCreateRequest, BookUpdateRequest, BookResponse


router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Create a new book with the provided information"
)
async def create_book(
    book_data: BookCreateRequest,
    service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Create a new book"""
    try:
        book = await service.create_book(
            title=book_data.title,
            pages=book_data.pages,
            genre=book_data.genre,
            publication_year=book_data.publication_year,
            author_ids=book_data.authors
        )
        
        return BookResponse(
            id=book.id,
            title=book.title,
            pages=book.pages,
            genre=book.genre,
            publication_year=book.publication_year,
            authors=[author.id for author in book.authors]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/",
    response_model=List[BookResponse],
    summary="Get all books",
    description="Retrieve a list of all books"
)
async def get_all_books(
    service: BookService = Depends(get_book_service)
) -> List[BookResponse]:
    """Get all books"""
    books = await service.get_all_books()
    
    return [
        BookResponse(
            id=book.id,
            title=book.title,
            pages=book.pages,
            genre=book.genre,
            publication_year=book.publication_year,
            authors=[author.id for author in book.authors]
        )
        for book in books
    ]


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get a book by ID",
    description="Retrieve a specific book by its ID"
)
async def get_book_by_id(
    book_id: UUID,
    service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Get a book by ID"""
    book = await service.get_book_by_id(book_id)
    
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    return BookResponse(
        id=book.id,
        title=book.title,
        pages=book.pages,
        genre=book.genre,
        publication_year=book.publication_year,
        authors=[author.id for author in book.authors]
    )


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update a book",
    description="Update an existing book with new information"
)
async def update_book(
    book_id: UUID,
    book_data: BookUpdateRequest,
    service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Update a book"""
    try:
        book = await service.update_book(
            book_id=book_id,
            title=book_data.title,
            pages=book_data.pages,
            genre=book_data.genre,
            publication_year=book_data.publication_year,
            author_ids=book_data.authors
        )
        
        return BookResponse(
            id=book.id,
            title=book.title,
            pages=book.pages,
            genre=book.genre,
            publication_year=book.publication_year,
            authors=[author.id for author in book.authors]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    description="Delete a book by its ID"
)
async def delete_book(
    book_id: UUID,
    service: BookService = Depends(get_book_service)
) -> None:
    """Delete a book"""
    try:
        await service.delete_book(book_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))