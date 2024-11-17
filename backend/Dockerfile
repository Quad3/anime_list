FROM python:3.10-alpine

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without test

# RUN alembic upgrade head
