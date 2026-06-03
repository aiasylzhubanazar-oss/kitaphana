"""
Database Connection — SQLAlchemy + SQLite
Developer 1 жасайды
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite (дамыту кезінде), PostgreSQL-ге ауыстыруға болады
DATABASE_URL = "sqlite:///./kitaphana.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite үшін
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency — роутерларда қолданылады
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
