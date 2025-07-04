FROM python:3.13.5-slim-bullseye

RUN apt-get update && apt-get install -y curl && apt-get clean

# Install Poetry
ENV POETRY_VERSION=2.1.3
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --only main

COPY . .

EXPOSE 8000
CMD ["python", "playground.py"]