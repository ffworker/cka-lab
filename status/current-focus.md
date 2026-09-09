# Current Focus

## Weak
- Deployments
- Scheduler Profiles

## Improving
- Kubernetes Components
- Core Principles
- Pods
- Services
- NodePort
- ClusterIP
- Labels / Selectors
- Ingress
- Ingress Controllers
- Static Pods
- Admission Controllers
- Multiple Schedulers
- Rolling Updates / Rollbacks
- Environment Variables
- Secrets
- Manual Scaling
- HPA
- kubeconfig
- RBAC
- ServiceAccounts
- Authentication
- Certificates
- Resource Backup
- Node Selectors
- ConfigMaps

## Stable
- ReplicaSets
- DaemonSets
- Resource Limits
- Priority Classes
- Commands and Arguments
- Multi-Container Pods
- Init Containers
- VPA
- Logging
- Monitoring
- Backup and Restore
- etcd Backup
- OS Upgrades
- TLS
- ClusterRoles
- Taints and Tolerations

## Unstable Concepts
- scheduler vs kubelet
- current replicas vs available replicas
- Service -> Endpoints -> Pod
- precise Pod definition under pressure
- multiple schedulers vs scheduler profiles
- available replicas during rolling updates
- certificate vs private key
- kubeconfig vs RBAC boundary
- Ingress controller NodePort vs application Service NodePort
- Ingress rule -> Service -> Endpoints -> Pod

## Practical recommendations sent to lab
- trace Deployment -> ReplicaSet -> Pods
- debug a Service with no endpoints
- differentiate scheduler vs kubelet from symptom patterns
- compare ClusterIP vs NodePort with exact troubleshooting chain
- build and break Deployment -> Service -> Endpoints -> Ingress controller routing
- explain Host header routing through an Ingress controller NodePort
- compare static Pods vs DaemonSets
- compare multiple schedulers vs scheduler profiles
- contrast admission controllers with normal controllers
- practice rolling updates and watch available replica behavior
- compare multi-container Pods with init containers
- compare manual scaling, HPA, and VPA
- compare etcd snapshot restore with YAML-only restore
- compare kubeconfig, RBAC, ServiceAccounts, and authentication flow
- compare certificate, private key, and CA trust roles
- compare ConfigMaps, env vars, and Secrets
- compare nodeSelector with taints/tolerations and later affinity
