#!/bin/sh
set -eu
n=cka-mission-taints
kubectl delete ns "$n" --ignore-not-found --wait=true --timeout=60s >/dev/null
existing=$(kubectl get node cka-worker01 -o go-template='{{range .spec.taints}}{{if and (eq .key "training") (eq .effect "NoSchedule")}}{{.value}}{{end}}{{end}}')
case "$existing" in
  ""|dedicated) ;;
  *) echo 'refusing to overwrite non-factory training taint' >&2; exit 1 ;;
esac
kubectl taint node cka-worker01 training=dedicated:NoSchedule --overwrite >/dev/null
kubectl create ns "$n" >/dev/null; kubectl label ns "$n" managed-by=cka-trainer >/dev/null
kubectl apply -n "$n" -f - >/dev/null <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: audit-agent}
spec:
  nodeSelector: {kubernetes.io/hostname: cka-worker01}
  containers: [{name: audit-agent, image: "busybox:1.36", command: [sh, -c, "sleep 3600"]}]
EOF
