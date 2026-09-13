Repair the Deployment template and wait for rollout:

    kubectl -n cka-mission-replica set image deployment/signal-web nginx=nginx:1.27
    kubectl -n cka-mission-replica rollout status deployment/signal-web
    kubectl -n cka-mission-replica get deployment,replicaset,pods
