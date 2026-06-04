"""
Search Router — /api/search
Developer 1 жасайды
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from database import get_db
from models import Book
from schemas import BookOut

router = APIRouter()


@router.get("/search", response_model=List[BookOut])
def search_books(
    q: str = Query(..., min_length=1, description="Іздеу сөзі"),
    db: Session = Depends(get_db),
):
    """
    Кітаптарды іздеу.
    Атауы, авторы немесе жанры бойынша іздейді.
    
    Мысалы: /api/search?q=абай
    """
    search_term = f"%{q.lower()}%"

    results = (
        db.query(Book)
        .filter(
            or_(
                Book.title.ilike(search_term),
                Book.author.ilike(search_term),
                Book.genre.ilike(search_term),
                Book.description.ilike(search_term),
            )
        )
        .limit(20)
        .all()
    )

    return results
