#!/bin/sh
set -eu
n=cka-mission-boundary
kubectl delete ns "$n" --ignore-not-found --wait=true --timeout=60s >/dev/null
kubectl create ns "$n" >/dev/null; kubectl label ns "$n" managed-by=cka-trainer >/dev/null
kubectl apply -n "$n" -f - >/dev/null <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: placement-case}
spec:
  nodeSelector: {training-zone: moon}
  containers: [{name: sleeper, image: "busybox:1.36", command: [sh, -c, "sleep 3600"]}]
---
apiVersion: v1
kind: Pod
metadata: {name: runtime-case}
spec:
  containers: [{name: sleeper, image: "busybox:not-a-real-tag", command: [sh, -c, "sleep 3600"]}]
EOF
