# Raw Kubernetes Deployment

The `k8s/Makefile` deploys the API with raw manifests. This path is useful for
understanding the resources before introducing Helm or ArgoCD.

[Back to the project README](../README.md)

## Architecture

| Namespace | Components |
|---|---|
| `default` | External Secrets Operator |
| `vault` | Development Vault server |
| `student-api` | PostgreSQL, Flask API, SecretStore, ExternalSecrets |

Vault stores the PostgreSQL password and Flask secret. External Secrets
Operator writes them to Kubernetes Secrets. PostgreSQL must become ready before
the API migration and application containers can start.

The Minikube target creates three nodes and assigns workload labels:

| Node | Label |
|---|---|
| `minikube` | `type=application` |
| `minikube-m02` | `type=database` |
| `minikube-m03` | `type=dependent_services` |

## Requirements

- Docker
- Minikube with the `kvm2` driver, unless overridden
- `kubectl`, `curl`, and `envsubst`

## Run Order

Create the cluster and load the local image:

```bash
make -C k8s cluster
make -C k8s build
make -C k8s image-load-minikube
```

For kind, use `make -C k8s image-load-kind` instead of the Minikube image-load
target. The `cluster` target itself is Minikube-specific.

Configure secrets, then install dependencies in order:

```bash
cp k8s/.env.example k8s/.env
make -C k8s eso-install
make -C k8s vault
make -C k8s bootstrap
```

Deploy and wait for secret synchronization, PostgreSQL, and the API:

```bash
make -C k8s deploy
make -C k8s wait
make -C k8s status
```

Access the API with `make -C k8s port-forward`, then use
`http://127.0.0.1:5000`.

## Targets

| Target | Purpose |
|---|---|
| `cluster` | Create and label a three-node Minikube cluster |
| `label-nodes` | Reapply workload labels |
| `build` | Build the local API image |
| `image-load-minikube` | Load the image into Minikube |
| `image-load-kind` | Load the image into kind |
| `eso-install` | Install External Secrets Operator |
| `vault` | Deploy development Vault |
| `bootstrap` | Seed Vault and configure Kubernetes auth |
| `deploy` | Apply database, secret, and API manifests |
| `wait` | Wait for secrets and workloads |
| `status` | Show deployed resources |
| `port-forward` | Forward the API to port `5000` |
| `delete` | Delete application and Vault manifests |

Do not combine this deployment path with Helm or ArgoCD ownership on the same
cluster.
