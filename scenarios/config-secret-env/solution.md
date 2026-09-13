Add the exact ConfigMap key expected by the Pod:

    kubectl -n cka-mission-config patch configmap app-settings --type merge -p '{"data":{"app_mode":"practice"}}'
    kubectl -n cka-mission-config get pod env-reader -w

Do not move the token into a Pod value or ConfigMap.
