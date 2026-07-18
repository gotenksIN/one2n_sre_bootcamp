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

### Create Cluster

```bash
make -C k8s cluster
```

Three nodes are created and automatically labeled:
- `minikube` — `type=application`
- `minikube-m02` — `type=database`
- `minikube-m03` — `type=dependent_services`

To label an existing cluster without recreating it:

```bash
make -C k8s label-nodes
```

### Build And Load Image

```bash
make -C k8s build
make -C k8s image-load-minikube
```

For kind:

```bash
make -C k8s image-load-kind
```

### Create Secrets File

```bash
cp .env.example .env
```

### Install Dependencies And Seed Vault

```bash
make -C k8s eso-install
make -C k8s vault
make -C k8s bootstrap
```

## Deploy

```bash
make -C k8s deploy
make -C k8s wait
```

The API waits for PostgreSQL and runs migrations before the Flask container starts.

## Access API

```bash
curl http://$(minikube ip):30080/health
```

Or use port forwarding:

```bash
make -C k8s port-forward
curl http://127.0.0.1:5000/health
```

Expected response:

```json
{"status":"healthy"}
```

## Commands

```bash
make -C k8s status  # Show stack status
make -C k8s delete  # Remove stack manifests
```

Useful checks:

```bash
kubectl logs -n student-api deployment/student-api
kubectl logs -n student-api statefulset/postgres
kubectl describe externalsecret -n student-api student-api-secret
```

## Node Labels

Labels are applied automatically by `make -C k8s cluster`. To re-label an
existing cluster:

```bash
make -C k8s label-nodes
```
