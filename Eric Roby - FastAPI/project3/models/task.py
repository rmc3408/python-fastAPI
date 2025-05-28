from typing import List
from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class RoleUser(Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(SQLEnum(RoleUser), default=RoleUser.USER)
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
    
    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String, nullable=True)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="tasks")
    comment: Mapped["Comment"] = relationship(back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, user_id={self.user_id}, completed={self.completed}, comment={self.comment})>"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String)
    author = Column(String, nullable=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task: Mapped["Task"] = relationship(back_populates="comment")

    def __repr__(self):
        return f"<Comment(id={self.id}, content={self.content}, author={self.author})>"
    
