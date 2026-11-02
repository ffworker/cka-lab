# Learning-first reset (November 2026)

> I started with a simple need: **I want to pass the CKA exam.**
> Along the way I built a trainer, an AI tutor, eight missions, game mechanics,
> and a two-repository Proxmox/Terraform/Ansible lab factory.
> Building it was useful practice, but **building a learning platform is not the
> same as using it to learn**.

This document is the scope guard for [Linear CKA-Lab · Learning First](https://linear.app/bytegeist/project/cka-lab-learning-first-3c7cc473970e). It is **not** a claim that the full learning loop has passed a live acceptance test.

## Goal: one real session before the next feature

1. Preview a mission *without touching infrastructure* with `make preview`.
2. Explicitly choose an isolated disposable environment (never a production Kubernetes context).
3. Run a mission; observe initial validator failure; diagnose and fix it yourself.
4. Observe the independent Kubernetes validator pass; reset cleanly.
5. Repeat the failure class later, ideally with fewer hints.

**The model may teach. The learner repairs. Deterministic checks decide PASS/FAIL.**
A model asserting that something should work is not a successful lab test.

## KEEP / CLEAN / REMOVE / VERIFY

| Decision | Existing feature | Reason / next gate |
| --- | --- | --- |
| KEEP | Trainer CLI, structured mission definitions | A small, inspectable loop that can be tested offline |
| KEEP | Namespace-scoped injectors, validators and resets | They test the actual cluster state, not model prose |
| KEEP | Two progressive hints and a hidden solution | Supports graduated guidance without taking over |
| KEEP (optional) | Pod-Professor / Hermes adapter | Good teaching contract, but effectiveness not yet demonstrated |
| KEEP (minimal) | Local history and attempts | Needed to compare repeated performance; no new data store |
| CLEAN | Entry point and preflight | `make preview` introduces the task offline; no factory before learning intent |
| CLEAN | Hardcoded two-node assumptions | Only pilot on the intended disposable kubeadm context; no production Talos reuse |
| VERIFY | Each injector/reset ownership boundary | Static tests are insufficient for real cluster isolation |
| VERIFY | Negative and positive live validator outcomes | CI mocks and shell syntax are not proof of a real mission |
| VERIFY | AI hints are useful and don't spoil tasks | Compare attempts with and without assistance |
| FREEZE | `proxmox-lab` as a separate platform project | Existing dependency stays available, but no expansion or live `terraform destroy` without explicit review |
| LATER | Dynamic sandbox provisioning, broader domains, multi-user Web UI | Future vision, **not a V1 requirement** |
| DEFER | XP/ranks/achievements expansion | Already implemented; no new gamification work until needed |

## v1 reality check

- Eight mission scenarios exist, focused on Deployments, Services, ConfigMaps/Secrets, scaling, rollbacks and scheduling/taints.
- Those missions **do not amount to full CKA-exam coverage**; coverage gaps must be mapped against current exam objectives before making a readiness claim.
- The CKA factory describes a fixed two-VM kubeadm/Flannel stack, pinned to `proxmox-lab`. It needs Proxmox template, network, tokens, state and ownership metadata. It is not a frictionless general learning backend.
- The Rocky reference scenario inside `proxmox-lab` is a separate historical track, not part of the CKA tutor loop.
- Existing CI checks Python logic, JSON contracts and shell syntax. They are **not a live Proxmox apply/destroy proof**, and this repository has not captured a personally completed end-to-end CKA learning session.
- The AI tutor should **never** be allowed to configure or destroy the host, or silently modify the active mission.
- Do not run the mission pack against the user's live Talos/GitOps cluster. The scenarios intentionally break workloads or alter a node taint.

## Safe first action

```bash
git clone --recurse-submodules https://github.com/ffworker/cka-lab.git
cd cka-lab
make preview
```

`make preview` reads local catalogue/learning state and prints a suggested mission. It **does not** call `kubectl`, invoke a scenario script, initialize local profile state, or start the VM factory. It is not a simulation of a live successful mission.

After preflight and explicit resource-safety review, provisioning and practice remain separate, manual operations. Record the actual first complete mission before building anything new.

## Publication discipline

The future Bytegeist article may honestly describe both sides: AI made this architecture possible, but encouraged scope drift and premature feature-building. The story only becomes a published case study **after** the author has personally learned with, tested, and validated the lab. Technical artifacts or green CI alone don't prove improved learning.
