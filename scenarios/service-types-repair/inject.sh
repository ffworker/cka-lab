#!/bin/sh
set -eu
n=cka-mission-services
kubectl delete ns "$n" --ignore-not-found --wait=true --timeout=60s >/dev/null
kubectl create ns "$n" >/dev/null; kubectl label ns "$n" managed-by=cka-trainer >/dev/null
kubectl -n "$n" create deploy storefront --image=nginx:1.27 --replicas=2 >/dev/null
kubectl -n "$n" rollout status deploy/storefront --timeout=120s >/dev/null
kubectl apply -n "$n" -f - >/dev/null <<'EOF'
apiVersion: v1
kind: Service
metadata: {name: store-internal}
spec: {selector: {app: storefront}, ports: [{port: 80, targetPort: 8080}]}
---
apiVersion: v1
kind: Service
metadata: {name: store-external}
spec: {type: NodePort, selector: {app: wrong-store}, ports: [{port: 80, targetPort: 80, nodePort: 30080}]}
EOF
