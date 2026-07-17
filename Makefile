VERSION := $(shell grep -m 1 "version =" pyproject.toml | cut -d '"' -f 2)
COMPOSE := VERSION=$(VERSION) docker compose
TEST_COMPOSE := docker compose -p rest-test -f docker-compose.test.yml

.PHONY: build db-up api-up ci-build run down clean logs migrate test lint ruffcheck openapi

openapi:
	uv run python scripts/generate_openapi.py "$(VERSION)"

build:
	docker build -t rest-api:$(VERSION) .

ci-build:
	docker build -t $(IMAGE_REF):$(IMAGE_TAG) .
	docker push $(IMAGE_REF):$(IMAGE_TAG)

db-up:
	$(COMPOSE) up -d postgres

api-up:
	$(COMPOSE) up -d rest-api

run:
	$(COMPOSE) up --build -d

down:
	docker compose down

clean:
	docker compose down -v

logs:
	docker compose logs -f

migrate:
	$(COMPOSE) run --rm migrate

test:
	@test -f .env.test || (printf '%s\n' "Missing .env.test. Copy .env.test.example and adjust values." && exit 1)
	$(TEST_COMPOSE) down -v --remove-orphans
	$(TEST_COMPOSE) up -d --wait test-db
	uv run dotenv -f .env.test run -- flask --app app.main:app db upgrade && uv run dotenv -f .env.test run -- pytest; status=$$?; $(TEST_COMPOSE) down -v; exit $$status

lint:
	uv run ruff check .

ruffcheck: lint
