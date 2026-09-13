Repair only the selector:

    kubectl -n cka-mission-endpoints patch service api-svc -p '{"spec":{"selector":{"app":"mission-api"}}}'
    kubectl -n cka-mission-endpoints get service,endpointslice
