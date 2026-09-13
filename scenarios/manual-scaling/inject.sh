#!/bin/sh
set -eu
n=cka-mission-scale
kubectl delete ns "$n" --ignore-not-found --wait=true --timeout=60s >/dev/null
kubectl create ns "$n" >/dev/null; kubectl label ns "$n" managed-by=cka-trainer >/dev/null
kubectl -n "$n" create deploy queue-processor --image=nginx:1.27 --replicas=1 >/dev/null
kubectl -n "$n" rollout status deploy/queue-processor --timeout=120s >/dev/null
