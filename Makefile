.PHONY: run migrate test lint ruffcheck docker-build docker-run compose-up compose-down

run:
	uv run flask --app app.main:app run

migrate:
	uv run flask --app app.main:app db upgrade

test:
	uv run pytest

lint:
	uv run ruff check .

ruffcheck: lint

VERSION := $(shell grep -m 1 "version =" pyproject.toml | cut -d '"' -f 2)
IMAGE_NAME := rest-api

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

docker-run:
	docker run -p 5000:5000 --env-file .env $(IMAGE_NAME):$(VERSION)

compose-up:
	VERSION=$(VERSION) docker compose up --build -d

compose-down:
	docker compose down
