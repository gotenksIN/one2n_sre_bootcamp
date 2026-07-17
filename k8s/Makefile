.PHONY: build image-load-minikube image-load-kind eso-install vault bootstrap deploy wait status port-forward delete

IMAGE_NAME := rest-api
VERSION := $(shell grep -m 1 "version =" ../pyproject.toml | cut -d '"' -f 2)
IMAGE := $(IMAGE_NAME):$(VERSION)

APP_NS := student-api
VAULT_NS := vault
ESO_NS := default

ESO_VERSION := v2.7.0
ESO_MANIFEST := https://github.com/external-secrets/external-secrets/releases/download/$(ESO_VERSION)/external-secrets.yaml
ESO_DEPLOYMENTS := external-secrets external-secrets-webhook external-secrets-cert-controller

DEPENDENT_SERVICES_AFFINITY := '{"spec":{"template":{"spec":{"affinity":{"nodeAffinity":{"preferredDuringSchedulingIgnoredDuringExecution":[{"weight":100,"preference":{"matchExpressions":[{"key":"type","operator":"In","values":["dependent_services"]}]}}]}}}}}}'

build:
	docker build -t $(IMAGE) ..

image-load-minikube:
	minikube image load $(IMAGE)

image-load-kind:
	kind load docker-image $(IMAGE)

eso-install:
	curl -L $(ESO_MANIFEST) \
		| kubectl apply --server-side -f -
	kubectl patch deployment \
		$(ESO_DEPLOYMENTS) \
		-n $(ESO_NS) \
		--type=merge \
		-p $(DEPENDENT_SERVICES_AFFINITY)
	for deployment in $(ESO_DEPLOYMENTS); do \
		kubectl wait \
			--for=condition=Available \
			deployment/$$deployment \
			-n $(ESO_NS) \
			--timeout=120s; \
	done

vault:
	kubectl apply -f vault.yml
	kubectl wait \
		--for=condition=Available \
		deployment/vault \
		-n $(VAULT_NS) \
		--timeout=120s

bootstrap:
	kubectl exec \
		-n $(VAULT_NS) \
		deploy/vault \
		-- sh -c ' \
			export VAULT_ADDR=http://127.0.0.1:8200; \
			export VAULT_TOKEN=root; \
			vault secrets enable -path=secret kv-v2 2>/dev/null || true; \
			vault kv put secret/student-api \
				postgres-password=change-me \
				secret-key=change-me; \
			printf "%s\n" \
				"path \"secret/data/student-api\" {" \
				"  capabilities = [\"read\"]" \
				"}" \
				> /tmp/student-api-policy.hcl; \
			vault policy write student-api /tmp/student-api-policy.hcl; \
			vault auth enable kubernetes 2>/dev/null || true; \
			vault write auth/kubernetes/config \
				kubernetes_host="https://$$KUBERNETES_SERVICE_HOST:$$KUBERNETES_SERVICE_PORT"; \
			vault write auth/kubernetes/role/student-api \
				bound_service_account_names=external-secrets-vault \
				bound_service_account_namespaces=$(APP_NS) \
				policies=student-api \
				audience=vault \
				ttl=1h'

deploy:
	kubectl apply -f external-secrets.yml
	kubectl apply -f database.yml
	IMAGE=$(IMAGE) \
		envsubst '$$IMAGE' < application.yml \
		| kubectl apply -f -

wait:
	kubectl wait \
		--for=condition=Ready \
		secretstore/vault-secret-store \
		-n $(APP_NS) \
		--timeout=120s
	for secret in postgres-secret student-api-secret; do \
		kubectl wait \
			--for=condition=Ready \
			externalsecret/$$secret \
			-n $(APP_NS) \
			--timeout=120s; \
	done
	kubectl rollout status \
		statefulset/postgres \
		-n $(APP_NS) \
		--timeout=120s
	kubectl rollout status \
		deployment/student-api \
		-n $(APP_NS) \
		--timeout=120s

status:
	kubectl get pods,svc,externalsecret,secretstore -n $(APP_NS)
	kubectl get pods,svc -n $(VAULT_NS)
	kubectl get pods -n $(ESO_NS)

port-forward:
	kubectl port-forward -n $(APP_NS) svc/student-api 5000:5000

delete:
	IMAGE=$(IMAGE) \
		envsubst '$$IMAGE' < application.yml \
		| kubectl delete -f - --ignore-not-found=true
	kubectl delete -f database.yml --ignore-not-found=true
	kubectl delete -f external-secrets.yml --ignore-not-found=true
	kubectl delete -f vault.yml --ignore-not-found=true
