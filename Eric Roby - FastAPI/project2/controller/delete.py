from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from ..models.book import BOOKS

router = APIRouter()

@router.delete('/{id}')
async def remove_book(id: str):
  for i, book in enumerate(BOOKS):
    if book.id == int(id):
      del BOOKS[i]
      return { 'message': f'deleted book ID {id}', 'item_deleted': book }
  
  return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"message": f"Book with id {id} not found."},
  )
