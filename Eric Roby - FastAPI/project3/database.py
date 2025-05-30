from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


SQLLITE_DATABASE_URL = "sqlite:///./project3.db"
POSTGRES_DATABASE_URL = "postgresql://admin:root@localhost/db"

# engine = create_engine(SQLLITE_DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()
