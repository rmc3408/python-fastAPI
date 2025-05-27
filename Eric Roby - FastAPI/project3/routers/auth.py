from fastapi import APIRouter, Body, Depends, Request, Response, status
from sqlalchemy import select
from ..database import session
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from ..models.task import RoleUser, User
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext


router = APIRouter()

# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency to get the database session
def get_db():
    db = session
    try:
      yield db #Like AWAIT
    finally:
        db.close()

DB_Dependency = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(min_length=5, max_length=50)
    password: str = Field(min_length=2)
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)
    role: RoleUser


@router.get("/current")
async def getUser(request: Request):
  cok = request.cookies.get('user')
  if not cok:
      return {"message": "No user cookie found"}
  return {"message": cok}


@router.get("/users")
def read_all_users(db: DB_Dependency):
  result = db.query(User).all()
  return result


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_users(body: CreateUserRequest, db: DB_Dependency):
  raw_data = body.model_dump()
  new_user = User(
      username=raw_data['username'],
      email=raw_data['email'],
      hashed_password=bcrypt_context.hash(raw_data['password']),
      first_name=raw_data['first_name'],
      last_name=raw_data['last_name'],
      role=raw_data['role'],
      is_active=True,
  )
  db.add(new_user)
  db.commit()
  result = db.get(User, new_user.id)
  if result is None:
      return {"message": "User not created"}
  return result


@router.post("/signin")
def signin(db: DB_Dependency, response: Response, raw_data = Body()):
    
    # Validate a existing user by username
    statement = select(User).where(User.username == raw_data['username'])
    user = db.execute(statement).scalars().first()
    if user is None:
      return {"message": "Invalid username or password"}
    

    # Check if the password is correct using bcrypt
    if user.hashed_password is str:
      print(raw_data['password'], user.hashed_password)
      passChecked = bcrypt_context.verify(raw_data['password'], user.hashed_password)
      print('PASSED CHECKED:', passChecked)

      if passChecked is False:
          return {"message": "password does not match"}
    
    # Set the user cookie Authenticated
    response.set_cookie(key="user", value=str(user.username), httponly=True)

    return {"message": "User signed in successfully"}