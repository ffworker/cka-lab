# Network Troubleshooting

See the visual flow in the embedded diagrams in the root `README.md`.

Main scope:
- Pod-to-Pod connectivity
- Service routing
- Ingress request routing
- DNS resolution
- CNI status
- kube-proxy rules

Reference: `DEMO/troubleshoot/03-NETWORK.md`.

## Ingress Request Path

Ingress troubleshooting starts by separating the exposed controller from the
backend application Service.

```text
client
-> ingress controller Service, often NodePort in a bare-metal lab
-> ingress controller Pod
-> Ingress host/path rule
-> backend Service
-> Endpoints
-> Pods
```

Important boundaries:

- The ingress controller Service exposes the controller, not the app.
- The `Host` header chooses the matching Ingress rule.
- The Ingress backend points to a Service port.
- The Service selector chooses Pods and creates Endpoints.
- Empty Endpoints means the Service points to no ready backend Pods.

Core checks:

```bash
kubectl get ingress
kubectl describe ingress <name>
kubectl get ingressclass
kubectl get svc -n ingress-nginx
kubectl get svc <backend-service> -o wide
kubectl get endpoints <backend-service>
kubectl get pods --show-labels
```

Bare-metal NodePort test:

```bash
curl -H "Host: web.local" http://<node-ip>:<ingress-controller-nodeport>
```

Common mistake:

Do not say the application Service points to the Ingress. The direction is:

```text
Ingress rule -> backend Service -> Endpoints -> Pods
```

## Stale k3s Node IP

Symptoms after the single-node host changes networks:

- `metrics-server` times out connecting to the Kubernetes API or kubelet.
- `node-exporter` probes target an address the host no longer owns.
- `kubectl top nodes` reports that the Metrics API is unavailable.
- The `kubernetes` service endpoint still contains the old node address.

Check the advertised address against the host:

```bash
ip -br addr
kubectl get node -o wide
kubectl get endpoints kubernetes -o wide
kubectl get apiservice v1beta1.metrics.k8s.io
```

For a single-node k3s lab, configure the reachable LAN address in
`/etc/rancher/k3s/config.yaml`:

```yaml
node-ip: 172.17.11.37
advertise-address: 172.17.11.37
tls-san:
  - 172.17.11.37
```

Restart and verify:

```bash
sudo systemctl restart k3s
kubectl rollout status deployment/metrics-server -n kube-system
kubectl top nodes
```

Use a DHCP reservation or stable address for a persistent cluster. Otherwise,
repeat this after the host address changes.
