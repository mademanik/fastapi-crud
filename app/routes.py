from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schema import BookSchema, Request, Response, RequestBook

import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
async def create_book_service(request: RequestBook, db: Session = Depends(get_db)):
    new_book = crud.create_book(db, book=request.parameter)
    book_response = BookSchema.model_validate(new_book)
    return Response(status="Ok",
                    code="200",
                    message="Book created successfully",
                    result=book_response).dict(exclude_none=True)


@router.get("/")
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _books = crud.get_book(db, skip, limit)
    books_response = [BookSchema.model_validate(book) for book in _books]  # Convert ORM to Pydantic
    return Response(status="Ok", code="200", message="Success fetch all data", result=books_response)

@router.get("/{book_id}", response_model=BookSchema)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/update")
async def update_book(request: RequestBook, db: Session = Depends(get_db)):
    _book = crud.update_book(db, book_id=request.parameter.id,
                             title=request.parameter.title, description=request.parameter.description)
    book_response = BookSchema.model_validate(_book)  # Convert single object
    return Response(status="Ok", code="200", message="Success update data", result=book_response)


# Option 1: With path parameter
@router.delete("/delete/{book_id}")
async def delete_book_path(book_id: int, db: Session = Depends(get_db)):
    deleted_book = crud.remove_book(db, book_id=book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status="Ok", code="200", message="Success delete data", result="Book deleted")

