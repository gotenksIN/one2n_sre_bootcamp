# Helm

Deploys the API, PostgreSQL, Vault, and External Secrets Operator using Helm.

## Prerequisites

- Docker
- Helm
- kubectl
- Minikube

Create the three-node cluster:

```bash
make -C k8s cluster
```

## Charts

- `external-secrets/` - External Secrets Operator and CRDs
- `vault/` - development Vault server and bootstrap job
- `stack/` - PostgreSQL, API, and ExternalSecret resources

Vault uses development mode and the demo credentials in
`vault/values-demo.yaml`.

## Setup

```bash
make -C helm repo-update
make -C helm deps
make -C helm build
make -C helm image-load-minikube
```

## Deploy

```bash
make -C helm lint
make -C helm install
make -C helm wait
```

Releases are installed in dependency order:

1. `external-secrets` in `external-secrets`
2. `vault` in `vault`
3. `stack` in `student-api`

## Verify

```bash
make -C helm status
curl http://$(minikube ip):30080/health
curl http://$(minikube ip):30080/readyz
```

Expected responses:

```json
{"status":"healthy"}
{"status":"ready"}
```

## Commands

```bash
make -C helm template       # Render all charts
make -C helm port-forward   # Forward API to 127.0.0.1:5000
make -C helm uninstall      # Remove all releases
```

PostgreSQL PVCs remain after uninstall. Do not use direct Helm deployment on a
cluster where ArgoCD manages these releases.
