"""
KitapHana — Казақша Онлайн Кітапхана
Backend API (Developer 1 жасайды)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from database import engine, Base
from routers import books, users, search

# ───────────────────────────────────────────
# App creation
# ───────────────────────────────────────────
app = FastAPI(
    title="KitapHana API",
    description="Қазақша Онлайн Кітапхана — REST API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ───────────────────────────────────────────
# CORS — Frontend (Developer 2) үшін
# ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────────────────────────
# Database tables жасау
# ───────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ───────────────────────────────────────────
# Routers
# ───────────────────────────────────────────
app.include_router(books.router, prefix="/api", tags=["📚 Кітаптар"])
app.include_router(users.router, prefix="/api", tags=["👤 Пайдаланушылар"])
app.include_router(search.router, prefix="/api", tags=["🔍 Іздеу"])


# ───────────────────────────────────────────
# Root endpoint
# ───────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "app": "KitapHana",
        "version": "1.0.0",
        "status": "✅ Жұмыс істеп тұр",
        "docs": "/api/docs",
        "books": "/api/books",
    }


@app.get("/api/health", tags=["Root"])
def health():
    return {"status": "ok", "message": "KitapHana API is alive 🟢"}


# ───────────────────────────────────────────
# Run
# ───────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 50)
    print("  📚  KitapHana Backend Server")
    print("  🌐  http://localhost:8000")
    print("  📖  http://localhost:8000/api/docs")
    print("═" * 50 + "\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
