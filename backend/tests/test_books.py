"""
Кітаптар API тесттері
Іске қосу: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Тест дерекқоры (бөлек файл)
TEST_DATABASE_URL = "sqlite:///./test_kitaphana.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Әр тест алдында таза дерекқор жасаймыз"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


class TestBooksAPI:
    """Кітаптар API тесттері"""

    def test_get_empty_books(self):
        """Бос дерекқорда кітаптар тізімі"""
        response = client.get("/api/books")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_book(self):
        """Жаңа кітап қосу"""
        book_data = {
            "title": "Абай жолы",
            "author": "Мұхтар Әуезов",
            "genre": "Қазақ әдебиеті",
            "pages": 873,
            "rating": 4.9,
            "cover_color": "#4A2F1A",
        }
        response = client.post("/api/books", json=book_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Абай жолы"
        assert data["author"] == "Мұхтар Әуезов"
        assert data["id"] is not None

    def test_get_book_by_id(self):
        """ID бойынша кітапты алу"""
        # Алдымен жасаймыз
        book_data = {
            "title": "Ботагөз",
            "author": "Сәкен Сейфуллин",
            "genre": "Тарих",
            "pages": 412,
            "rating": 4.7,
        }
        create_resp = client.post("/api/books", json=book_data)
        book_id = create_resp.json()["id"]

        # Содан кейін аламыз
        response = client.get(f"/api/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Ботагөз"

    def test_get_nonexistent_book(self):
        """Жоқ кітапты іздеу — 404 қайтаруы керек"""
        response = client.get("/api/books/99999")
        assert response.status_code == 404

    def test_search_books(self):
        """Кітаптарды іздеу"""
        # Кітаптар қосамыз
        books = [
            {"title": "Абай жолы", "author": "Мұхтар Әуезов", "genre": "Қазақ әдебиеті", "pages": 873, "rating": 4.9},
            {"title": "Ботагөз", "author": "Сәкен Сейфуллин", "genre": "Тарих", "pages": 412, "rating": 4.7},
        ]
        for b in books:
            client.post("/api/books", json=b)

        # Іздейміз
        response = client.get("/api/books/search?q=Абай")
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["title"] == "Абай жолы"

    def test_duplicate_book_rejected(self):
        """Бірдей кітапты екі рет қосу мүмкін емес"""
        book_data = {
            "title": "Тест кітап",
            "author": "Тест Автор",
            "genre": "Тест",
            "pages": 100,
            "rating": 4.0,
        }
        client.post("/api/books", json=book_data)
        response = client.post("/api/books", json=book_data)
        assert response.status_code == 400

    def test_filter_by_genre(self):
        """Жанр бойынша сүзгі"""
        books = [
            {"title": "Кітап 1", "author": "Автор 1", "genre": "Тарих", "pages": 300, "rating": 4.0},
            {"title": "Кітап 2", "author": "Автор 2", "genre": "Философия", "pages": 200, "rating": 4.2},
        ]
        for b in books:
            client.post("/api/books", json=b)

        response = client.get("/api/books?genre=Тарих")
        assert response.status_code == 200
        results = response.json()
        assert all(r["genre"] == "Тарих" for r in results)

    def test_get_genres(self):
        """Жанрлар тізімі"""
        books = [
            {"title": "К1", "author": "А1", "genre": "Тарих", "pages": 100, "rating": 4.0},
            {"title": "К2", "author": "А2", "genre": "Философия", "pages": 150, "rating": 4.1},
            {"title": "К3", "author": "А3", "genre": "Тарих", "pages": 200, "rating": 4.2},  # Қайталаған
        ]
        for b in books:
            client.post("/api/books", json=b)

        response = client.get("/api/genres")
        assert response.status_code == 200
        genres = response.json()
        assert "Тарих" in genres
        assert "Философия" in genres
        assert len(genres) == 2  # Қайталанбайды
