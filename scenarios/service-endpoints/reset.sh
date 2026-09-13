#!/bin/sh
set -eu
kubectl delete namespace cka-mission-endpoints --ignore-not-found --wait=true --timeout=60s >/dev/null
