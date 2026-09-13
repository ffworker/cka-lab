#!/bin/sh
set -eu
n=cka-mission-rollback
kubectl delete ns "$n" --ignore-not-found --wait=true --timeout=60s >/dev/null
kubectl create ns "$n" >/dev/null; kubectl label ns "$n" managed-by=cka-trainer >/dev/null
kubectl -n "$n" create deploy kraken --image=nginx:1.27 --replicas=3 >/dev/null
kubectl -n "$n" rollout status deploy/kraken --timeout=120s >/dev/null
kubectl -n "$n" set image deploy/kraken nginx=nginx:not-a-real-tag >/dev/null
