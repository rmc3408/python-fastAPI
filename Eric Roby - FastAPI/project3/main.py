from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from .database import engine, session
from .models.task import Base, Task, User

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
      yield db
    finally:
        db.close()



@app.get("/tasks")
def read_all_tasks(db: Annotated[Session, Depends(get_db)]):
  result = db.query(Task).all()
  return result

@app.get("/users")
def read_all_users(db: Annotated[Session, Depends(get_db)]):
  result = db.query(User).options(joinedload(User.tasks)).all()
  return result

@app.get("/user/{user_id}/alltasks")
def read_user_with_tasks(user_id: int, db: Session = Depends(get_db)):
    user = db.get_one(User, user_id)
    if user is None:
        return {"error": "User not found"}
    return user.tasks


@app.get("/populate")
def populate(db: Annotated[Session, Depends(get_db)]):
  user1 = User(username='user1', email='user1@example.com')
  user2 = User(username='user2', email='user2@example.com')

  task1 = Task(title='Task One', description='Description for task one', priority=2, completed=False)
  task2 = Task(title='Task Two', description='Description for task two', priority=1, completed=True)
  task3 = Task(title='Task Three', description='Description for task three', priority=3, completed=False)
  task4 = Task(title='Task Four', description='Description for task four', priority=1, completed=True)

  user1.tasks.extend([task1, task2, task4])
  user2.tasks.append(task3)
  db.add_all([user1, user2, task1, task2, task3, task4])
 
  db.commit()
  return {"message": "Database populated with sample data."}