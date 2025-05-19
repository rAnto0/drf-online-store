FROM python:3.11-slim
WORKDIR /app

# Установим утилиты для сборки psycopg2
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ARG SECRET_KEY
# ENV SECRET_KEY=${SECRET_KEY}
# RUN python zaharovo/manage.py collectstatic --no-input

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1
EXPOSE 8000