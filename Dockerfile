FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
# Shell form so $PORT expands (Railway sets it; array form would pass literal $PORT)
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --timeout 120 app:app
