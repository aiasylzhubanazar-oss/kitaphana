"""
Оқу барысы API — /api/progress
Developer 1 жасайды
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.models import ReadingProgress, Book, User
from app.schemas.schemas import ProgressUpdate, ProgressResponse

router = APIRouter()


@router.get("/progress/{user_id}", response_model=List[ProgressResponse])
def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    """Пайдаланушының барлық оқу барысы"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пайдаланушы табылмады")

    progress = (
        db.query(ReadingProgress)
        .filter(ReadingProgress.user_id == user_id)
        .order_by(ReadingProgress.last_read_at.desc())
        .all()
    )
    return progress


@router.put("/progress/{user_id}/{book_id}", response_model=ProgressResponse)
def update_progress(
    user_id: int,
    book_id: int,
    progress_data: ProgressUpdate,
    db: Session = Depends(get_db),
):
    """Оқу барысын жаңарту немесе жасау"""
    # Кітап бар ма тексеру
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Кітап табылмады")

    # Бар барысты табу немесе жаңасын жасау
    progress = (
        db.query(ReadingProgress)
        .filter(
            ReadingProgress.user_id == user_id,
            ReadingProgress.book_id == book_id,
        )
        .first()
    )

    if not progress:
        progress = ReadingProgress(user_id=user_id, book_id=book_id)
        db.add(progress)

    # Барысты жаңарту
    pct = max(0, min(100, progress_data.progress_pct))  # 0-100 арасында
    progress.progress_pct = pct
    progress.current_page = progress_data.current_page
    progress.last_read_at = datetime.utcnow()

    # Аяқталды ма?
    if pct >= 100:
        progress.is_completed = True
        # Пайдаланушының оқылған кітаптар санын арттыру
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.books_read += 1

    db.commit()
    db.refresh(progress)
    return progress


@router.delete("/progress/{user_id}/{book_id}", status_code=204)
def remove_progress(user_id: int, book_id: int, db: Session = Depends(get_db)):
    """Оқу барысын жою"""
    progress = (
        db.query(ReadingProgress)
        .filter(
            ReadingProgress.user_id == user_id,
            ReadingProgress.book_id == book_id,
        )
        .first()
    )

    if not progress:
        raise HTTPException(status_code=404, detail="Барыс табылмады")

    db.delete(progress)
    db.commit()
    return None
