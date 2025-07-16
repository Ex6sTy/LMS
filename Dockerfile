FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash gcc libpq-dev build-essential curl \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . .

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["bash"]
