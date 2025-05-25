from fastapi import APIRouter
from ..utils.mock import BOOKS
from ..utils.helpers import find

router = APIRouter()

@router.delete('/{id}')
async def remove_book(id: str):
    [ index, data ] = find('id', id, BOOKS)
    if index != -1:
        del BOOKS[index]
        return { 'msg': f'deleted books index {index}', 'item_deleted': data }
    else:
        return { 'msg': 'book not found' }