# Priority Drills

Generated from `cka-shared/handoff.json`.

## Current top drills
1. trace Deployment -> ReplicaSet -> Pods
2. debug a Service with no endpoints
3. differentiate scheduler vs kubelet from symptom patterns
4. compare ClusterIP vs NodePort with exact troubleshooting chain
5. build and break Deployment -> Service -> Endpoints -> Ingress controller routing
6. explain Host header routing through an Ingress controller NodePort
7. compare static Pods vs DaemonSets
8. compare multiple schedulers vs scheduler profiles
9. contrast admission controllers with normal controllers
10. practice rolling updates and watch available replica behavior
11. compare multi-container Pods with init containers
12. compare manual scaling, HPA, and VPA
13. compare etcd snapshot restore with YAML-only restore
14. compare kubeconfig, RBAC, ServiceAccounts, and authentication flow
15. compare certificate, private key, and CA trust roles
16. compare ConfigMaps, env vars, and Secrets
17. compare nodeSelector with taints/tolerations and later affinity

## Ready for practical work
- Pods
- ReplicaSets
- Services basics
- ClusterIP basics
- NodePort basics
- Labels and Selectors
- Ingress basics
- Ingress controller basics
- Static Pods
- DaemonSets
- Resource Limits
- Priority Classes
- Admission Controllers basics
- Commands and Arguments
- Environment Variables
- Secrets
- ConfigMaps
- Multi-Container Pods
- Init Containers
- Manual Scaling
- HPA
- VPA
- Logging
- Monitoring
- Backup and Restore
- etcd Backup
- Resource Backup
- kubeconfig
- RBAC
- ServiceAccounts
- TLS
- ClusterRoles
- OS Upgrades
- Node Selectors
- Taints and Tolerations

## Constraint
Do not build drills for topics listed under `notYetIntroduced` in the shared handoff.
Current examples not yet introduced include Jobs, CronJobs, Affinity / Anti-Affinity, Network Policies, Security Contexts, Authentication deeper internals, and Certificate API details.
