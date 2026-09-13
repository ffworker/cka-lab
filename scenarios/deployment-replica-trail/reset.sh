#!/bin/sh
set -eu
kubectl delete namespace cka-mission-replica --ignore-not-found --wait=true --timeout=60s >/dev/null
