# Observability Chart

The `helm/observability/Makefile` manages the metrics, logs, dashboards, and
alerting release in the `observability` namespace.

[Back to the Helm README](../README.md) | [Back to the project README](../../README.md)

## Architecture

| Signal | Flow |
|---|---|
| API metrics | Flask `/metrics` -> ServiceMonitor -> Prometheus -> Grafana |
| Database metrics | PostgreSQL -> PostgreSQL Exporter -> Prometheus -> Grafana |
| Cluster metrics | Node Exporter and kube-state-metrics -> Prometheus -> Grafana |
| Probe metrics | Blackbox Exporter -> Prometheus -> Grafana |
| Application logs | Kubernetes pod logs -> Alloy -> Loki -> Grafana |
| Alerts | PrometheusRule -> Alertmanager -> Slack |

`kube-prometheus-stack` supplies Prometheus, Alertmanager, Grafana, Node
Exporter, and kube-state-metrics. Separate chart dependencies supply Loki,
Alloy, Blackbox Exporter, and PostgreSQL Exporter. Grafana discovers dashboards
from labeled ConfigMaps and uses provisioned Prometheus and Loki data sources.

Alloy replaces end-of-life Promtail as the Kubernetes log collector.

## Dependencies

This chart expects the following resources to exist before installation:

- External Secrets Operator and its CRDs
- Vault with the `observability` secret and Kubernetes auth role
- The API and PostgreSQL release in `student-api`
- A node labeled `type=dependent_services`

For a complete deployment, use the ordered workflow in the
[parent Helm README](../README.md). Running this chart alone is intended for
observability-only development after those dependencies exist.

## Run Order

```bash
make -C helm/observability deps
make -C helm/observability lint
make -C helm/observability template
make -C helm/observability install
make -C helm/observability wait
make -C helm/observability status
```

Use `deps-update` only when intentionally changing dependency versions;
`deps` builds the versions pinned in `Chart.lock`.

## Dashboards

| Dashboard | UID | Source |
|---|---|---|
| Student API - Database | `student-api-database` | Prometheus |
| Student API - Application Errors | `student-api-application-errors` | Loki |
| Node Exporter / Nodes | `7d57716318ee0dddbac5a7f451fb7753` | Prometheus |
| Student API - Kubernetes State | `student-api-kubernetes-state` | Prometheus |
| Student API - Blackbox | `student-api-blackbox` | Prometheus |

Project dashboard JSON is stored in `dashboards/`. The Node Exporter dashboard
comes from kube-prometheus-stack. UI edits are not durable; export intended
changes back to JSON.

## Alerts

Ten rules are grouped by signal:

| Group | Rules |
|---|---|
| `infrastructure` | High node CPU and disk usage |
| `api-red` | Error rate, p90/p95/p99 latency, and request rate |
| `component-restarts` | PostgreSQL, Vault, and ArgoCD server restarts |

Thresholds and the evaluation window are configured under `alerts` in
`values.yaml`. Alertmanager routes `warning` and `critical` alerts to Slack and
sends resolved notifications.

## Slack Webhook

The default deployment uses `https://example.invalid/slack-webhook`. This keeps
Alertmanager healthy without delivering notifications or storing a real
webhook in Helm release history.

Inject a real webhook directly into Vault after the full stack is installed:

```bash
cp helm/vault/slack-webhook.local.example helm/vault/slack-webhook.local
make -C helm set-slack-webhook
```

The ignored local file is streamed through `kubectl exec`; it is not passed as
a Helm value. The target then forces External Secrets to refresh
`alertmanager-slack-webhook`.

Verify synchronization without decoding the Secret:

```bash
kubectl get externalsecret observability-alertmanager-slack -n observability
kubectl get secret alertmanager-slack-webhook -n observability
```

## Access

```bash
make -C helm/observability port-forward-grafana
make -C helm/observability port-forward-prometheus
make -C helm/observability port-forward-alertmanager
```

| Service | Local URL |
|---|---|
| Grafana | `http://127.0.0.1:3000` |
| Prometheus | `http://127.0.0.1:9090` |
| Alertmanager | `http://127.0.0.1:9093` |

Prometheus targets and rules must report healthy before alert testing. Do not
restart stateful services or fill a disk to force alerts; temporarily lower a
threshold when a controlled rule test is required.

## Targets

| Target | Purpose |
|---|---|
| `deps` | Build pinned chart dependencies |
| `deps-update` | Resolve and update dependency versions |
| `lint` | Lint the chart |
| `template` | Render the chart with CRDs |
| `install` | Install or upgrade the observability release |
| `wait` | Wait for bootstrap jobs and workloads |
| `status` | Show the release and monitored resources |
| `port-forward-grafana` | Forward Grafana to port `3000` |
| `port-forward-prometheus` | Forward Prometheus to port `9090` |
| `port-forward-alertmanager` | Forward Alertmanager to port `9093` |
| `uninstall` | Remove the observability release |
