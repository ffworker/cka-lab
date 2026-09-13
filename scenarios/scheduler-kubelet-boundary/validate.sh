#!/bin/sh
set -eu
n=cka-mission-boundary
for p in placement-case runtime-case; do [ "$(kubectl -n "$n" get pod "$p" -o jsonpath='{.status.phase}' 2>/dev/null||true)" = Running ] || { echo "FAIL: $p is not Running"; exit 1; }; done
[ "$(kubectl -n "$n" get pod runtime-case -o jsonpath='{.spec.containers[0].image}')" = busybox:1.36 ] || exit 1
echo 'PASS: placement and runtime failures are repaired'
