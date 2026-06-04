"""
Seed Script — Деректер базасына үлгі деректер қосу
Developer 1 іске қосады: python seed.py
"""

from database import SessionLocal, engine, Base
from models import Book, User
from routers.users import hash_password

# Tables жасау
Base.metadata.create_all(bind=engine)


BOOKS = [
    {
        "title": "Абай жолы",
        "author": "М. Әуезов",
        "genre": "Қазақ әдебиеті",
        "description": "Ұлы қазақ жазушысы Мұхтар Әуезовтің шедевры. Абай Құнанбаевтың өмірі туралы роман-эпопея.",
        "pages": 873,
        "rating": 4.9,
        "cover_color": "#4A2F1A",
        "year": 1942,
        "is_featured": True,
    },
    {
        "title": "Ботагөз",
        "author": "С. Сейфуллин",
        "genre": "Қазақ әдебиеті",
        "description": "Сәкен Сейфуллиннің тарихи романы. Азамат соғысы кезіндегі оқиғалар.",
        "pages": 412,
        "rating": 4.7,
        "cover_color": "#1C3A4E",
        "year": 1927,
        "is_featured": True,
    },
    {
        "title": "Дала уілі",
        "author": "Б. Майлин",
        "genre": "Қазақ әдебиеті",
        "description": "Бейімбет Майлиннің шығармалар жинағы.",
        "pages": 298,
        "rating": 4.6,
        "cover_color": "#2E1A4E",
        "year": 1935,
    },
    {
        "title": "Қан мен тер",
        "author": "А. Нұрпейісов",
        "genre": "Қазақ әдебиеті",
        "description": "Әбдіжәміл Нұрпейісовтың трилогиясы. Арал теңізіндегі балықшылар туралы.",
        "pages": 556,
        "rating": 4.8,
        "cover_color": "#103020",
        "year": 1961,
        "is_new": True,
        "is_featured": True,
    },
    {
        "title": "Атамекен",
        "author": "Ж. Аймауытов",
        "genre": "Тарих",
        "description": "Жүсіпбек Аймауытовтың романы.",
        "pages": 320,
        "rating": 4.5,
        "cover_color": "#4A1E1A",
        "year": 1926,
    },
    {
        "title": "Алдаркөсе",
        "author": "халық ертегісі",
        "genre": "Ертегі",
        "description": "Қазақ халқының сүйікті айлакер кейіпкері — Алдаркөсе туралы ертегілер жинағы.",
        "pages": 180,
        "rating": 4.4,
        "cover_color": "#3A1A3A",
        "year": 1900,
    },
    {
        "title": "Өтеген батыр",
        "author": "И. Есенберлин",
        "genre": "Тарих",
        "description": "Іліяс Есенберлиннің тарихи романы.",
        "pages": 445,
        "rating": 4.6,
        "cover_color": "#1A2A4A",
        "year": 1970,
    },
    {
        "title": "Жайық",
        "author": "Т. Ахтанов",
        "genre": "Қазақ әдебиеті",
        "description": "Тахауи Ахтановтың романы.",
        "pages": 380,
        "rating": 4.3,
        "cover_color": "#3A3A1A",
        "year": 1955,
    },
    {
        "title": "Сапар",
        "author": "О. Сүлейменов",
        "genre": "Поэзия",
        "description": "Олжас Сүлейменовтың өлеңдер жинағы.",
        "pages": 210,
        "rating": 4.7,
        "cover_color": "#1A3D4A",
        "year": 1975,
        "is_new": True,
    },
    {
        "title": "Ноғайлы",
        "author": "І. Есенберлин",
        "genre": "Тарих",
        "description": "«Көшпенділер» трилогиясының бірінші кітабы.",
        "pages": 520,
        "rating": 4.9,
        "cover_color": "#3A1A1A",
        "year": 1969,
        "is_featured": True,
    },
]

DEMO_USERS = [
    {
        "username": "aibek_reads",
        "email": "aibek@kitaphana.kz",
        "password": "demo1234",
        "full_name": "Айбек Сейтқали",
    },
    {
        "username": "dana_books",
        "email": "dana@kitaphana.kz",
        "password": "demo1234",
        "full_name": "Дана Нұрланова",
    },
]


def seed():
    db = SessionLocal()
    try:
        # Кітаптар
        existing_books = db.query(Book).count()
        if existing_books == 0:
            for book_data in BOOKS:
                book = Book(**book_data)
                db.add(book)
            db.commit()
            print(f"✅ {len(BOOKS)} кітап қосылды")
        else:
            print(f"ℹ️  Кітаптар бар ({existing_books} дана) — өткізілді")

        # Пайдаланушылар
        existing_users = db.query(User).count()
        if existing_users == 0:
            for user_data in DEMO_USERS:
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    hashed_password=hash_password(user_data["password"]),
                )
                db.add(user)
            db.commit()
            print(f"✅ {len(DEMO_USERS)} пайдаланушы қосылды")
        else:
            print(f"ℹ️  Пайдаланушылар бар ({existing_users} дана) — өткізілді")

        print("\n🎉 Seed аяқталды!")
        print("📖  http://localhost:8000/api/docs — API-ды тексеру үшін")

    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Деректер базасын толтыру...\n")
    seed()
