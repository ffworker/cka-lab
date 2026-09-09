Step-by-Step usually

# APP FAILURE ->

**1. FRONTEND -> Check Webserver access of NodeiP:**

```bash
curl http://web-service-ip:node-port 
```

**2. Check Service to web-service -> if not check labels & Label-Selector**

```bash
kubectl get svc <service-name>
```

**3. Check the pod itself (status / restarts)**

```bash
kubectl get pods
```

**4. describe pod events**

```bash
kubectl describe pod <pod-name>
```

**5. check pod logs**

```bash
kubectl logs <pod-name>
```

*parameters:*   `-f` = follow logs`
                --previous` = shows logs before pod went down

**6. check pod logs**

```bash
kubectl logs <pod-name>
```

**7. do the same for the DB-Service**

check `services` `endpoints` `logs` `events` `labels`