# Observability Chart

Deploys Prometheus, Grafana, Loki, Alloy, Blackbox Exporter, PostgreSQL
Exporter, Alertmanager, dashboards, and alert rules in the `observability`
namespace.

Requires External Secrets Operator, Vault, and a node labeled
`type=dependent_services`.

## RED vs USE Metrics

- **RED** (Rate, Errors, Duration): Application-level metrics exposed by
  `prometheus-flask-exporter` at `/metrics`. Covers request rate, error count,
  and latency percentiles.
- **USE** (Utilization, Saturation, Errors): Infrastructure-level metrics from
  Node Exporter and kube-state-metrics. Covers CPU, memory, disk, network, and
  Kubernetes object state.

## Dashboards

Four project dashboards and the chart's bundled Node Exporter dashboard are
provisioned automatically via ConfigMaps:

| Dashboard | UID | Data Source |
|---|---|---|
| Student API - Database | `student-api-database` | Prometheus |
| Student API - Application Errors | `student-api-application-errors` | Loki |
| Node Exporter / Nodes | `7d57716318ee0dddbac5a7f451fb7753` | Prometheus |
| Student API - Kubernetes State | `student-api-kubernetes-state` | Prometheus |
| Student API - Blackbox | `student-api-blackbox` | Prometheus |

Project dashboards are stored as JSON in `helm/observability/dashboards/` and
packaged into ConfigMaps labeled `grafana_dashboard: "1"`. The Node Exporter
dashboard is supplied by kube-prometheus-stack. The Grafana sidecar loads all
of them automatically. UI edits are not persisted — export changes back to
Git using **Share > Export > Export for sharing externally**.

## Alerts

Ten alert rules are configured in three groups:

| Group | Alerts |
|---|---|
| infrastructure | HighNodeCPUUsage, HighNodeDiskUsage |
| api-red | HighAPIErrorRate, HighAPIP90Latency, HighAPIP95Latency, HighAPIP99Latency, HighAPIRequestRate |
| component-restarts | PostgreSQLRestarted, VaultServerRestarted, ArgoCDServerRestarted |

Thresholds are in `values.yaml` under `alerts.thresholds`. Edit them there
rather than in the template.

Alertmanager routes all `warning` and `critical` alerts to Slack. Firing and
resolved messages are both delivered.

## Slack Webhook

The default Helm and ArgoCD workflows install the non-secret URL
`https://example.invalid/slack-webhook`. This keeps a fresh deployment healthy
without sending notifications anywhere.

To configure a real Slack webhook without putting it in Helm values or release
history:

1. Copy the example file:

   ```bash
   cp helm/vault/slack-webhook.local.example helm/vault/slack-webhook.local
   ```

2. Replace the example URL in `slack-webhook.local` with the real URL.

3. Deploy the stack normally, then stream the webhook directly into Vault:

   ```bash
   make -C helm install
   make -C helm set-slack-webhook
   ```

4. The Make target forces External Secrets to refresh. ExternalSecret
   `observability-alertmanager-slack` syncs the value into
   Kubernetes Secret `alertmanager-slack-webhook`, which Alertmanager mounts
   at `/etc/alertmanager/secrets/alertmanager-slack-webhook/url`.

Verify the secret exists (without decoding it):

```bash
kubectl get secret alertmanager-slack-webhook -n observability
kubectl get externalsecret observability-alertmanager-slack -n observability
```

Confirm no real webhook is tracked:

```bash
git grep 'hooks\.slack\.com/services/' -- ':!helm/vault/slack-webhook.local.example'
```

## Deploy

```bash
make -C helm deps
make -C helm lint
make -C helm install
make -C helm wait
```

Use either Helm or ArgoCD ownership, never both concurrently.

## Access

```bash
make -C helm port-forward-grafana        # http://localhost:3000
make -C helm port-forward-prometheus     # http://localhost:9090
make -C helm port-forward-alertmanager   # http://localhost:9093
```

Prometheus targets at <http://localhost:9090/targets>. Rules at
<http://localhost:9090/rules>. Alerts at <http://localhost:9090/alerts>.

## Verify

```bash
make -C helm status
kubectl get servicemonitor,prometheusrule,alertmanager -n observability
kubectl get externalsecret -n observability
```

All Prometheus targets must be UP. Rule evaluation must show no errors.

## Synthetic Slack Test

Port-forward Alertmanager, then submit a synthetic firing alert:

```bash
kubectl port-forward -n observability svc/observability-kube-prometh-alertmanager 9093:9093
STARTS_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
curl -fsS -X POST http://localhost:9093/api/v2/alerts \
  -H 'Content-Type: application/json' \
  --data-binary "[{
    \"labels\": {
      \"alertname\": \"Milestone11SlackTest\",
      \"severity\": \"warning\",
      \"namespace\": \"observability\",
      \"category\": \"test\"
    },
    \"annotations\": {
      \"summary\": \"Milestone 11 Slack delivery test\",
      \"description\": \"Synthetic alert proving Alertmanager can deliver a descriptive Slack message.\"
    },
    \"startsAt\": \"$STARTS_AT\",
    \"generatorURL\": \"http://localhost:9090/alerts\"
  }]"
```

Resolve it with an `endsAt` in the past:

```bash
ENDS_AT=$(date -u -d '-1 minute' +%Y-%m-%dT%H:%M:%SZ)
curl -fsS -X POST http://localhost:9093/api/v2/alerts \
  -H 'Content-Type: application/json' \
  --data-binary "[{
    \"labels\": {
      \"alertname\": \"Milestone11SlackTest\",
      \"severity\": \"warning\",
      \"namespace\": \"observability\",
      \"category\": \"test\"
    },
    \"annotations\": {
      \"summary\": \"Milestone 11 Slack delivery test\",
      \"description\": \"Synthetic alert proving Alertmanager can deliver a descriptive Slack message.\"
    },
    \"startsAt\": \"$STARTS_AT\",
    \"endsAt\": \"$ENDS_AT\",
    \"generatorURL\": \"http://localhost:9090/alerts\"
  }]"
```

## Safe Testing Warnings

- Do **not** restart Vault or PostgreSQL merely to test restart alerts.
- Do **not** fill a disk to test the disk-usage alert.
- Temporarily lower a threshold in `values.yaml` (e.g. `apiRequestRatePerSecond`)
  to safely trigger a real Prometheus rule, then restore the original value.
