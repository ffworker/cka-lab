#!/bin/sh
set -eu
n=cka-mission-rollback
i=$(kubectl -n "$n" get deploy kraken -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null||true)
a=$(kubectl -n "$n" get deploy kraken -o jsonpath='{.status.availableReplicas}' 2>/dev/null||true)
r=$(kubectl -n "$n" get deploy kraken -o jsonpath='{.metadata.annotations.deployment\.kubernetes\.io/revision}' 2>/dev/null||echo 0)
uid=$(kubectl -n "$n" get deploy kraken -o jsonpath='{.metadata.uid}' 2>/dev/null||true)
owners=$(kubectl -n "$n" get replicaset -l app=kraken -o jsonpath='{range .items[*].metadata.ownerReferences[?(@.controller==true)]}{.uid}{" "}{end}' 2>/dev/null||true)
owned=0
for owner in $owners; do [ "$owner" = "$uid" ] && owned=$((owned + 1)); done
[ "$i:$a" = nginx:1.27:3 ] && [ "$r" -ge 3 ] && [ "$owned" -ge 2 ] || { echo 'FAIL: healthy revision or retained rollout history is incomplete'; exit 1; }
echo 'PASS: rollout restored with history intact'
