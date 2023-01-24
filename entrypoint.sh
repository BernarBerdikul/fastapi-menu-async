#!/bin/sh
echo "Run migrations..."
poetry run alembic -c ./alembic.ini upgrade head

echo "Starting server..."
exec uvicorn src.main:app --host 0.0.0.0 --reload
