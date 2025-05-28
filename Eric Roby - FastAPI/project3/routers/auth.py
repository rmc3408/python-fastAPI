from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from ..database import session
from sqlalchemy.orm import Session, joinedload
from typing import Annotated, Optional
from ..models.task import RoleUser, User
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone


router = APIRouter(prefix="/auth", tags=["auth"])

# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/whoami")

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

class SignInRequest(BaseModel):
    username: str 
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class BearerData(BaseModel):
    exp: datetime
    sub: str
    role: str
    id: int

class CurrentUser(BaseModel):
    from_cookie: str
    from_bearer: BearerData


credentials_exception = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED,
  detail="Could not validate credentials",
  headers={"WWW-Authenticate": "Bearer"},
)

async def validate_user(token: Annotated[str, Depends(oauth2_bearer)]) -> BearerData:
    try:
        payload = jwt.decode(token, 'ABCD', algorithms=["HS256"])
        if payload is None:
            raise credentials_exception
        return BearerData(**payload)
    except InvalidTokenError:
        raise credentials_exception

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    # Validate a existing user by username
    statement = select(User).where(User.username == username)
    user = db.execute(statement).scalars().first()
    if not user:
        return None
    if not bcrypt_context.verify(password, str(user.hashed_password)):
        return None
    return user

def create_access_token(data: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    user_dict = data.to_dict()
    to_encode = {
        "exp": expire, 
        "sub": user_dict['username'], 
        "role": user_dict['role'].value,
        "id": user_dict['id'],
    }
    encoded_jwt = jwt.encode(to_encode, 'ABCD', algorithm="HS256")
    return encoded_jwt

## AUTH ROUTES ###
@router.get("/whoami", response_model=CurrentUser)
async def get_current_user(request: Request, current_user: Annotated[BearerData, Depends(validate_user)]): 
  cookie = request.cookies.get('user')
  if not cookie:
      return {"message": "No user cookie found"}
  return CurrentUser(from_cookie=cookie, from_bearer=current_user)

@router.post("/signin", response_model=Token)
def signin(db: DB_Dependency, response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Check if the password is correct using bcrypt
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise credentials_exception
    
    #set JWT token
    access_token = create_access_token(data=user)

    # Set the user cookie Authenticated
    response.set_cookie(key="user", value=form_data.username, httponly=True)

    return Token(access_token=access_token, token_type="bearer")

### USER ROUTES ###

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