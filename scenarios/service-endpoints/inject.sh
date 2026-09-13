#!/bin/sh
set -eu
n=cka-mission-endpoints
kubectl delete ns "$n" --ignore-not-found --wait=true --timeout=60s >/dev/null
kubectl create ns "$n" >/dev/null; kubectl label ns "$n" managed-by=cka-trainer >/dev/null
kubectl -n "$n" create deploy mission-api --image=nginx:1.27 --replicas=2 >/dev/null
kubectl -n "$n" expose deploy mission-api --name=api-svc --port=80 >/dev/null
kubectl -n "$n" patch svc api-svc -p '{"spec":{"selector":{"app":"wrong-backend"}}}' >/dev/null
kubectl -n "$n" rollout status deploy/mission-api --timeout=120s >/dev/null
