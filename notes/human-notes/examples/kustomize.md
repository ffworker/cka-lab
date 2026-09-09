# Resources can be added as files or directories

```yaml
resources:

- api/
- db/
```

## Common labels can be added to all resources

```yaml
commonLabels:
  department: demo
```

## Namespace can be set for all resources

```yaml
namespace: demo
```

## Name prefix and suffix can be used to modify the names of all resources

```yaml
namePrefix: KAPPEL.TECH-
```

## Common annotations can be added to all resources

```yaml
commonAnnotations:
  owner: Dennis Kappel
  project: demo
  description: Demo application
```

## (INLINE) Patches can be used to modify resources without changing the original files

```yaml
patches:

- target:
      kind: Deployment
      name: api-deployment
    patch: |-
  - op: replace
        path: /spec/replicas
        value: 3
```

## (FILE) Patches can also be defined in separate files

```yaml
patches:

- label-patch.yaml
```

## strategic merge patches can be used to modify resources based on their structure

```yaml
patches:

- patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: api-deployment
      spec:
        template:
          spec:
            containers:
              - name: api-container
                resources:
                  limits:
                    cpu: "500m"
                    memory: "256Mi"
        spec:
          replicas: 3
```

## another approach is using link to a patch-file -> just patch what you want to change (merges)

```yaml
patches:
  - patch.yaml
```

## patch.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    metadata:
      labels:
        component: web
```

## delete a KEY with a patch -> set key to NULL

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  template:
    metadata:
      labels:
        component: null
```
