"""
Pydantic схемалары — API сұраныс/жауап форматтары
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# ─── КІТАП СХЕМАЛАРЫ ─────────────────────────────────────────

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    genre: str = "Белгісіз"
    pages: int = 0
    rating: float = 0.0
    cover_color: str = "#3A2010"
    published_year: Optional[int] = None
    is_featured: bool = False


class BookCreate(BookBase):
    """Жаңа кітап қосу үшін"""
    pass


class BookUpdate(BaseModel):
    """Кітапты өзгерту үшін (барлығы optional)"""
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    rating: Optional[float] = None


class BookResponse(BookBase):
    """Кітап жауабы"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── ПАЙДАЛАНУШЫ СХЕМАЛАРЫ ───────────────────────────────────

class UserCreate(BaseModel):
    """Тіркелу үшін"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Кіру үшін"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Пайдаланушы жауабы (парольсыз!)"""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    books_read: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── ОҚУ БАРЫСЫ СХЕМАЛАРЫ ────────────────────────────────────

class ProgressUpdate(BaseModel):
    """Оқу барысын жаңарту"""
    progress_pct: int      # 0-100 пайыз
    current_page: int = 0


class ProgressResponse(BaseModel):
    """Оқу барысы жауабы"""
    id: int
    user_id: int
    book_id: int
    progress_pct: int
    current_page: int
    is_completed: bool
    book: BookResponse
    last_read_at: datetime

    class Config:
        from_attributes = True
