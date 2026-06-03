"""
Database Models — SQLAlchemy ORM
Developer 1 жасайды
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Book(Base):
    """Кітап моделі"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    pages = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    cover_color = Column(String(20), default="#3A2010")
    year = Column(Integer, nullable=True)
    language = Column(String(50), default="Қазақша")
    is_new = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    progresses = relationship("ReadingProgress", back_populates="book")

    def __repr__(self):
        return f"<Book id={self.id} title='{self.title}'>"


class User(Base):
    """Пайдаланушы моделі"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    progresses = relationship("ReadingProgress", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} username='{self.username}'>"


class ReadingProgress(Base):
    """Оқу барысы моделі"""
    __tablename__ = "reading_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    percent = Column(Integer, default=0)        # 0–100
    current_page = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="progresses")
    book = relationship("Book", back_populates="progresses")

    def __repr__(self):
        return f"<Progress user={self.user_id} book={self.book_id} {self.percent}%>"
