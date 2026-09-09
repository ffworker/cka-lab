# *Patch Types*
Two patch strategies are available: **JSON 6902** and **Strategic Merge Patch**.
---
## **JSON 6902 Patch**
Defined by RFC 6902. Operations are explicit — you specify an `op`, a JSON Pointer `path`, and a `value`.
Rename a deployment (`metadata.name`)
```yaml
patches:
  - target:
      kind: Deployment
      name: MY-deployment
    patch: |-
      - op: replace
        path: /metadata/name
        value: YOUR-deployment
```
Change replica count
```yaml
patches:
  - target:
      kind: Deployment
      name: my-deployment
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
```
---
## **Strategic Merge Patch**
Write only what you want changed — Kubernetes merges it automatically. No need to specify an operation type; the structure speaks for itself.
Change replica count
```yaml
patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-deployment
      spec:
        replicas: 5
```
Rename a deployment (`metadata.name`)
```yaml
patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: YOUR-deployment
```
---
Quick Comparison
	JSON 6902	Strategic Merge
Syntax	Explicit ops (`replace`, `add`, `remove`)	Partial manifest
Targeting	JSON Pointer path (`/spec/replicas`)	Resource identity (`kind` + `name`)
Best for	Surgical, precise edits	Readable, common-case changes

## **Seperate File**

In your **`kustomization.yaml`** just point to a file like that:

```yaml
patches:
  - path: patch.yaml
    target:
      kind: deployment
      name: my-deployment
```

* that points to:

**`inline-patch.yaml`**
```yaml
- op: replace
  path: /spec/replicas
  value: 5
```

** NOTE: You can also point to strategic Merge Patches instead of Inline Patches. **

**`strategic-patch.yaml`**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 5
```

## another example for using strategic inline patches to **REMOVE**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    spec:
      containers:
        - $patch: delete
          name: my-container
```
