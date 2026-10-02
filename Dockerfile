FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CAPSTONE_DB_PATH=/app/data/capstone.sqlite3

RUN mkdir -p /app/data

EXPOSE 8000

# Uvicorn serves the ASGI capstone directly in this learning container.
CMD ["uvicorn", "capstone_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
