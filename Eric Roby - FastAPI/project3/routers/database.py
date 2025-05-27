from fastapi import APIRouter, Depends
from pydantic import Field
from sqlalchemy.orm import joinedload, Session
from typing import Annotated
from ..models.task import RoleUser, User, Task, Comment
from ..database import session


router = APIRouter()

def get_db():
    db = session
    try:
      yield db #Like AWAIT
    finally:
        db.close()

DB_Dependency = Annotated[Session, Depends(get_db)]


@router.get("/seed")
def populate(db: DB_Dependency):
  user1 = User(username='user1', email='user36@example.com', hashed_password='hashedpassword1', first_name='First1', last_name='Last1', is_active=True, role=RoleUser.ADMIN)
  user2 = User(username='user2', email='user21@example.com', hashed_password='hashedpassword2', first_name='First2', last_name='Last2', is_active=True, role=RoleUser.USER)

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
  db.add_all([user1, user2, task1, task2, task3, task4, comment1, comment2])
 
  db.commit()
  return {"message": "Database populated with sample data."}
