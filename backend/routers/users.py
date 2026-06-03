"""
Users Router — /api/users
Developer 1 жасайды
JWT Authentication бар
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from models import User
from schemas import UserCreate, UserLogin, UserOut, Token, MessageOut

router = APIRouter()

# ──────────────────────────────────────────
# Security Config
# ──────────────────────────────────────────
SECRET_KEY = "kitaphana-super-secret-2024-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 сағат

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ──────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────

@router.post("/users/register", response_model=UserOut, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Жаңа пайдаланушы тіркеу"""
    # Username тексеру
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бұл username бұрын тіркелген",
        )
    # Email тексеру
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бұл email бұрын тіркелген",
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/users/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Жүйеге кіру — JWT token қайтарады"""
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Қате логин немесе пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/{username}", response_model=UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    """Пайдаланушы профилін алу"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пайдаланушы табылмады")
    return user
