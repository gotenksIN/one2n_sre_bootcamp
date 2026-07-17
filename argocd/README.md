# ArgoCD

Installs ArgoCD and configures GitOps deployment for the Helm stack.

## Prerequisites

- `kubectl`
- Public GitHub repository
- Self-hosted GitHub Actions runner
- Nodes labeled with `type`

## Layout

- `install/` - ArgoCD control plane in the `argocd` namespace
- `apps/` - ArgoCD project and `stack` application

## Install

From the repository root:

```bash
kubectl apply -k argocd/install
kubectl rollout status deployment/argocd-server -n argocd --timeout=180s
kubectl rollout status statefulset/argocd-application-controller -n argocd --timeout=180s
```

ArgoCD pods use this node selector:

```yaml
type: dependent_services
```

## Configure Application

Make the repository public, then apply the app manifests:

```bash
kubectl apply -k argocd/apps
```

Application source:

```yaml
repoURL: https://github.com/gotenksIN/one2n_sre_bootcamp.git
targetRevision: master
path: helm/stack
```

Auto-sync, prune, and self-heal are enabled.

## Access UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d
```

Open `https://127.0.0.1:8080`.

## Verify

```bash
kubectl get pods -n argocd -o wide
kubectl get applications -n argocd
kubectl get pods -n student-api
```

## CI Flow

`.github/workflows/argocd-image-update.yml` runs on the self-hosted runner.

On push to `master`, it runs tests, builds `rest-api:<short-sha>`, pushes to
`ghcr.io/gotenksin/rest-api`, updates `helm/stack/values.yaml` image tag, and commits
the change. ArgoCD syncs from that commit.

The first push creates the GHCR package. **The package must be made public** so
Kubernetes can pull it without authentication:

```bash
gh api "/users/gotenksin/packages/container/rest-api/visibility" \
  -X PUT -H "Accept: application/vnd.github+json" \
  -f "visibility=public"
```

If the package should remain private, configure `imagePullSecrets` in
`helm/stack/values.yaml` with a Docker config JSON secret.
