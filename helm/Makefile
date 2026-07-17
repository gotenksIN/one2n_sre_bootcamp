APP_VERSION := $(shell grep -m 1 "version =" ../pyproject.toml | cut -d '"' -f 2)
IMAGE_REF := ghcr.io/gotenksin/rest-api
IMAGE_NAME := rest-api
IMAGE := $(IMAGE_NAME):$(APP_VERSION)

RELEASE := stack
NAMESPACE := student-api
CHART := stack
SET_IMAGE := --set image.repository=$(IMAGE_NAME) --set image.tag=$(APP_VERSION)

.PHONY: repo-update deps build image-load-minikube image-load-kind lint template install wait status port-forward uninstall

repo-update:
	helm repo add hashicorp https://helm.releases.hashicorp.com
	helm repo update

deps:
	rm -f $(CHART)/charts/*.tgz $(CHART)/Chart.lock
	helm dependency update $(CHART)

build:
	docker build -t $(IMAGE) ..

image-load-minikube:
	minikube image load $(IMAGE)

image-load-kind:
	kind load docker-image $(IMAGE)

lint:
	helm lint $(CHART)

template:
	helm template $(RELEASE) $(CHART) --namespace $(NAMESPACE) $(SET_IMAGE)

install:
	helm upgrade --install $(RELEASE) $(CHART) \
		--namespace $(NAMESPACE) \
		--create-namespace \
		$(SET_IMAGE)
	kubectl rollout status deployment/$(RELEASE)-vault-agent-injector -n vault --timeout=180s
	kubectl rollout restart deployment/$(RELEASE) -n $(NAMESPACE)

wait:
	kubectl rollout status statefulset/$(RELEASE)-vault -n vault --timeout=180s
	kubectl rollout status deployment/$(RELEASE)-vault-agent-injector -n vault --timeout=180s
	kubectl rollout status statefulset/$(RELEASE)-postgresql -n $(NAMESPACE) --timeout=180s
	kubectl rollout status deployment/$(RELEASE) -n $(NAMESPACE) --timeout=180s

status:
	helm status $(RELEASE) -n $(NAMESPACE)
	kubectl get pods -n vault
	kubectl get pods,svc -n $(NAMESPACE)

port-forward:
	kubectl port-forward -n $(NAMESPACE) svc/$(RELEASE) 5000:5000

uninstall:
	helm uninstall $(RELEASE) -n $(NAMESPACE) --ignore-not-found
