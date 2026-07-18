TIMEOUT ?= 5m

.PHONY: install deploy wait status port-forward uninstall

install:
	kubectl apply --server-side -k install
	kubectl wait --for=condition=Available deployment --all -n argocd --timeout=$(TIMEOUT)
	kubectl rollout status statefulset/argocd-application-controller -n argocd --timeout=$(TIMEOUT)

deploy: install
	kubectl apply -f bootstrap.yaml
	$(MAKE) wait

wait:
	kubectl wait --for=jsonpath='{.status.sync.status}'=Synced application/bootcamp -n argocd --timeout=$(TIMEOUT)
	kubectl wait --for=jsonpath='{.status.health.status}'=Healthy application/bootcamp -n argocd --timeout=$(TIMEOUT)
	kubectl wait --for=jsonpath='{.status.sync.status}'=Synced applications --all -n argocd --timeout=$(TIMEOUT)
	kubectl wait --for=jsonpath='{.status.health.status}'=Healthy applications --all -n argocd --timeout=$(TIMEOUT)

status:
	kubectl get applications -n argocd
	kubectl get pods -n argocd -o wide

port-forward:
	kubectl port-forward -n argocd svc/argocd-server 8080:443

uninstall:
	kubectl delete -f bootstrap.yaml --ignore-not-found=true
	kubectl delete -k install --ignore-not-found=true
