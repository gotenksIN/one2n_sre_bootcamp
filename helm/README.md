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

- `student-api` - API and PostgreSQL
- `vault` - Vault and Vault Agent injector

## Local Secrets

The committed `values.yaml` sets sensitive fields to empty values. Provide
them via a local values file before deploying:

```bash
cp stack/values-local.yaml.example stack/values-local.yaml
# edit stack/values-local.yaml with your dev secrets
```

The Makefile automatically includes `values-local.yaml` when it exists.

For production use, External Secrets Operator or Vault should supply runtime
secrets rather than static values files.

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
make lint      # Lint the chart
make template  # Render manifests
make status    # Show release and pod status
make uninstall # Remove the release
```
