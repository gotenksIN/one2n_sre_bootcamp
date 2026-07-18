RELEASE := observability
NAMESPACE := observability
CHART := .

.PHONY: deps deps-update lint template install wait status port-forward-grafana port-forward-prometheus port-forward-alertmanager uninstall

deps:
	helm dependency build $(CHART)

deps-update:
	helm dependency update $(CHART)

lint:
	helm lint $(CHART)

template:
	helm template $(RELEASE) $(CHART) --namespace $(NAMESPACE) --include-crds

install:
	helm upgrade --install $(RELEASE) $(CHART) \
		--namespace $(NAMESPACE) \
		--create-namespace \
		--rollback-on-failure \
		--wait \
		--wait-for-jobs \
		--timeout 5m

wait:
	kubectl wait --for=condition=Complete job -l app.kubernetes.io/component=pg-monitor-bootstrap -n $(NAMESPACE) --timeout=300s
	kubectl wait --for=condition=Available deployment --all -n $(NAMESPACE) --timeout=300s
	kubectl wait --for=create statefulset/$(RELEASE)-loki -n $(NAMESPACE) --timeout=300s
	kubectl rollout status statefulset/$(RELEASE)-loki -n $(NAMESPACE) --timeout=300s
	kubectl wait --for=condition=Available prometheus/$(RELEASE)-kube-prometh-prometheus -n $(NAMESPACE) --timeout=300s
	kubectl wait --for=condition=Available alertmanager/$(RELEASE)-kube-prometh-alertmanager -n $(NAMESPACE) --timeout=300s

status:
	helm status $(RELEASE) -n $(NAMESPACE)
	@echo ""
	@echo "Pods:"
	kubectl get pods -n $(NAMESPACE) -o wide
	@echo ""
	@echo "Services:"
	kubectl get svc -n $(NAMESPACE)
	@echo ""
	@echo "PVCs:"
	kubectl get pvc -n $(NAMESPACE)
	@echo ""
	@echo "ServiceMonitors:"
	kubectl get servicemonitors -n $(NAMESPACE)
	@echo ""
	@echo "Alertmanager:"
	kubectl get alertmanager -n $(NAMESPACE)
	@echo ""
	@echo "PrometheusRules:"
	kubectl get prometheusrules -n $(NAMESPACE)

port-forward-grafana:
	kubectl port-forward -n $(NAMESPACE) svc/$(RELEASE)-grafana 3000:80

port-forward-prometheus:
	kubectl port-forward -n $(NAMESPACE) svc/$(RELEASE)-kube-prometh-prometheus 9090:9090

port-forward-alertmanager:
	kubectl port-forward -n $(NAMESPACE) svc/$(RELEASE)-kube-prometh-alertmanager 9093:9093

uninstall:
	helm uninstall $(RELEASE) -n $(NAMESPACE) --ignore-not-found
