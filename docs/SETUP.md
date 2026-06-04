# 🛠️ Орнату нұсқаулығы

## Developer 1 (Backend) үшін

### 1. Репозиторийді fork жасаңыз
GitHub-та "Fork" батырмасын басыңыз.

### 2. Клондаңыз
```bash
git clone https://github.com/YOUR_USERNAME/kitaphana.git
cd kitaphana
```

### 3. Backend branch жасаңыз
```bash
git checkout -b feature/backend-api
```

### 4. Python ортасын орнатыңыз
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Тест деректерін қосыңыз
```bash
python seed_data.py
```

### 6. Серверді іске қосыңыз
```bash
uvicorn app.main:app --reload --port 8000
```

✅ API: http://localhost:8000
✅ Docs: http://localhost:8000/docs

### 7. Тесттерді іске қосыңыз
```bash
pytest tests/ -v
```

---

## Developer 2 (Frontend) үшін

### 1. Репозиторийді клондаңыз
```bash
git clone https://github.com/DEVELOPER1_USERNAME/kitaphana.git
cd kitaphana
```

### 2. Frontend branch жасаңыз
```bash
git checkout -b feature/frontend-ui
```

### 3. Node.js тәуелділіктерін орнатыңыз
```bash
cd frontend
npm install
```

### 4. Сайтты іске қосыңыз
```bash
npm run dev
```

✅ Site: http://localhost:3000

> **Ескерту:** Backend іске қосулы болса, API-мен жұмыс жасайды.
> Болмаса, demo деректермен жұмыс жасайды.

---

## Docker арқылы (Екеуі де)

```bash
# Жоба папкасынан:
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## GitHub Pull Request жасау

### Developer 1:
```bash
git add backend/
git commit -m "feat: add books/users/progress API"
git push origin feature/backend-api
```
GitHub-та: Pull Request → main branch-қа → Developer 2 review жасайды

### Developer 2:
```bash
git add frontend/
git commit -m "feat: add book catalog and auth UI"
git push origin feature/frontend-ui
```
GitHub-та: Pull Request → main branch-қа → Developer 1 review жасайды

---

## VS Code кеңестері

Ұсынылатын extensions:
- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **REST Client** (humao.rest-client) — API тестілеу үшін
- **Live Server** (ritwickdey.liveserver) — Frontend үшін
- **GitLens** (eamodio.gitlens) — Git үшін
- **Docker** (ms-azuretools.vscode-docker)

`.vscode/settings.json` файлы жобада бар — автоматты конфигурация.
