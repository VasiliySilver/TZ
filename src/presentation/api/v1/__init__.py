from fastapi import APIRouter

from src.presentation.api.v1 import books, authors


router = APIRouter(prefix="/v1")
router.include_router(books.router)
router.include_router(authors.router)