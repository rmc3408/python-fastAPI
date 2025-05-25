from typing import Optional
from app.models.book import BOOKS, BookUpdateRequest, Book, BookUpdateResponse
from fastapi import APIRouter

router = APIRouter()

@router.put('/{id}', response_model=BookUpdateResponse, tags=['books/update'])
async def update_book(id: str, update_book: BookUpdateRequest):
  num_book = -1
  found_book: Optional[Book] = None
  for i in range(len(BOOKS)):
    if BOOKS[i].id == int(id):
      num_book = i
      found_book = BOOKS[i]

  if num_book is not -1 and found_book is not None:
    for key in found_book.__dict__.keys():
      if key == 'id':
        continue
      value = getattr(update_book, key)
      if value is not None:
        setattr(found_book, key, value)
    BOOKS[num_book] = found_book

  return found_book
