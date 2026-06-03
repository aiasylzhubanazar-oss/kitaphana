"""
Pydantic Schemas — Request / Response validation
Developer 1 жасайды
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ──────────────────────────────────────────
# BOOK Schemas
# ──────────────────────────────────────────

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, example="Абай жолы")
    author: str = Field(..., min_length=1, max_length=255, example="М. Әуезов")
    genre: str = Field(..., example="Қазақ әдебиеті")
    description: Optional[str] = None
    pages: Optional[int] = Field(default=0, ge=0)
    rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    cover_color: Optional[str] = Field(default="#3A2010", example="#4A2F1A")
    year: Optional[int] = None
    language: Optional[str] = "Қазақша"
    is_new: Optional[bool] = False
    is_featured: Optional[bool] = False


class BookCreate(BookBase):
    """POST /api/books — Кітап жасау"""
    pass


class BookUpdate(BaseModel):
    """PATCH /api/books/{id} — Кітап жаңарту"""
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    pages: Optional[int] = None
    rating: Optional[float] = None
    is_new: Optional[bool] = None
    is_featured: Optional[bool] = None


class BookOut(BookBase):
    """GET response"""
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────
# USER Schemas
# ──────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100, example="aibek_reads")
    email: EmailStr = Field(..., example="aibek@example.com")
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ──────────────────────────────────────────
# PROGRESS Schemas
# ──────────────────────────────────────────

class ProgressUpdate(BaseModel):
    book_id: int
    percent: int = Field(..., ge=0, le=100)
    current_page: Optional[int] = 0


class ProgressOut(BaseModel):
    id: int
    book_id: int
    percent: int
    current_page: int
    updated_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────
# GENERIC Schemas
# ──────────────────────────────────────────

class MessageOut(BaseModel):
    message: str
    success: bool = True
