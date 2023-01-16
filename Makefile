start: #use last migration and start uvicorn server for menu_app
	poetry run alembic upgrade head
	poetry run uvicorn src.main:app --reload
