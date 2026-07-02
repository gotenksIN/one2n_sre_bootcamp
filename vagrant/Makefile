.PHONY: build up down status logs clean

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

status:
	docker compose ps

logs:
	docker compose logs -f

clean:
	docker compose down -v
	docker system prune -f
