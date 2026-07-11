# Helm

Deploys the API stack with one Helm chart.

## Prerequisites

- `helm`
- `kubectl`
- Docker
- Minikube or kind

## Layout

- `stack/` - Flask API, PostgreSQL, Vault, and Vault bootstrap job
- `Makefile` - local build, render, deploy, and cleanup commands

Vault runs in dev mode for this exercise.

## Setup

From the `helm/` directory:

```bash
make repo-update
make deps
make build
```

Load the image into the local cluster:

```bash
make image-load-minikube
```

For kind:

```bash
make image-load-kind
```

## Deploy

```bash
make install
make wait
```

Namespaces:

- `app` - API and PostgreSQL
- `vault` - Vault and Vault Agent injector

Default local secrets are in `stack/values.yaml`:

```yaml
vaultBootstrap:
  postgresPassword: change-me
  flaskSecretKey: change-me
```

## Access API

```bash
curl http://$(minikube ip):30080/api/v1/healthcheck
```

Or use port forwarding:

```bash
make port-forward
curl http://127.0.0.1:5000/api/v1/healthcheck
```

Expected response:

```json
{"status":"healthy"}
```

## Commands

```bash
make lint      # Lint the chart
make template  # Render manifests
make status    # Show release and pod status
make uninstall # Remove the release
```
