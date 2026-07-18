# ArgoCD Deployment

The `argocd/Makefile` installs ArgoCD and bootstraps the Helm stack through an
app-of-apps workflow.

[Back to the project README](../README.md)

## Architecture

`bootstrap.yaml` creates the root `bootcamp` Application. It reads `argocd/apps`
from Git and creates the project and four child Applications.

| Sync wave | Application | Chart |
|---|---|---|
| `-2` | `external-secrets` | `helm/external-secrets` |
| `-1` | `vault` | `helm/vault` |
| `0` | `stack` | `helm/stack` |
| `1` | `observability` | `helm/observability` |

All Applications use automated synchronization, pruning, and self-healing.
ArgoCD reads the configured Git branch, not uncommitted local files.

See the [Helm deployment README](../helm/README.md) for release architecture
and the [observability README](../helm/observability/README.md) for dashboards,
alerts, and Slack configuration.

## Requirements

- A reachable Kubernetes cluster
- `kubectl`
- Repository changes pushed to the repository and revision configured in the
  Application manifests
- No directly installed Helm releases for the same resources

## Run Order

Install ArgoCD and deploy the root Application:

```bash
make -C argocd deploy
```

The target runs `install`, applies `bootstrap.yaml`, then waits for the root and
all child Applications to become `Synced` and `Healthy`.

Inspect the result:

```bash
make -C argocd status
```

Access the UI with `make -C argocd port-forward` at
`https://127.0.0.1:8080`.

## Targets

| Target | Purpose |
|---|---|
| `install` | Server-side apply the pinned ArgoCD installation |
| `deploy` | Install ArgoCD and apply the app-of-apps bootstrap |
| `wait` | Wait for root and child Applications |
| `status` | Show Applications and ArgoCD pods |
| `port-forward` | Forward the ArgoCD API and UI to port `8080` |
| `uninstall` | Delete the bootstrap and ArgoCD installation |

Do not run `make -C helm install` while ArgoCD owns these releases.
