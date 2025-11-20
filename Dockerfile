FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync

COPY . .

RUN chmod +x docker/scripts/entrypoint.sh

CMD ["./docker/scripts/entrypoint.sh"]