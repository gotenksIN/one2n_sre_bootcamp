# Kubernetes

Deploys the API stack with raw Kubernetes manifests.

## Prerequisites

- `kubectl`
- Docker
- `curl`
- `envsubst`
- Minikube or kind

## Layout

- `vault.yml` - Vault in the `vault` namespace
- `external-secrets.yml` - External Secrets resources in `student-api`
- `database.yml` - PostgreSQL in `student-api`
- `application.yml` - Flask API in `student-api`

Vault runs in dev mode for this exercise.

## Setup

From the `k8s/` directory:

```bash
make build
make image-load-minikube
```

For kind:

```bash
make image-load-kind
```

Install dependencies and seed Vault:

```bash
make eso-install
make vault
make bootstrap
```

## Deploy

```bash
make deploy
make wait
```

The API waits for PostgreSQL and runs migrations before the Flask container starts.

## Access API

```bash
curl http://$(minikube ip):30080/health
```

Or use port forwarding:

```bash
make port-forward
curl http://127.0.0.1:5000/health
```

Expected response:

```json
{"status":"healthy"}
```

## Commands

```bash
make status  # Show stack status
make delete  # Remove stack manifests
```

Useful checks:

```bash
kubectl logs -n student-api deployment/student-api
kubectl logs -n student-api statefulset/postgres
kubectl describe externalsecret -n student-api student-api-secret
```

## Node Labels

```bash
kubectl label node <application-node> student-api/node-role=application --overwrite
kubectl label node <database-node> student-api/node-role=database --overwrite
kubectl label node <dependent-services-node> student-api/node-role=dependent-services --overwrite
```
