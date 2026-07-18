# ArgoCD

Installs ArgoCD and deploys the application and observability stacks using
GitOps.

## Prerequisites

- kubectl
- Minikube
- Helm and ArgoCD changes pushed to the configured Git repository

Create the three-node cluster:

```bash
make -C k8s cluster
```

ArgoCD components run in `argocd` on the node labeled
`type=dependent_services`.

## Layout

- `install/` - pinned ArgoCD installation
- `bootstrap.yaml` - root Application
- `apps/` - AppProject and child Applications
- `Makefile` - install, deploy, status, and cleanup commands

## Deploy

```bash
make -C argocd deploy
```

The child Applications sync in this order:

1. External Secrets Operator
2. Vault
3. API and PostgreSQL stack
4. Observability stack

Automated sync, pruning, and self-healing are enabled.

Do not manage the observability release with Helm and ArgoCD simultaneously.

## Verify

```bash
make -C argocd status
curl http://$(minikube ip):30080/health
curl http://$(minikube ip):30080/readyz
kubectl get pods -n observability
```

## ArgoCD UI

```bash
make -C argocd port-forward
```

Open `https://127.0.0.1:8080`. Get the initial password with:

```bash
kubectl get secret argocd-initial-admin-secret -n argocd \
  -o jsonpath='{.data.password}' | base64 -d
```

## Image Updates

`.github/workflows/ci.yml` builds and pushes the commit-tagged image on the
self-hosted runner. After CI succeeds, `update-helm-image.yml` updates
`helm/stack/values-image.yaml`. ArgoCD detects the commit and syncs the stack.

## Commands

```bash
make -C argocd install       # Install ArgoCD only
make -C argocd wait          # Wait for Applications
make -C argocd status        # Show Applications and pods
make -C argocd uninstall     # Remove ArgoCD
```

Do not install the same releases directly with `make -C helm install` while
ArgoCD manages them.
