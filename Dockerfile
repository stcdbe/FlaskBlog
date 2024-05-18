FROM python:3.11.8-alpine AS builder

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir -U pip setuptools && \
    pip install --no-cache-dir poetry && \
    poetry self add poetry-plugin-export && \
    poetry export -o requirements.prod.txt --without-hashes && \
    poetry export --with=dev -o requirements.dev.txt --without-hashes

FROM python:3.11.8-alpine AS dev

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder requirements.dev.txt /app

RUN pip install --no-cache-dir -U pip setuptools && \
    pip install --no-cache-dir -r requirements.dev.txt

COPY . .
