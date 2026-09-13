#!/bin/sh
set -eu
n=cka-mission-services
[ "$(kubectl -n "$n" get svc store-internal -o jsonpath='{.spec.type}:{.spec.ports[0].targetPort}' 2>/dev/null||true)" = ClusterIP:80 ] || { echo 'FAIL: internal Service is wrong'; exit 1; }
[ "$(kubectl -n "$n" get svc store-external -o jsonpath='{.spec.type}:{.spec.ports[0].targetPort}:{.spec.ports[0].nodePort}:{.spec.selector.app}' 2>/dev/null||true)" = NodePort:80:30080:storefront ] || { echo 'FAIL: external Service is wrong'; exit 1; }
for svc in store-internal store-external; do
  ready=$(kubectl -n "$n" get endpointslice -l kubernetes.io/service-name="$svc" -o jsonpath='{range .items[*].endpoints[?(@.conditions.ready==true)]}{.addresses[0]}{" "}{end}' 2>/dev/null || true)
  [ "$(printf '%s' "$ready" | wc -w)" -eq 2 ] || { echo "FAIL: $svc does not have two ready endpoints"; exit 1; }
done
echo 'PASS: ClusterIP and NodePort paths are repaired'
