#!/bin/sh
set -eu
n=cka-mission-endpoints
s=$(kubectl -n "$n" get svc api-svc -o jsonpath='{.spec.selector.app}' 2>/dev/null||true)
service=$(kubectl -n "$n" get svc api-svc -o jsonpath='{.spec.type}:{.spec.ports[0].port}' 2>/dev/null||true)
r=$(kubectl -n "$n" get endpointslice -l kubernetes.io/service-name=api-svc -o jsonpath='{range .items[*].endpoints[?(@.conditions.ready==true)]}{.addresses[0]}{" "}{end}' 2>/dev/null||true)
[ "$s:$service" = mission-api:ClusterIP:80 ] && [ "$(printf '%s' "$r"|wc -w)" -eq 2 ] || { echo 'FAIL: selector, Service type/port, or ready endpoints are wrong'; exit 1; }
echo 'PASS: Service has two ready endpoints'
