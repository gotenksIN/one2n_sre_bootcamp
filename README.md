# Student REST API

Flask API backed by PostgreSQL in Docker Compose or SQLite for local
development. The root `Makefile` owns application development, testing, image
builds, and the local Compose stack.

## Requirements

- Docker with Compose
- `uv`
- Python 3.14, installed by `uv` when required

## Configuration

```bash
cp .env.example .env
cp .env.test.example .env.test
```

`.env` configures the Compose stack. `.env.test` configures the isolated test
database on port `5433`.

## Architecture

The root Makefile supports three execution paths:

| Path | Flow |
|---|---|
| Local | Flask -> SQLite `dev.db` |
| Compose | PostgreSQL -> one-shot migration -> Flask API on port `5000` |
| Test | Temporary PostgreSQL -> migration -> pytest -> teardown |

The image version comes from `pyproject.toml`. `openapi.json` is generated from
the application and is the canonical API client and testing artifact.

## Run

Containerized development:

```bash
make run
make logs
```

Local development without Dockerized PostgreSQL:

```bash
make local-setup
make local-run
```

Run PostgreSQL and the API separately when debugging startup:

```bash
make db-up
make migrate
make api-up
```

## Quality Checks

```bash
make test
make lint
make openapi
```

`make test` recreates the test database and removes it after pytest exits.
`make openapi` regenerates `openapi.json` using the project version.

## Targets

| Target | Purpose |
|---|---|
| `build` | Build `rest-api:<version>` |
| `db-up` | Start PostgreSQL |
| `api-up` | Start the API after its Compose dependencies |
| `run` | Build and start the full Compose stack |
| `migrate` | Run the migration service once |
| `logs` | Follow Compose logs |
| `down` | Stop containers |
| `clean` | Stop containers and delete volumes |
| `local-setup` | Install dependencies and migrate SQLite |
| `local-run` | Run Flask against SQLite |
| `test` | Run pytest against temporary PostgreSQL |
| `lint`, `ruffcheck` | Run Ruff |
| `openapi` | Regenerate `openapi.json` |
| `ci-setup` | Install Python 3.14 and frozen dependencies |
| `ci-build` | Build and push `IMAGE_REF:IMAGE_TAG` |

## Deployment Documentation

- [Raw Kubernetes manifests](k8s/README.md)
- [Helm deployment](helm/README.md)
- [ArgoCD GitOps deployment](argocd/README.md)
- [Vagrant environment](vagrant/README.md)
- [Database migrations](migrations/README)
