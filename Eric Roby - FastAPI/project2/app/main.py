from fastapi import FastAPI
from .controller import create, read, update, delete

app = FastAPI()

app.include_router(read.router, prefix="/books")
app.include_router(create.router, prefix="/books")
app.include_router(update.router, prefix="/books")
app.include_router(delete.router, prefix="/books")

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}