FROM python:3.11-slim

WORKDIR /app

# Тәуелділіктерді жүктеу
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Кодты көшіру
COPY . .

# Тест деректерін жүктеу
RUN python seed_data.py

# Порт ашу
EXPOSE 8000

# Серверді іске қосу
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
