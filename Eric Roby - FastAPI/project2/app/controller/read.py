from typing import Optional, Union
from fastapi import APIRouter, HTTPException, Path, Query, Response, status
from ..models.book import BOOKS, Book

router = APIRouter()

@router.get("")
async def read_all_books(skip_book: str | None = None):
    newBooks = BOOKS.copy()
    if skip_book is not None:
        del newBooks[int(skip_book)]
    return newBooks


@router.get("/rating")
async def read_books_by_rating(rate: int = Query(ge=1, le=5)):
    books_rated = []
    for book in BOOKS:
        if book.rating == rate:
            books_rated.append(book)
    return books_rated


@router.get("/{id}", response_model=None, status_code=status.HTTP_200_OK)
async def read_one_book(id: int = Path(gt=0)) -> Optional[Book]:
    for book in BOOKS:
        if book.id == id:
            return book
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {id} not found",
    )
