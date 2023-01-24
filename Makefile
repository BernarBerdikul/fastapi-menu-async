start: # run migrations and start uvicorn server
	poetry run alembic upgrade head
	poetry run uvicorn src.main:app --reload

test: # run tests
	poetry run pytest -vv
