#!/bin/sh
set -eu
n=cka-mission-replica
i=$(kubectl -n "$n" get deploy signal-web -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null||true)
state=$(kubectl -n "$n" get deploy signal-web -o jsonpath='{.spec.replicas}:{.status.replicas}:{.status.updatedReplicas}:{.status.readyReplicas}:{.status.availableReplicas}:{.status.observedGeneration}:{.metadata.generation}' 2>/dev/null||true)
pods=$(kubectl -n "$n" get pod -l app=signal-web -o name 2>/dev/null | wc -l)
[ "$i" = "nginx:1.27" ] || { echo 'FAIL: expected image nginx:1.27'; exit 1; }
observed=${state%:*}; observed=${observed##*:}; generation=${state##*:}
[ "$state" = "3:3:3:3:3:$observed:$generation" ] && [ "$observed" = "$generation" ] || { echo 'FAIL: Deployment replica state has not converged'; exit 1; }
[ "$pods" -eq 3 ] && kubectl -n "$n" wait --for=condition=Ready pod -l app=signal-web --timeout=1s >/dev/null || { echo 'FAIL: expected exactly three Ready managed Pods'; exit 1; }
echo 'PASS: Deployment ownership chain is healthy'
