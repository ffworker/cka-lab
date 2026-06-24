# Networking Drill: Ingress Build/Break

## Goal

Understand the CKA-relevant traffic chain:

```text
client -> ingress controller Service -> ingress controller Pod -> Ingress rule -> backend Service -> Endpoints -> Pods
```

## Build

Create two apps and expose them internally:

```bash
kubectl create deployment web --image=nginx --port=80
kubectl expose deployment web --name=web --port=80 --target-port=80

kubectl create deployment apache --image=httpd --port=80
kubectl expose deployment apache --name=apache --port=80 --target-port=80
```

Create one Ingress with two host rules:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-host
spec:
  ingressClassName: nginx
  rules:
  - host: web.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 80
  - host: apache.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: apache
            port:
              number: 80
```

## Verify

Find the ingress controller HTTP NodePort:

```bash
kubectl get svc -n ingress-nginx ingress-nginx-controller
```

Test both host rules:

```bash
curl -H "Host: web.local" http://<node-ip>:<ingress-http-nodeport>
curl -H "Host: apache.local" http://<node-ip>:<ingress-http-nodeport>
```

## Break

Break the `apache` Service selector:

```bash
kubectl patch svc apache -p '{"spec":{"selector":{"app":"wrong"}}}'
```

Diagnose:

```bash
kubectl get ingress multi-host
kubectl describe ingress multi-host
kubectl get svc apache -o wide
kubectl get endpoints apache
kubectl get pods --show-labels
```

## Fix

Restore the selector:

```bash
kubectl patch svc apache -p '{"spec":{"selector":{"app":"apache"}}}'
```

## Explain Back

Answer without notes:

1. What does the ingress controller NodePort expose?
2. What does the `Host` header decide?
3. What does the Ingress backend point to?
4. What does the Service selector decide?
5. Why did breaking the Service selector break only `apache.local`?
