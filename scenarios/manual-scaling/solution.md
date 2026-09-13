Scale and wait:

    kubectl -n cka-mission-scale scale deployment queue-processor --replicas=4
    kubectl -n cka-mission-scale rollout status deployment/queue-processor
    kubectl -n cka-mission-scale get deployment queue-processor
