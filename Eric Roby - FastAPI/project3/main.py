from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, database, task, admin
from .database import engine
from .models.entity import Base


app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(task.router)
app.include_router(database.router)
app.include_router(admin.router)

