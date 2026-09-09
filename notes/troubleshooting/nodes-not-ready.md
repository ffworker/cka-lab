# Nodes NotReady Troubleshooting

Systematic checks when one or more nodes become `NotReady`.

## Fast checks

```bash
kubectl get nodes -o wide
kubectl describe node <node-name>
```

## Typical areas

1. Kubelet health
2. Container runtime health
3. Disk/memory pressure
4. Network plugin readiness
5. Certificate expiration and trust issues

## Logs

```bash
journalctl -u kubelet -n 200 --no-pager
```
