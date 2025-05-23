from fastapi import APIRouter, Body
from ..utils.mock import BOOKS
from ..utils.helpers import find

router = APIRouter()

@router.put('/{id}')
async def update_book(id: str, update_book=Body()):
    
    [index, data] = find('id', id, BOOKS)
    print(f'index: {data}')
    if index == -1 or data == None:
        return { 'msg': 'Book not found' }

    for key in update_book.keys():
        if update_book[key] == None:
            continue
        data.update({ **data, key: update_book[key] })

    BOOKS[index] = data
    return { 'msg': data }