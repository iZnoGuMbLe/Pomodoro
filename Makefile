run:
	uvicorn main:app --reload --env-file .local.env

migrate-create:
	alembic revision --autogenerate -m $(NAME)

migrate-apply:
	alembic upgrade head

