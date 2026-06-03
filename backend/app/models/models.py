"""
SQLAlchemy модельдері — дерекқор кестелері
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
)
from sqlalchemy.orm import relationship
from app.database import Base


class Book(Base):
    """Кітап кестесі"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)          # Атауы
    author = Column(String(255), nullable=False, index=True)         # Автор
    description = Column(Text, nullable=True)                         # Сипаттама
    genre = Column(String(100), nullable=False, default="Белгісіз")  # Жанр
    pages = Column(Integer, nullable=False, default=0)                # Беттер саны
    rating = Column(Float, nullable=False, default=0.0)               # Рейтинг
    cover_color = Column(String(20), default="#3A2010")               # Мұқаба түсі
    published_year = Column(Integer, nullable=True)                   # Жыл
    is_featured = Column(Boolean, default=False)                      # Ерекше кітап
    created_at = Column(DateTime, default=datetime.utcnow)

    # Байланыстар
    progress_items = relationship("ReadingProgress", back_populates="book")


class User(Base):
    """Пайдаланушы кестесі"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    books_read = Column(Integer, default=0)                # Оқылған кітаптар
    created_at = Column(DateTime, default=datetime.utcnow)

    # Байланыстар
    progress_items = relationship("ReadingProgress", back_populates="user")


class ReadingProgress(Base):
    """Оқу барысы кестесі"""
    __tablename__ = "reading_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    progress_pct = Column(Integer, default=0)              # Пайыз (0-100)
    current_page = Column(Integer, default=0)              # Ағымдағы бет
    is_completed = Column(Boolean, default=False)          # Аяқталды ма?
    started_at = Column(DateTime, default=datetime.utcnow)
    last_read_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Байланыстар
    user = relationship("User", back_populates="progress_items")
    book = relationship("Book", back_populates="progress_items")
