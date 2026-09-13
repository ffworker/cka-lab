---
name: pod-professor
description: Load current CKA state before tutoring.
version: 0.1.0
author: Dennis (ffworker), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cka, kubernetes, tutoring, active-recall]
    related_skills: []
---

# Pod-Professor Session Bootstrap

Use at the start of every CKA study session in the `cka-lab` repository.

## Procedure

1. Confirm the working directory is the repository root by locating `agents/pod-professor/AGENT.md` and `docs/cka-shared/handoff.json`.
2. Read `agents/pod-professor/AGENT.md` and `agents/pod-professor/TEACHING.md` completely.
3. Read `docs/cka-shared/handoff.json` and `qa/status/current-focus.md`.
4. Read only relevant `qa/` material, plus `.cka-factory/profile.json` and mission/scenario history when present and useful.
5. Teach from the current repository state; use memory only for compact cross-session learner observations.
6. Rely on `make lab-up`, `make lab-down`, trainer commands, and kubectl-visible state. Never manually inventory or configure proxmox.example. Delegate a broken factory to the main infrastructure agent outside the tutor session.
7. When the user asks for practice, a mission, hands-on work, a CKA task, training, or to continue, inspect `make status` and the trainer profile, start or resume `make mission`, and present only the generated briefing and success criteria.
8. Let the learner operate the cluster. Use `make validate` for checks, `make hint` for progressive help, and `make solution` only after an explicit solution request.
9. After PASS, relay the trainer-owned XP, achievement, streak, rank, and recommendation output. Use `make reset` to clean completed objects before another mission.

## Pitfalls

- Do not treat memory as the academic source of truth.
- Do not start a quiz merely because this bootstrap skill loaded.
- Do not rewrite theory classifications without evidence and the supported repository workflow.
- Do not create separate XP, achievement, streak, or mission-history state.
- Do not replace practical-first requests with broad theory quizzes. Keep explanations short, just-in-time, and after an attempt.

## Verification

Before the first teaching checkpoint, be able to identify the current focus, weak or unstable concepts, stable topics eligible for revision, trainer/cluster status, active mission, and existing trainer history without relying on memory alone.
