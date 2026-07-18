APP_VERSION := $(shell grep -m 1 "version =" ../pyproject.toml | cut -d '"' -f 2)
IMAGE_NAME := rest-api
IMAGE := $(IMAGE_NAME):$(APP_VERSION)
TIMEOUT ?= 5m

ESO_RELEASE := external-secrets
ESO_NAMESPACE := external-secrets
VAULT_RELEASE := vault
VAULT_NAMESPACE := vault
STACK_RELEASE := stack
STACK_NAMESPACE := student-api
OBSERVABILITY_RELEASE := observability
OBSERVABILITY_NAMESPACE := observability

STACK_VALUES := --values stack/values.yaml --values stack/values-image.yaml
LOCAL_IMAGE := --set image.repository=$(IMAGE_NAME) --set image.tag=$(APP_VERSION) --set image.pullPolicy=IfNotPresent

.PHONY: repo-update deps build image-load-minikube image-load-kind lint template install wait status port-forward port-forward-grafana port-forward-prometheus uninstall

repo-update:
	helm repo add external-secrets https://charts.external-secrets.io --force-update
	helm repo add grafana https://grafana.github.io/helm-charts --force-update
	helm repo add grafana-community https://grafana-community.github.io/helm-charts --force-update
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts --force-update
	helm repo update

deps:
	helm dependency build external-secrets
	helm dependency build observability

build:
	docker build -t $(IMAGE) ..

image-load-minikube:
	minikube image load $(IMAGE)

image-load-kind:
	kind load docker-image $(IMAGE)

lint:
	helm lint external-secrets
	helm lint vault --values vault/values-demo.yaml
	helm lint stack $(STACK_VALUES)
	helm lint observability

template:
	helm template $(ESO_RELEASE) external-secrets --namespace $(ESO_NAMESPACE)
	helm template $(VAULT_RELEASE) vault --namespace $(VAULT_NAMESPACE) --values vault/values-demo.yaml
	helm template $(STACK_RELEASE) stack --namespace $(STACK_NAMESPACE) $(STACK_VALUES) $(LOCAL_IMAGE)
	helm template $(OBSERVABILITY_RELEASE) observability --namespace $(OBSERVABILITY_NAMESPACE) --include-crds

install:
	helm upgrade --install $(ESO_RELEASE) external-secrets \
		--namespace $(ESO_NAMESPACE) \
		--create-namespace \
		--rollback-on-failure \
		--wait \
		--timeout $(TIMEOUT)
	helm upgrade --install $(VAULT_RELEASE) vault \
		--namespace $(VAULT_NAMESPACE) \
		--create-namespace \
		--values vault/values-demo.yaml \
		--rollback-on-failure \
		--wait \
		--wait-for-jobs \
		--timeout $(TIMEOUT)
	helm upgrade --install $(STACK_RELEASE) stack \
		--namespace $(STACK_NAMESPACE) \
		--create-namespace \
		$(STACK_VALUES) \
		$(LOCAL_IMAGE) \
		--rollback-on-failure \
		--wait \
		--timeout $(TIMEOUT)
	helm upgrade --install $(OBSERVABILITY_RELEASE) observability \
		--namespace $(OBSERVABILITY_NAMESPACE) \
		--create-namespace \
		--rollback-on-failure \
		--wait \
		--wait-for-jobs \
		--timeout $(TIMEOUT)

wait:
	kubectl wait --for=condition=Available deployment --all -n $(ESO_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl wait --for=condition=Available deployment/$(VAULT_RELEASE) -n $(VAULT_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl wait --for=condition=Ready secretstore/vault -n $(STACK_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl wait --for=condition=Ready externalsecret --all -n $(STACK_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl rollout status statefulset/$(STACK_RELEASE)-postgresql -n $(STACK_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl rollout status deployment/$(STACK_RELEASE) -n $(STACK_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl wait --for=condition=Ready secretstore/vault -n $(OBSERVABILITY_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl wait --for=condition=Ready externalsecret --all -n $(OBSERVABILITY_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl wait --for=condition=Complete job -l app.kubernetes.io/component=pg-monitor-bootstrap -n $(OBSERVABILITY_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl wait --for=condition=Available deployment --all -n $(OBSERVABILITY_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl rollout status statefulset/$(OBSERVABILITY_RELEASE)-loki -n $(OBSERVABILITY_NAMESPACE) --timeout=$(TIMEOUT)
	kubectl wait --for=condition=Available prometheus/$(OBSERVABILITY_RELEASE)-kube-prometh-prometheus -n $(OBSERVABILITY_NAMESPACE) --timeout=$(TIMEOUT)

status:
	helm list --all-namespaces
	kubectl get pods -n $(ESO_NAMESPACE)
	kubectl get pods -n $(VAULT_NAMESPACE)
	kubectl get pods,svc,externalsecret,secretstore -n $(STACK_NAMESPACE)
	kubectl get pods,svc,pvc,externalsecret,secretstore -n $(OBSERVABILITY_NAMESPACE)
	kubectl get servicemonitor -n $(OBSERVABILITY_NAMESPACE)

port-forward:
	kubectl port-forward -n $(STACK_NAMESPACE) svc/$(STACK_RELEASE) 5000:5000

port-forward-grafana:
	kubectl port-forward -n $(OBSERVABILITY_NAMESPACE) svc/$(OBSERVABILITY_RELEASE)-grafana 3000:80

port-forward-prometheus:
	kubectl port-forward -n $(OBSERVABILITY_NAMESPACE) svc/$(OBSERVABILITY_RELEASE)-kube-prometh-prometheus 9090:9090

uninstall:
	helm uninstall $(OBSERVABILITY_RELEASE) -n $(OBSERVABILITY_NAMESPACE) --ignore-not-found
	helm uninstall $(STACK_RELEASE) -n $(STACK_NAMESPACE) --ignore-not-found
	helm uninstall $(VAULT_RELEASE) -n $(VAULT_NAMESPACE) --ignore-not-found
	helm uninstall $(ESO_RELEASE) -n $(ESO_NAMESPACE) --ignore-not-found
