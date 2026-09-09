# 2026-04-20 Wrap-up So Far

## New topics introduced
- Logging
- Monitoring
- Rolling Updates / Rollbacks
- Commands and Arguments
- Environment Variables
- Secrets
- Multi-Container Pods
- Init Containers
- Intro to Autoscaling
- Manual Scaling
- HPA
- VPA
- Backup and Restore
- etcd Backup
- Resource backup mentioned but not yet reviewed with quizzes
- Security block introduced but only partially covered, not yet reviewed here

## Judged state

### Stable
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

### Improving
- Kubernetes Components
- Core Principles
- Pods
- Services
- NodePort
- ClusterIP
- Labels / Selectors
- Static Pods
- Admission Controllers
- Multiple Schedulers
- Rolling Updates / Rollbacks
- Environment Variables
- Secrets
- Manual Scaling
- HPA

### Weak
- Deployments
- Scheduler Profiles

## Unstable concepts
- scheduler vs kubelet
- current replicas vs available replicas
- Service -> Endpoints -> Pod
- precise Pod definition under pressure
- multiple schedulers vs scheduler profiles
- available replicas during rolling updates

## Learning-process note
- The user benefits from short breaks at natural topic boundaries.
- Good break boundary just used: logging / monitoring / backup / etcd backup.
- Future sessions should include short recovery breaks after broad topic clusters.
