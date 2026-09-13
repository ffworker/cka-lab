#!/bin/sh
set -eu
n=cka-mission-scale
v=$(kubectl -n "$n" get deploy queue-processor -o jsonpath='{.spec.replicas}:{.status.replicas}:{.status.readyReplicas}:{.status.availableReplicas}' 2>/dev/null||true)
[ "$v" = 4:4:4:4 ] || { echo 'FAIL: replica counters have not converged at four'; exit 1; }
echo 'PASS: four replicas are desired, current, ready, and available'
