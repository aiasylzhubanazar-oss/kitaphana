"""
Тест деректері — дерекқорды нақты деректермен толтыру
Іске қосу: python seed_data.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models.models import Book, User
import hashlib

# Кестелерді жасаймыз
Base.metadata.create_all(bind=engine)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def seed():
    db = SessionLocal()

    # Кітаптар бар ма тексеру
    if db.query(Book).count() > 0:
        print("✅ Деректер бұрыннан бар, қайта жүктемейміз")
        db.close()
        return

    print("📚 Кітаптарды жүктеп жатырмыз...")

    books = [
        Book(
            title="Абай жолы",
            author="Мұхтар Әуезов",
            description="Абай Құнанбаевтың өмірі мен шығармашылығы туралы роман-эпопея. Қазақ әдебиетінің шедеврі.",
            genre="Қазақ әдебиеті",
            pages=873,
            rating=4.9,
            cover_color="#4A2F1A",
            published_year=1942,
            is_featured=True,
        ),
        Book(
            title="Ботагөз",
            author="Сәкен Сейфуллин",
            description="Азамат соғысы кезіндегі қазақ халқының өмірін суреттейтін тарихи роман.",
            genre="Тарих",
            pages=412,
            rating=4.7,
            cover_color="#1C3A4E",
            published_year=1938,
            is_featured=True,
        ),
        Book(
            title="Дала уілі",
            author="Бейімбет Майлин",
            description="Қазақ даласының өмірін, халықтың тұрмысын суреттейтін шығарма.",
            genre="Қазақ әдебиеті",
            pages=298,
            rating=4.6,
            cover_color="#2E1A4E",
            published_year=1935,
        ),
        Book(
            title="Қан мен тер",
            author="Әбдіжәміл Нұрпейісов",
            description="Аралдың балықшылары туралы трагедиялық роман-трилогия.",
            genre="Қазақ әдебиеті",
            pages=556,
            rating=4.8,
            cover_color="#1A3D2A",
            published_year=1961,
            is_featured=True,
        ),
        Book(
            title="Атамекен",
            author="Ғабит Мүсірепов",
            description="Туған жер сүйіспеншілігі туралы лирикалық проза.",
            genre="Қазақ әдебиеті",
            pages=185,
            rating=4.5,
            cover_color="#4A1E1A",
            published_year=1950,
        ),
        Book(
            title="Жайық",
            author="Хамза Есенжанов",
            description="Жайық өзені алқабындағы халықтың тағдыры.",
            genre="Тарих",
            pages=342,
            rating=4.3,
            cover_color="#3A3A1A",
            published_year=1968,
        ),
        Book(
            title="Алдаркөсе",
            author="Халық ертегілері",
            description="Қазақ халық ертегілерінің жинағы. Айлакер батыр Алдаркөсенің оқиғалары.",
            genre="Фольклор",
            pages=220,
            rating=4.4,
            cover_color="#1A2A4A",
            published_year=1900,
        ),
        Book(
            title="Сапарбай",
            author="Тахауи Ахтанов",
            description="Соғыс жылдарындағы адамзаттық ерлік пен махаббат.",
            genre="Тарих",
            pages=398,
            rating=4.6,
            cover_color="#3A1A3A",
            published_year=1957,
        ),
        Book(
            title="Шыңырау",
            author="Қабдеш Жұмаділов",
            description="Заманауи қазақ прозасының үздік үлгісі.",
            genre="Қазақ әдебиеті",
            pages=465,
            rating=4.5,
            cover_color="#1A3A2A",
            published_year=1980,
        ),
        Book(
            title="Тар жол, тайғақ кешу",
            author="Сәкен Сейфуллин",
            description="Автобиографиялық роман — революция жылдарындағы қазақ зиялысының өмірі.",
            genre="Тарих",
            pages=508,
            rating=4.7,
            cover_color="#2A1A1A",
            published_year=1927,
            is_featured=True,
        ),
    ]

    for book in books:
        db.add(book)

    print("👤 Тест пайдаланушыларды жүктеп жатырмыз...")

    users = [
        User(
            username="aibek",
            email="aibek@example.com",
            hashed_password=hash_password("password123"),
            full_name="Айбек Сейітов",
            books_read=5,
        ),
        User(
            username="ainur",
            email="ainur@example.com",
            hashed_password=hash_password("password123"),
            full_name="Айнұр Жақсыбекова",
            books_read=12,
        ),
        User(
            username="admin",
            email="admin@kitaphana.kz",
            hashed_password=hash_password("admin123"),
            full_name="Администратор",
            books_read=0,
        ),
    ]

    for user in users:
        db.add(user)

    db.commit()
    print("✅ Барлық деректер сәтті жүктелді!")
    print(f"   📚 {len(books)} кітап")
    print(f"   👤 {len(users)} пайдаланушы")
    print("\n🔑 Тест аккаунттары:")
    print("   aibek / password123")
    print("   ainur / password123")
    print("   admin / admin123")

    db.close()


if __name__ == "__main__":
    seed()
