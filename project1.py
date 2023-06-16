from typing import Union
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    { 'id': 1, 'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    { 'id': 2, 'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    { 'id': 3, 'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    { 'id': 4, 'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    { 'id': 5, 'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    { 'id': 6, 'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

class Direction(Enum):
    N = "North"
    S = "South"
    E = "East"
    W = "West"



@app.get("/")
async def read_all_books():
    return BOOKS


@app.get("/books/{id}")
async def read_one_book(id: int):
    filtered = filter(lambda x: x['id'] == id, BOOKS)
    result = list(filtered)[0]
    return {"item_id": result['id'], "item_title": result['title']}


@app.get('/direction/{code}')
async def get_direction(code: Direction):
    if code == Direction.E:
        return 'Go to East'
    elif code == Direction.W:
        return 'Go to West'
    elif code == Direction.N:
        return 'Go to North'
    elif code == Direction.S:
        return 'Go to South'
