#!/bin/sh
set -eu
kubectl delete namespace cka-mission-boundary --ignore-not-found --wait=true --timeout=60s >/dev/null
