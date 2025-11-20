#!/bin/sh
echo "Running migrations..."
uv run alembic upgrade head

echo "Starting bot..."
exec uv run python src/main.py
