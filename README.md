# Student REST API

A lightweight REST API for managing student records built with Flask, Flask-SQLAlchemy, and PostgreSQL.

## Prerequisites

- **Docker**
- **Docker Compose**
- **Python 3.14+** and **uv** for tests/linting

## Quick Start

1. **Configure Environment**
   ```bash
   cp .env.example .env
   cp .env.test.example .env.test
   ```

2. **Run with Docker Compose**
   ```bash
   make run
   ```
   Compose starts PostgreSQL, runs database migrations, and starts the API at `http://127.0.0.1:5000`.

## API Endpoints

- `GET /health` — Health status (also available at `/healthcheck`)
- `GET /livez` — Liveness check
- `GET /readyz` — Readiness check (DB reachable)
- `GET /api/v1/students` — List all students
- `POST /api/v1/students` — Create a student
- `GET /api/v1/students/<id>` — Retrieve a student
- `PUT /api/v1/students/<id>` — Update a student
- `DELETE /api/v1/students/<id>` — Delete a student

`POST /api/v1/students` returns `201 Created` on success. All other
successful responses return `200 OK`.

API testing is done via the `openapi.json` spec — import it into Postman or any
OpenAPI-compatible client. The spec is generated from code, so it stays in sync
with the implementation and replaces manual Postman collections.

## Development

### Local (SQLite, no Docker)

```bash
make local-setup  # Install deps and set up SQLite database
make local-run    # Start the dev server at http://127.0.0.1:5000
```

### Tests and Lint

```bash
make test  # Run tests against Dockerized PostgreSQL
make lint  # Run lint checks (ruff)
```

## Docker

### Local Stack

Run the containerized API and PostgreSQL using the semver-tagged version from `pyproject.toml`:

```bash
make run
```

The container automatically runs database migrations on startup and will be accessible at `http://127.0.0.1:5000`.

Useful local commands:

```bash
make build    # Build the API image
make db-up    # Start PostgreSQL only
make api-up   # Start DB, run migrations, start API
make logs     # Follow logs
make migrate  # Run migrations
make down     # Stop containers
make clean    # Stop containers and remove the database volume
```
