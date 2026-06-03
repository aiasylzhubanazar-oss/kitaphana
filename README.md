# 📚 Кітапхана — Online Library Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)

**Қазақша онлайн кітапхана — 2 адаммен жасалған командалық жоба**

</div>

---

## 👥 Командалық бөліну

| Рөл | Тапсырмалар |
|-----|-------------|
| 🧑‍💻 **Developer 1 (Backend)** | Python FastAPI, SQLite, REST API, тесттер |
| 🎨 **Developer 2 (Frontend)** | HTML/CSS/JS, UI, API интеграциясы |

---

## 🗂️ Жоба құрылымы

```
kitaphana/
├── backend/                  # Python FastAPI сервер
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── api/
│   │   │   ├── books.py
│   │   │   ├── users.py
│   │   │   └── progress.py
│   │   ├── models/models.py
│   │   ├── schemas/schemas.py
│   │   └── services/book_service.py
│   ├── tests/
│   │   ├── test_books.py
│   │   └── test_users.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── seed_data.py
├── frontend/
│   ├── public/index.html
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/main.css
│   │   └── utils/api.js
│   └── package.json
├── docs/
│   ├── API.md
│   └── SETUP.md
├── docker-compose.yml
└── .github/workflows/ci.yml
```

---

## 🚀 Жылдам бастау

### Backend (Developer 1)
```bash
cd backend
pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### Frontend (Developer 2)
```bash
cd frontend
npm install
npm run dev
# Site: http://localhost:3000
```

### Docker (Екеуі де)
```bash
docker-compose up --build
```

---

## 🔗 API Endpoints

| Метод | URL | Сипаттама |
|-------|-----|-----------|
| GET | `/api/books` | Барлық кітаптар |
| GET | `/api/books/{id}` | Кітап мәліметі |
| GET | `/api/books/search?q=` | Іздеу |
| POST | `/api/books` | Жаңа кітап |
| GET | `/api/genres` | Жанрлар |
| POST | `/api/users/register` | Тіркелу |
| POST | `/api/users/login` | Кіру |
| GET | `/api/progress/{user_id}` | Оқу барысы |
| PUT | `/api/progress/{book_id}` | Барысты жаңарту |

---

## 🤝 GitHub жұмыс ағыны

```bash
# Developer 1
git checkout -b feature/backend-api
git commit -m "feat: add books API"
git push origin feature/backend-api
# → Pull Request жасаңыз

# Developer 2
git checkout -b feature/frontend-ui
git commit -m "feat: book catalog page"
git push origin feature/frontend-ui
# → Pull Request жасаңыз
```

## 🧪 Тесттер

```bash
cd backend && pytest tests/ -v
```
