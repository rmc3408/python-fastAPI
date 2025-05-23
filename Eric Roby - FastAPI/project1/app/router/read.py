from fastapi import APIRouter
from enum import Enum
from ..utils.mock import BOOKS

router = APIRouter()

@router.get("/")
async def read_all_books(skip_book: str | None = None):
    newBooks = BOOKS.copy()
    if skip_book is not None:
        del newBooks[int(skip_book)]
    return newBooks


@router.get("/{id}")
async def read_one_book(id: str, category: str | None = None):
    filtered = None
    if category is not None:
        filtered = filter(lambda x: x['id'] == id or x['category'] == category, BOOKS)
    else:
        filtered = filter(lambda x: x['id'] == id, BOOKS)

    result = list(filtered)
    return {"item": result}


class Direction(Enum):
    N = "North"
    S = "South"
    E = "East"
    W = "West"

@router.get('/direction/{code}')
async def get_direction(code: Direction):
    if code == Direction.E:
        return 'Go to East'
    elif code == Direction.W:
        return 'Go to West'
    elif code == Direction.N:
        return 'Go to North'
    elif code == Direction.S:
        return 'Go to South'

