# Kubelet Certificates

Quick notes for kubelet certificate related issues.

## What to verify

- kubelet client certificate validity
- CA trust chain on node and control plane
- CSR approval status

## Useful commands

```bash
kubectl get csr
kubectl describe csr <csr-name>
openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem -noout -dates -subject -issuer
```
