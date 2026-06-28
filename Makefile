.PHONY: run migrate test lint ruffcheck

run:
	uv run flask --app app.main:app run

migrate:
	uv run flask --app app.main:app db upgrade

test:
	uv run pytest

lint:
	uv run ruff check .

ruffcheck: lint
