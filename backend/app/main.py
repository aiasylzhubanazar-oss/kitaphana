"""
Кітапхана — Online Library Platform
Backend: FastAPI + SQLite
Developer 1 жасайды
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import books, users, progress

# Дерекқор кестелерін жасаймыз
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="📚 Кітапхана API",
    description="Қазақша онлайн кітапхана платформасының REST API-і",
    version="1.0.0",
)

# CORS — frontend-пен жұмыс жасауға рұқсат береміз
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутерлерді қосамыз
app.include_router(books.router, prefix="/api", tags=["📖 Кітаптар"])
app.include_router(users.router, prefix="/api", tags=["👤 Пайдаланушылар"])
app.include_router(progress.router, prefix="/api", tags=["📊 Оқу барысы"])


@app.get("/", tags=["🏠 Басты"])
async def root():
    """API жұмыс жасап тұр ма тексеру"""
    return {
        "message": "📚 Кітапхана API жұмыс жасап тұр!",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["🏥 Денсаулық"])
async def health_check():
    """Сервер күйін тексеру"""
    return {"status": "ok", "service": "kitaphana-api"}
