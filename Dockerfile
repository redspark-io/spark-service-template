FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

RUN pip install --upgrade pip

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# install dependencies
RUN pip install poetry==2.1.1
RUN poetry install --only=main --no-interaction --no-ansi  && rm -rf $POETRY_CACHE_DIR
