# Observability Chart

Deploys Prometheus, Grafana, Loki, Alloy, Blackbox Exporter, and PostgreSQL
Exporter in the `observability` namespace.

Requires External Secrets Operator, Vault, and a node labeled
`type=dependent_services`.

## Deploy

```bash
make -C helm deps
make -C helm lint
make -C helm install
make -C helm wait
```

Use either Helm or ArgoCD, not both. Vault provides credentials through
External Secrets.

## Verify

```bash
make -C helm status
make -C helm port-forward-prometheus
make -C helm port-forward-grafana
```

Prometheus targets must be UP. Query API logs in Loki with:

```logql
{namespace="student-api", container="stack"}
```

Loki retains logs for seven days on persistent storage.
