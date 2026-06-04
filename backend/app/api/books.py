"""
Кітаптар API — /api/books
Developer 1 жасайды
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.models import Book
from app.schemas.schemas import BookCreate, BookResponse, BookUpdate

router = APIRouter()


@router.get("/books", response_model=List[BookResponse])
def get_books(
    genre: Optional[str] = Query(None, description="Жанр бойынша сүзгі"),
    featured: Optional[bool] = Query(None, description="Тек ерекше кітаптар"),
    limit: int = Query(20, le=100, description="Максимал саны"),
    offset: int = Query(0, description="Бастапқы орын"),
    db: Session = Depends(get_db),
):
    """Барлық кітаптар тізімі — фильтр мен pagination бар"""
    query = db.query(Book)

    if genre:
        query = query.filter(Book.genre == genre)
    if featured is not None:
        query = query.filter(Book.is_featured == featured)

    books = query.order_by(Book.rating.desc()).offset(offset).limit(limit).all()
    return books


@router.get("/books/search", response_model=List[BookResponse])
def search_books(
    q: str = Query(..., min_length=1, description="Іздеу сөзі"),
    db: Session = Depends(get_db),
):
    """Кітаптарды атауы немесе автор бойынша іздеу"""
    search_term = f"%{q}%"
    books = db.query(Book).filter(
        or_(
            Book.title.ilike(search_term),
            Book.author.ilike(search_term),
        )
    ).limit(20).all()

    if not books:
        return []
    return books


@router.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """ID бойынша кітап мәліметтері"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Кітап табылмады")
    return book


@router.post("/books", response_model=BookResponse, status_code=201)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """Жаңа кітап қосу"""
    # Бірдей кітап бар ма тексеру
    existing = db.query(Book).filter(
        Book.title == book_data.title,
        Book.author == book_data.author,
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Бұл кітап бұрыннан бар",
        )

    new_book = Book(**book_data.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
):
    """Кітап мәліметтерін өзгерту"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Кітап табылмады")

    update_data = book_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Кітапты жою"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Кітап табылмады")

    db.delete(book)
    db.commit()
    return None


@router.get("/genres", response_model=List[str])
def get_genres(db: Session = Depends(get_db)):
    """Барлық жанрлар тізімі"""
    genres = db.query(Book.genre).distinct().all()
    return [g[0] for g in genres if g[0]]
