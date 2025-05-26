from fastapi import Depends, FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from typing import Annotated, Optional
from .database import engine, session
from .models.task import Base, Task, User, Comment

app = FastAPI()
# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = session
    try:
      yield db #Like AWAIT
    finally:
        db.close()

DB_Dependency = Annotated[Session, Depends(get_db)]

class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=50)
    priority: int = Field(gt=0, le=5, description="Priority must be between 1 and 5")
    user_id: int = Field(frozen=True)


class TaskCreateResponse(TaskCreateRequest):
    id: int
    completed: bool

class TaskUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=50)
    priority: int = Field(gt=0, le=5, description="Priority must be between 1 and 5")
    user_id: int = Field(frozen=True)
    completed: bool


@app.post("/tasks", response_model=TaskCreateResponse, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreateRequest, db: DB_Dependency):
    raw_data = body.model_dump()
    new_task = Task(
        title=raw_data['title'],
        description=raw_data['description'],
        priority=raw_data['priority'],
        user_id=raw_data['user_id'],
        completed=False
    )
    db.add(new_task)
    db.commit()
    data = db.get_one(Task, new_task.id)
    if data is None:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Task not created")
    return data


@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
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

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(db: DB_Dependency, task_id: int = Path(ge=1)):
    task = db.get_one(Task, task_id)
    if task is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def read_one_tasks(db: DB_Dependency, task_id: int = Path(gt=0)):
  result = db.query(Task).filter(Task.id == task_id).options(joinedload(Task.comment)).first()
  if result is None:
      return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
  print('ONE TASK')
  return result

@app.get("/tasks")
def read_all_tasks(db: DB_Dependency):
  # result = db.query(Task).all()
  query = select(Task).options(joinedload(Task.comment))
  result = db.execute(query).scalars().all()
  print('ALL TASK')
  return result


@app.get("/users")
def read_all_users(db: DB_Dependency):
  result = db.query(User).options(joinedload(User.tasks)).all()
  return result

@app.get("/user/{user_id}/alltasks")
def read_user_with_tasks(user_id: int, db: Session = Depends(get_db)):
    user = db.get_one(User, user_id)
    if user is None:
        return {"error": "User not found"}
    return user.tasks




@app.get("/populate")
def populate(db: DB_Dependency):
  user1 = User(username='user1', email='user1@example.com')
  user2 = User(username='user2', email='user2@example.com')

  task1 = Task(title='Task One', description='Description for task one', priority=2, completed=False)
  task2 = Task(title='Task Two', description='Description for task two', priority=1, completed=True)
  task3 = Task(title='Task Three', description='Description for task three', priority=3, completed=False)
  task4 = Task(title='Task Four', description='Description for task four', priority=1, completed=True)

  comment1 = Comment(content='Comment for task one', author='Author One')
  comment2 = Comment(content='Comment for task two', author='Author Two')

  task1.comment = comment1
  task2.comment = comment2

  user1.tasks.extend([task1, task2, task4])
  user2.tasks.append(task3)
  db.add_all([user1, user2, task1, task2, task3, task4])
 
  db.commit()
  return {"message": "Database populated with sample data."}