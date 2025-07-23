FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash gcc libpq-dev build-essential curl \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock README.md ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry check && \
    poetry install --no-root --only main

COPY . .

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

