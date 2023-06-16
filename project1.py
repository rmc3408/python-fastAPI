from string import Template
from typing import Optional, Union
from enum import Enum
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    { 'id': '0', 'title': 'Title Zero', 'author': 'Author Zero', 'category': 'math'},
    { 'id': '1', 'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    { 'id': '2', 'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    { 'id': '3', 'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    { 'id': '4', 'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    { 'id': '5', 'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    { 'id': '6', 'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


class Book(BaseModel):
    title: str | None
    author: str | None
    category: str


class Direction(Enum):
    N = "North"
    S = "South"
    E = "East"
    W = "West"


def find(keyTarget, valueTarget, listObj):
    for index, obj in enumerate(listObj):
        if obj.get(keyTarget) == valueTarget:
            return [index, obj]
    return [ -1, {}]    

@app.post('/')
async def create_book(item: Book):
    # newBook = { 
    #     'id': uuid.uuid4(), 
    #     'title': item.title, 
    #     'author': item.author, 
    #     'category': item.category
    # }
    newBook = item.dict()
    newBook['id'] = uuid.uuid4()
    BOOKS.append(newBook)
    return {'msg': newBook }


@app.put('/{id}')
async def update_book(id: str, item: Book):
    
    [index, data] = find('id', id, BOOKS)

    modifiedData = item.dict()

    for key in modifiedData.keys():
        if modifiedData[key] == None:
            continue
        data.update({ key: modifiedData[key] })

    BOOKS[index] = data
    return { 'msg': data }


@app.get("/")
async def read_all_books(skip_book: str | None = None):
    newBooks = BOOKS.copy()
    if skip_book is not None:
        del newBooks[skip_book-1]
    return newBooks


@app.get("/books/{id}")
async def read_one_book(id: str):
    filtered = filter(lambda x: x['id'] == id, BOOKS)
    result = list(filtered)[0]
    return {"item_id": result['id'], "item_title": result['title']}


@app.delete('/{id}')
async def remove_book(id: str):
    [ index, data ] = find('id', id, BOOKS)
    if index != -1:
        del BOOKS[index]
        return { 'msg': f'deleted books index {index}' }
    else:
        return { 'msg': 'not found' }


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

