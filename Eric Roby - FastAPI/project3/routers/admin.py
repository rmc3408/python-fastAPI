from fastapi import APIRouter, Depends, HTTPException, status
from project3.routers.auth import CurrentUser, get_current_user
from ..database import session
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from ..models.entity import RoleUser, Task, User
from pydantic import BaseModel, Field


router = APIRouter(prefix="/admin", tags=["admin"])

# Dependency to get the database session
def get_db():
    db = session
    try:
      yield db #Like AWAIT
    finally:
        db.close()

DB_Dependency = Annotated[Session, Depends(get_db)]
User_Dependency = Annotated[CurrentUser, Depends(get_current_user)]

# Pydantic models
class UsersResponse(BaseModel):
    id: int
    email: str
    role: RoleUser


# ADMIN ROUTES
@router.get("/users", response_model=list[UsersResponse])
def read_all_users(user: User_Dependency, db: DB_Dependency):
    if user is None or not user.from_bearer.role == RoleUser.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    return db.query(User).all()


@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(user: User_Dependency, db: DB_Dependency, task_id: int):
    if user is None or not user.from_bearer.role == RoleUser.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    task = db.get_one(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()
    return { "message": "Task deleted successfully"}
