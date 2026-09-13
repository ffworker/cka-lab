#!/bin/sh
set -eu
n=cka-mission-replica
kubectl delete ns "$n" --ignore-not-found --wait=true --timeout=60s >/dev/null
kubectl create ns "$n" >/dev/null
kubectl label ns "$n" managed-by=cka-trainer >/dev/null
kubectl -n "$n" create deployment signal-web --image=nginx:not-a-real-tag --replicas=3 >/dev/null
