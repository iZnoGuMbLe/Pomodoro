run:
	poetry run gunicorn app.main:app -c gunicorn.conf.py

migrate-create:
	alembic revision --autogenerate -m $(NAME)

migrate-apply:
	alembic upgrade head

