from typing import Optional
from pydantic import BaseModel, Field, model_serializer

class Book():
    def __init__(self, id: int, title: str, author: str, description: str, rating: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.description: str = description
        self.rating: int = rating

    def __repr__(self):
        return f"({self.id}, {self.title}, {self.author}, {self.description}, {self.rating})"


BOOKS: list[Book] = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "A novel about the American dream and the Roaring Twenties.", 4),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "A novel about racial injustice in the Deep South.", 5),
    Book(3, "1984", "George Orwell", "A dystopian novel about totalitarianism and surveillance.", 5),
]


class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, description="ID of the book, auto-generated if not provided")
    title: str=Field(min_length=3)
    author: str=Field(min_length=3)
    description: str=Field(min_length=5, max_length=100)
    rating: int=Field(ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A novel about the American dream and the Roaring Twenties.",
                "rating": 4
            }
        }
    }


class BookResponse(BaseModel):
    id: int
    title: str

    @model_serializer()
    def book_serialize(self):
        return {
            'id' : self.id,
            'title' : 'the ' + self.title
        }


class BookUpdateRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[int] = None


class BookUpdateResponse(BookUpdateRequest):
    id: int
