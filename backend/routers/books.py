"""
Books Router — /api/books
Developer 1 жасайды
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Book
from schemas import BookCreate, BookOut, BookUpdate, MessageOut

router = APIRouter()


@router.get("/books", response_model=List[BookOut])
def get_books(
    skip: int = 0,
    limit: int = 20,
    genre: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Барлық кітаптар тізімі.
    - genre параметрі арқылы жанр бойынша сүзуге болады
    - featured=true арқылы тек таңдаулыларды алуға болады
    """
    query = db.query(Book)

    if genre:
        query = query.filter(Book.genre == genre)
    if featured is not None:
        query = query.filter(Book.is_featured == featured)

    books = query.offset(skip).limit(limit).all()
    return books


@router.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Бір кітапты ID бойынша алу"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Кітап табылмады (id={book_id})",
        )
    return book


@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """Жаңа кітап қосу"""
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.patch("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, updates: BookUpdate, db: Session = Depends(get_db)):
    """Кітап мәліметтерін жаңарту"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Кітап табылмады")

    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/books/{book_id}", response_model=MessageOut)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Кітапты өшіру"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Кітап табылмады")

    db.delete(book)
    db.commit()
    return {"message": f"'{book.title}' кітабы өшірілді", "success": True}


@router.get("/genres", response_model=List[str])
def get_genres(db: Session = Depends(get_db)):
    """Барлық жанрлар тізімі"""
    genres = db.query(Book.genre).distinct().all()
    return [g[0] for g in genres]
