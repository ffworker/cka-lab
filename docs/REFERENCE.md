# CKA field reference

This is a compact, public reference for the commands most useful during the
build/break/fix loop. It is intentionally separate from personal learner state:
progress and observations belong in ignored `.cka-factory/learner-state.json`.

## Session workflow

1. Read the active mission and its success criteria.
2. Inspect the object chain before changing anything.
3. Break one link at a time; compare symptoms with the expected control flow.
4. Repair with normal `kubectl` commands.
5. Validate the live state, then record only useful local feedback.

For networking, trace:

```text
Ingress -> Service -> EndpointSlices -> Pods
```

For workloads, trace:

```text
Deployment -> ReplicaSet -> Pods -> containers
```

## Context and namespace

```bash
kubectl config current-context
kubectl config get-contexts
kubectl config use-context <context-name>
kubectl config set-context --current --namespace=<namespace>
kubectl config view --minify -o jsonpath='{..namespace}'
```

## Inspect before editing

```bash
kubectl get all -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --all-containers
kubectl get <kind> <name> -n <namespace> -o yaml
```

## JSONPath and compact output

```bash
kubectl get nodes -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.capacity.cpu}{"\n"}{end}'
kubectl get pods -A -o=custom-columns=NAMESPACE:.metadata.namespace,POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
kubectl get pods -A --sort-by=.status.containerStatuses[0].restartCount
kubectl get pods -A -o=jsonpath='{range .items[?(@.status.phase!="Running")]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
```

## Common control-flow checks

```bash
kubectl get deploy,rs,pods -n <namespace> -l app=<label>
kubectl rollout status deployment/<name> -n <namespace>
kubectl rollout history deployment/<name> -n <namespace>
kubectl get svc,endpointslice -n <namespace>
kubectl get nodes --show-labels
kubectl get node <name> -o jsonpath='{.spec.taints}'
kubectl get configmap,secret -n <namespace>
```

Keep the reference generic. Do not add private hostnames, credentials, learner
assessments, or environment-specific addresses here.
