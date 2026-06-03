"""
Пайдаланушылар API тесттері
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test_users.db"
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
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


class TestUsersAPI:
    """Пайдаланушылар API тесттері"""

    def test_register_user(self):
        """Жаңа пайдаланушы тіркеу"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "secure123",
            "full_name": "Тест Пайдаланушы",
        }
        response = client.post("/api/users/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert "hashed_password" not in data  # Пароль қайтарылмайды!
        assert data["books_read"] == 0

    def test_register_duplicate_username(self):
        """Бірдей username тіркеу мүмкін емес"""
        user_data = {
            "username": "duplicate",
            "email": "first@example.com",
            "password": "pass123",
        }
        client.post("/api/users/register", json=user_data)

        user_data["email"] = "second@example.com"
        response = client.post("/api/users/register", json=user_data)
        assert response.status_code == 400

    def test_login_success(self):
        """Дұрыс деректермен кіру"""
        # Алдымен тіркелу
        client.post("/api/users/register", json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "mypassword",
        })

        # Кіру
        response = client.post("/api/users/login", json={
            "username": "logintest",
            "password": "mypassword",
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["username"] == "logintest"

    def test_login_wrong_password(self):
        """Қате паролмен кіру"""
        client.post("/api/users/register", json={
            "username": "wrongpass",
            "email": "wrong@example.com",
            "password": "correct",
        })

        response = client.post("/api/users/login", json={
            "username": "wrongpass",
            "password": "incorrect",
        })
        assert response.status_code == 401

    def test_get_user_profile(self):
        """Пайдаланушы профилін алу"""
        resp = client.post("/api/users/register", json={
            "username": "profileuser",
            "email": "profile@example.com",
            "password": "pass",
            "full_name": "Профиль Тест",
        })
        user_id = resp.json()["id"]

        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["full_name"] == "Профиль Тест"
