#!/bin/sh
set -eu
kubectl delete namespace cka-mission-taints --ignore-not-found --wait=true --timeout=60s >/dev/null
existing=$(kubectl get node cka-worker01 -o go-template='{{range .spec.taints}}{{if and (eq .key "training") (eq .effect "NoSchedule")}}{{.value}}{{end}}{{end}}')
if [ "$existing" = dedicated ]; then
  kubectl taint node cka-worker01 training:NoSchedule- >/dev/null
fi
