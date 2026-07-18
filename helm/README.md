# Helm Deployment

The `helm/Makefile` builds and deploys the complete Kubernetes stack in a fixed
dependency order.

[Back to the project README](../README.md)

## Architecture

| Order | Release | Namespace | Responsibility |
|---|---|---|---|
| 1 | `external-secrets` | `external-secrets` | External Secrets Operator and CRDs |
| 2 | `vault` | `vault` | Development Vault and secret bootstrap |
| 3 | `stack` | `student-api` | PostgreSQL, migrations, and Flask API |
| 4 | `observability` | `observability` | Metrics, logs, dashboards, and alerts |

The stack chart reads application credentials through External Secrets. The
observability chart depends on both the running application and credentials
seeded by Vault. The default `vault/values-demo.yaml` is only for a disposable
local cluster.

See [Observability architecture and operations](observability/README.md) for
the final release in this sequence.

## Requirements

- A Kubernetes cluster with nodes labeled as described in
  [the raw Kubernetes guide](../k8s/README.md)
- Docker, Helm, and `kubectl`
- Minikube or kind for loading a local image

## Run Order

Prepare chart dependencies and the local API image:

```bash
make -C helm repo-update
make -C helm deps
make -C helm build
make -C helm image-load-minikube
```

Use `make -C helm image-load-kind` for kind.

Validate, deploy, and verify all four releases:

```bash
make -C helm lint
make -C helm template
make -C helm install
make -C helm wait
make -C helm status
```

`install` and `uninstall` use opposite release order. PersistentVolumeClaims
may remain after uninstall.

## Secrets

The default deployment uses public demo credentials and a non-delivering Slack
URL. To use local Vault values without committing them:

```bash
cp helm/vault/values-local.example.yaml helm/vault/values-local.yaml
make -C helm install VAULT_VALUES=vault/values-local.yaml
```

Real Slack webhook handling is documented in the
[observability README](observability/README.md#slack-webhook).

## Targets

| Target | Purpose |
|---|---|
| `repo-update` | Configure and refresh chart repositories |
| `deps` | Build chart dependencies |
| `build` | Build the versioned API image |
| `image-load-minikube` | Load the image into Minikube |
| `image-load-kind` | Load the image into kind |
| `lint` | Lint all local charts |
| `template` | Render all releases without installing |
| `install` | Install or upgrade the full stack |
| `set-slack-webhook` | Stream an ignored local webhook file into Vault |
| `wait` | Wait for secrets, jobs, and workloads |
| `status` | Show releases and Kubernetes resources |
| `port-forward` | Forward the API to port `5000` |
| `port-forward-grafana` | Forward Grafana to port `3000` |
| `port-forward-prometheus` | Forward Prometheus to port `9090` |
| `port-forward-alertmanager` | Forward Alertmanager to port `9093` |
| `uninstall` | Remove all four releases |

Use either direct Helm ownership or
[ArgoCD ownership](../argocd/README.md), never both on the same cluster.
