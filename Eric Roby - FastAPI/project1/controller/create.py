from fastapi import APIRouter, Body
from ..utils.mock import BOOKS
import uuid
from pydantic import BaseModel

router = APIRouter()

class Book(BaseModel):
    title: str | None
    author: str | None
    category: str

# @router.post('/')
# async def create_book(item: Book):
#     newBook = { 
#         'id': uuid.uuid4(), 
#         'title': item.title, 
#         'author': item.author, 
#         'category': item.category
#     }
#     return {'msg': 'ok'}

@router.post("")
async def create_book(item: Book = Body()):
    newBook = item.dict()
    newBook['id'] = str(uuid.uuid4())
    BOOKS.append(newBook)
    return {'item': newBook }