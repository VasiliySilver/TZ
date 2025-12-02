from fastapi import APIRouter

from src.modules.books.controller import BookControllerDep
from src.modules.books.schemas import BookResponse, BookCreateRequest

router = APIRouter(prefix="/books")


@router.get("/")
async def get(controller: BookControllerDep) -> list[BookResponse]:
    return await controller.read_books()


@router.post("/")
async def post(controller: BookControllerDep, book_data: BookCreateRequest ) -> BookResponse:
    return await controller.create_book(book_data)
