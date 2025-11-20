FROM python:3.13-slim

WORKDIR /app

#для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync

COPY . .

CMD ["uv", "run", "src/main.py"]