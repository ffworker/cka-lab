# CKA theory and recall

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

Use this directory for:
- quizzes
- repetition
- weak-topic tracking
- precise definitions
- mental models
- progress tracking

Do not use this directory for noisy manifest experiments. Do use it to turn
every introduced concept into a practical build/break recommendation for the
practical areas in this repository.

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

## Internal handoff

Theory state is written to `docs/cka-shared/handoff.json` in this repository.

## Core commands in chat

- `Status`
- `Quiz <topic>`
- `Repeat`
- `Update <topic>`

## Source of learning truth

The `qa/` area is the source of truth for:
- weak topics
- improving topics
- stable topics
- unstable concepts
- practical recommendations

## Workflow

1. theory and recall work happens in `qa/`
2. results are written into `docs/cka-shared/handoff.json`
3. practical work in this repository derives from those results
4. practical findings return through `practicalFeedback`

If theory changes but the shared handoff is not updated, the lab will drift.

## AI agents

Any future AI agent working in `qa/` must read:
- repository-root `AI-WORKFLOW.md`
- repository-root `AGENTS.md`
- `qa/AI-WORKFLOW.md`
- `qa/AGENTS.md`
- `docs/cka-shared/handoff.json`
