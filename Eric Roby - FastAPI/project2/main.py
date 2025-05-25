from .errors.book import BookException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .controller import create, read, update, delete

app = FastAPI()

app.include_router(read.router, prefix="/books")
app.include_router(create.router, prefix="/books")
app.include_router(update.router, prefix="/books")
app.include_router(delete.router, prefix="/books")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.exception_handler(BookException)
async def book_exception_handler(request: Request, exc: BookException):
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content={"message": f"BookException => {exc.detail}"},
    )