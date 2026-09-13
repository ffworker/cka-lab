#!/bin/sh
set -eu
kubectl delete namespace cka-mission-scale --ignore-not-found --wait=true --timeout=60s >/dev/null
