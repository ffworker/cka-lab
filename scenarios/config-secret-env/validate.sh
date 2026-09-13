#!/bin/sh
set -eu
n=cka-mission-config
[ "$(kubectl -n "$n" get pod env-reader -o jsonpath='{.status.phase}' 2>/dev/null||true)" = Running ] || { echo 'FAIL: env-reader is not Running'; exit 1; }
[ "$(kubectl -n "$n" get pod env-reader -o jsonpath='{.spec.containers[0].env[?(@.name=="APP_MODE")].valueFrom.configMapKeyRef.name}:{.spec.containers[0].env[?(@.name=="APP_MODE")].valueFrom.configMapKeyRef.key}' 2>/dev/null||true)" = app-settings:app_mode ] || { echo 'FAIL: APP_MODE is not sourced from the required ConfigMap key'; exit 1; }
[ "$(kubectl -n "$n" exec env-reader -- printenv APP_MODE 2>/dev/null||true)" = practice ] || exit 1
[ "$(kubectl -n "$n" exec env-reader -- printenv TOKEN 2>/dev/null||true)" = mission-token ] || exit 1
[ "$(kubectl -n "$n" get pod env-reader -o jsonpath='{.spec.containers[0].env[?(@.name=="TOKEN")].valueFrom.secretKeyRef.name}')" = app-credentials ] || exit 1
echo 'PASS: external configuration is injected correctly'
