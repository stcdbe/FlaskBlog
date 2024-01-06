FROM python:3.11.7-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache-dir --upgrade setuptools && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/prod.txt