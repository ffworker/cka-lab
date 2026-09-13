Use rollout history and rollback:

    kubectl -n cka-mission-rollback rollout history deployment/kraken
    kubectl -n cka-mission-rollback rollout undo deployment/kraken
    kubectl -n cka-mission-rollback rollout status deployment/kraken
