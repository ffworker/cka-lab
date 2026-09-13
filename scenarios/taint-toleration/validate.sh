#!/bin/sh
set -eu
n=cka-mission-taints
t=$(kubectl get node cka-worker01 -o go-template='{{range .spec.taints}}{{if and (eq .key "training") (eq .value "dedicated") (eq .effect "NoSchedule")}}owned{{end}}{{end}}' 2>/dev/null||true)
p=$(kubectl -n "$n" get pod audit-agent -o jsonpath='{.status.phase}:{.spec.nodeName}' 2>/dev/null||true)
o=$(kubectl -n "$n" get pod audit-agent -o go-template='{{range .spec.tolerations}}{{if and (eq .key "training") (eq .value "dedicated") (eq .effect "NoSchedule")}}owned{{end}}{{end}}' 2>/dev/null||true)
[ "$t:$p:$o" = owned:Running:cka-worker01:owned ] || { echo 'FAIL: taint, toleration, or placement is wrong'; exit 1; }
echo 'PASS: reservation and toleration are correct'
