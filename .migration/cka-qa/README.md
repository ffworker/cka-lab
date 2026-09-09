# cka-qa

## Kubernetes learning map

Legend:
- 🟢 good
- 🟡 meh / improving
- 🔴 needs improvement
- ⚪ not reviewed yet

```text
Kubernetes
├─ Foundations
│  ├─ 🟡 Core Principles
│  └─ 🟡 Kubernetes Components
│
├─ Workloads
│  ├─ 🟡 Pods
│  ├─ 🔴 Deployments
│  ├─ 🟢 ReplicaSets
│  ├─ 🟢 DaemonSets
│  ├─ 🟢 Commands and Arguments
│  ├─ 🟡 Rolling Updates / Rollbacks
│  ├─ 🟢 Multi-Container Pods
│  └─ 🟢 Init Containers
│
├─ Services and Networking
│  ├─ 🟡 Services
│  ├─ 🟡 ClusterIP
│  ├─ 🟡 NodePort
│  ├─ 🟡 Labels / Selectors
│  ├─ 🔴 Service -> Endpoints -> Pod
│  ├─ ⚪ Ingress
│  ├─ ⚪ Network Policies
│  ├─ ⚪ CoreDNS / DNS Resolution
│  └─ ⚪ CNI Basics
│
├─ Scheduling and Control
│  ├─ 🟡 scheduler vs kubelet
│  ├─ 🟡 Static Pods
│  ├─ 🟡 Multiple Schedulers
│  ├─ 🔴 Scheduler Profiles
│  ├─ 🟢 Priority Classes
│  ├─ 🟡 Node Selectors
│  ├─ 🟢 Taints and Tolerations
│  └─ ⚪ Affinity / Anti-Affinity
│
├─ Configuration and Secrets
│  ├─ 🟡 Environment Variables
│  ├─ 🟡 Secrets
│  ├─ 🟡 ConfigMaps
│  ├─ 🟡 ServiceAccounts
│  └─ ⚪ Security Contexts
│
├─ Scaling and Resource Control
│  ├─ 🟢 Resource Limits
│  ├─ 🟡 Manual Scaling
│  ├─ 🟡 HPA
│  └─ 🟢 VPA
│
├─ Observability and Maintenance
│  ├─ 🟢 Logging
│  ├─ 🟢 Monitoring
│  ├─ 🟢 Backup and Restore
│  ├─ 🟢 etcd Backup
│  ├─ 🟡 Resource Backup
│  └─ 🟢 OS Upgrades
│
└─ Security and Access
   ├─ 🟡 Admission Controllers
   ├─ 🟡 Authentication
   ├─ 🟢 TLS
   ├─ 🟡 Certificates
   ├─ 🟡 kubeconfig
   ├─ 🟡 RBAC
   ├─ 🟢 ClusterRoles
   └─ 🟡 ServiceAccounts
```

Theory and recall workspace for CKA preparation.

## Purpose

Use this repo for:
- quizzes
- repetition
- weak-topic tracking
- precise definitions
- mental models
- progress tracking

Do not use this repo for noisy manifest experiments. Do use it to turn every
introduced concept into a practical build/break recommendation for `cka-lab`.

## Current study mode

The learning loop is now theory plus practice:

1. define the component precisely
2. build a minimal working example
3. inspect the Kubernetes objects that were created
4. break one link in the chain on purpose
5. fix it with normal `kubectl` troubleshooting
6. explain the full request/control flow back in plain language

The goal is CKA exam readiness first. Vendor-specific tools, shortcuts, and
personal experiments are separate from the main study path unless explicitly
chosen.

## Connected repo

This repo writes handoff data to:
- `cka-shared/handoff.json` via the git submodule

## Core commands in chat

- `Status`
- `Quiz <topic>`
- `Repeat`
- `Update <topic>`

## Source of learning truth

This repo is the source of truth for:
- weak topics
- improving topics
- stable topics
- unstable concepts
- practical recommendations

## Workflow in the larger system

1. theory work happens here
2. results are written into `cka-shared/handoff.json`
3. `cka-lab` reads those results and builds practical work from them
4. practical findings come back through `practicalFeedback`

If theory changes but the shared handoff is not updated, the lab will drift.

## AI agents

Any future AI agent working in this repo must read:
- `AI-WORKFLOW.md`
- `AGENTS.md`
- `cka-shared/handoff.json`
