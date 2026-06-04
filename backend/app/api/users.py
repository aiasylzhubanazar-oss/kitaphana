"""
Пайдаланушылар API — /api/users
Developer 1 жасайды
"""

import hashlib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserLogin, UserResponse

router = APIRouter()


def hash_password(password: str) -> str:
    """Парольді хэштеу (SHA-256 — demo үшін; productionда bcrypt қолданыңыз)"""
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/users/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Жаңа пайдаланушы тіркеу"""
    # Username бар ма тексеру
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=400,
            detail="Бұл пайдаланушы аты бұрыннан тіркелген",
        )

    # Email бар ма тексеру
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=400,
            detail="Бұл email бұрыннан тіркелген",
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/users/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Пайдаланушы кіруі"""
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or user.hashed_password != hash_password(credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Пайдаланушы аты немесе пароль қате",
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Аккаунт белсенді емес")

    # Demo: нақты жобада JWT token беріледі
    return {
        "message": "Сәтті кірдіңіз!",
        "user_id": user.id,
        "username": user.username,
        "token": f"demo_token_{user.id}",  # Нақты жобада JWT болады
    }


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Пайдаланушы профилі"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пайдаланушы табылмады")
    return user
