#!/bin/sh
set -e

echo "Running database migrations..."

uv run alembic upgrade head

echo "Starting FastAPI..."

exec uv run uvicorn task_manager.main:app --host 0.0.0.0 --port 8000