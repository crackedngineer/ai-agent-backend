FROM python:3.13.5-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH"

RUN apk add --no-cache \
    gcc \
    libffi-dev \
    musl-dev \
    build-base \
    python3-dev \
    linux-headers \
    libpq \
    curl

RUN curl -sSL https://install.python-poetry.org | python -
WORKDIR /app

RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . .

EXPOSE 8000
CMD ["python", "playground.py"]