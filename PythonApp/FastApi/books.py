from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

BOOKS = {
    1: {'title': 'Title One', 'author': 'Author 1'},
    2: {'title': 'Title Two', 'author': 'Author 2'},
    3: {'title': 'Title Three', 'author': 'Author 3'},
    4: {'title': 'Title Four', 'author': 'Author 4'},
    5: {'title': 'Title Five', 'author': 'Author 5'}
}


# GET
@app.get("/")
async def read_all_books(skip_book_id: Optional[int] = None) -> dict[int, dict[str, str]]:
    if skip_book_id:
        new_books = BOOKS.copy()
        del new_books[skip_book_id]
        return new_books
    return BOOKS


# Basic GET
@app.get("/books/my_book")
async def read_favorite_book() -> dict[str, str]:
    return {'book_title': 'My favorite book'}


# Query Parameter GET
@app.get("/books/")
async def read_book(book_id: int) -> dict[str, str]:
    validate_book_id(book_id)
    return BOOKS.get(book_id)


# Path Parameter GET
@app.get("/books/{book_id}")
async def read_book(book_id: int) -> dict[str, str]:
    validate_book_id(book_id)
    return BOOKS.get(book_id)


# Basic POST
@app.post("/")
async def create_book(book_title: str, book_author: str) -> JSONResponse:
    book_id = len(BOOKS) + 1
    book = {'title': book_title, 'author': book_author}
    BOOKS[book_id] = book
    return JSONResponse(status_code=202, content=book)


# Basic PUT
@app.put("/books/{book_id}")
async def update_book(book_id: int, book_title: str, book_author: str) -> JSONResponse:
    validate_book_id(book_id)
    book = BOOKS.get(book_id)
    book['title'] = book_title
    book['author'] = book_author
    BOOKS[book_id] = book
    return JSONResponse(status_code=202, content=book)


# Basic DELETE
@app.delete("/books/{book_id}")
async def delete_book(book_id: int) -> JSONResponse:
    validate_book_id(book_id)
    book = BOOKS.get(book_id)
    del BOOKS[book_id]
    return JSONResponse(status_code=202, content=book)


@app.delete("/books/")
async def delete_book(book_id: int) -> JSONResponse:
    validate_book_id(book_id)
    book = BOOKS.get(book_id)
    del BOOKS[book_id]
    return JSONResponse(status_code=202, content=book)


# Helper Method
def validate_book_id(book_id: int) -> None:
    if book_id > len(BOOKS) or book_id <= 0:
        raise HTTPException(status_code=401, detail="Invalid Book Id")
