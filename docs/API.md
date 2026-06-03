# 📡 API Документациясы

Base URL: `http://localhost:8000/api`

Интерактивті docs: `http://localhost:8000/docs`

---

## 📖 Кітаптар

### GET /books
Барлық кітаптар тізімі.

**Query параметрлері:**
| Параметр | Тип | Сипаттама |
|----------|-----|-----------|
| `genre` | string | Жанр бойынша сүзгі |
| `featured` | bool | Тек ерекше кітаптар |
| `limit` | int | Максимал саны (default: 20) |
| `offset` | int | Бастапқы орын |

**Жауап:**
```json
[
  {
    "id": 1,
    "title": "Абай жолы",
    "author": "Мұхтар Әуезов",
    "genre": "Қазақ әдебиеті",
    "pages": 873,
    "rating": 4.9,
    "cover_color": "#4A2F1A",
    "is_featured": true,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### GET /books/search?q={сөз}
Кітаптарды атауы немесе автор бойынша іздеу.

---

### GET /books/{id}
ID бойынша кітап мәліметтері. 404 қайтарады егер жоқ болса.

---

### POST /books
Жаңа кітап қосу.

**Body:**
```json
{
  "title": "Кітап атауы",
  "author": "Автор аты",
  "genre": "Жанр",
  "pages": 300,
  "rating": 4.5,
  "cover_color": "#3A2010"
}
```

---

### PUT /books/{id}
Кітапты өзгерту (тек өзгертілетін өрістер жіберіледі).

---

### DELETE /books/{id}
Кітапты жою. 204 қайтарады.

---

### GET /genres
Барлық жанрлар тізімі.

```json
["Қазақ әдебиеті", "Тарих", "Философия", "Фольклор"]
```

---

## 👤 Пайдаланушылар

### POST /users/register
```json
{
  "username": "aibek",
  "email": "aibek@example.com",
  "password": "secure123",
  "full_name": "Айбек Сейітов"
}
```

---

### POST /users/login
```json
{
  "username": "aibek",
  "password": "secure123"
}
```

**Жауап:**
```json
{
  "message": "Сәтті кірдіңіз!",
  "user_id": 1,
  "username": "aibek",
  "token": "demo_token_1"
}
```

---

### GET /users/{id}
Пайдаланушы профилі.

---

## 📊 Оқу барысы

### GET /progress/{user_id}
Пайдаланушының барлық оқу барысы.

---

### PUT /progress/{user_id}/{book_id}
Оқу барысын жаңарту.

```json
{
  "progress_pct": 45,
  "current_page": 200
}
```

---

### DELETE /progress/{user_id}/{book_id}
Барысты жою.
