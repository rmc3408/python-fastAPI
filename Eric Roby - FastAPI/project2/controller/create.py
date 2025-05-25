from fastapi import APIRouter, status
from ..models.book import BOOKS, Book, BookRequest, BookResponse
from ..errors.book import BookException

router = APIRouter()


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(bodyitem: BookRequest):  # using Pydantic model for validation
    payload = bodyitem.model_dump()
    
    if payload['title'] == "yolo":
        raise BookException(detail="You cannot create a book with the name 'yolo'")
    payload['id'] = makeNewId()
    convertedBook = Book(**payload)
    BOOKS.append(convertedBook)
    return convertedBook

def makeNewId():
    return 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
