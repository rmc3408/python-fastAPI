from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import joinedload, Session
from typing import Optional, Annotated
from ..models.task import Task
from ..database import session
from ..routers.auth import get_current_user, CurrentUser


router = APIRouter()

def get_db():
    db = session
    try:
      yield db #Like AWAIT
    finally:
        db.close()

DB_Dependency = Annotated[Session, Depends(get_db)]
User_Dependency = Annotated[CurrentUser, Depends(get_current_user)]  # Placeholder for user ID dependency

class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=50)
    priority: int = Field(gt=0, le=5, description="Priority must be between 1 and 5")
    user_id: Optional[int] = None

class TaskCreateResponse(TaskCreateRequest):
    id: int
    completed: bool


class TaskUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=50)
    priority: int = Field(gt=0, le=5, description="Priority must be between 1 and 5")
    user_id: int = Field(frozen=True)
    completed: bool


@router.post("/tasks", response_model=TaskCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_task(user: User_Dependency, body: TaskCreateRequest, db: DB_Dependency):
    
    raw_data = body.model_dump()
    from_bearer = user.model_dump().get('from_bearer')

    new_task = Task(
        title=raw_data['title'],
        description=raw_data['description'],
        priority=raw_data['priority'],
        user_id=from_bearer.get('id') if from_bearer is not None else 0,
        completed=False
    )
    db.add(new_task)
    db.commit()
    data = db.get_one(Task, new_task.id)
    if data is None:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Task not created")
    return data


@router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, body: TaskUpdateRequest, db: DB_Dependency):
    raw_data = body.model_dump()
    task = db.get_one(Task, task_id)
    if task is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    task.title = raw_data['title']
    task.description = raw_data['description']
    task.priority = raw_data['priority']
    task.completed = raw_data['completed']
    
    db.add(task)
    db.commit()
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(db: DB_Dependency, task_id: int = Path(ge=1)):
    task = db.get_one(Task, task_id)
    if task is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def read_one_tasks(db: DB_Dependency, task_id: int = Path(gt=0)):
  result = db.query(Task).filter(Task.id == task_id).options(joinedload(Task.comment)).first()
  if result is None:
      return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
  print('ONE TASK')
  return result


@router.get("/tasks")
def read_all_tasks(db: DB_Dependency):
  # result = db.query(Task).all()
  query = select(Task).options(joinedload(Task.comment))
  result = db.execute(query).scalars().all()
  print('ALL TASK')
  return result
