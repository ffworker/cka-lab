#!/bin/sh
set -eu
n=cka-mission-config
kubectl delete ns "$n" --ignore-not-found --wait=true --timeout=60s >/dev/null
kubectl create ns "$n" >/dev/null; kubectl label ns "$n" managed-by=cka-trainer >/dev/null
kubectl -n "$n" create cm app-settings --from-literal=mode=broken >/dev/null
kubectl -n "$n" create secret generic app-credentials --from-literal=token=mission-token >/dev/null
kubectl apply -n "$n" -f - >/dev/null <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: env-reader}
spec:
  containers:
  - name: reader
    image: busybox:1.36
    command: [sh, -c, "sleep 3600"]
    env:
    - {name: APP_MODE, valueFrom: {configMapKeyRef: {name: app-settings, key: app_mode}}}
    - {name: TOKEN, valueFrom: {secretKeyRef: {name: app-credentials, key: token}}}
EOF
