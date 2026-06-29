# Student REST API

A lightweight REST API for managing student records built with Flask, Flask-SQLAlchemy, and SQLite.

## Prerequisites

- **Python 3.14+**
- **uv** (Python package manager)

## Quick Start

1. **Configure Environment**
   ```bash
   cp .env.example .env
   ```

2. **Setup and Run**
   ```bash
   uv sync
   make migrate
   make run
   ```
   The server will start on `http://127.0.0.1:5000`.

## API Endpoints

- `GET /api/v1/healthcheck` — Health status
- `GET /api/v1/students` — List all students
- `POST /api/v1/students` — Create a student
- `GET /api/v1/students/<id>` — Retrieve a student
- `PUT /api/v1/students/<id>` — Update a student
- `DELETE /api/v1/students/<id>` — Delete a student

## Development

```bash
make test  # Run tests (pytest)
make lint  # Run lint checks (ruff)
```

## Docker

### Build and Run with Makefile

Build and run the containerized API using the semver-tagged version from `pyproject.toml`:

```bash
make docker-build
make docker-run
```

The container automatically runs database migrations on startup and will be accessible at `http://127.0.0.1:5000`.
