# AGENTS.md

## Purpose

CKA Lab is a practical-first CKA training system. Preserve the working trainer,
mission pack, Pod-Professor behavior, and fail-closed Proxmox factory.

## Read before changing behavior

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/TRAINING-MODEL.md`
- `.cka-factory/learner-state.json` when it exists
- `trainer/config/learner-state.default.json` for the generic contract

Individual weak topics, readiness, observations, XP, mission history,
credentials, and active mission state belong under ignored `.cka-factory/`.

## Ownership boundaries

Theory or tutoring work may update `theoryStatus`, `practicalFocus`, and
`lastUpdated`. Practical work may update `practicalFeedback` and `lastUpdated`.
Do not silently overwrite the other side's fields.

Do not introduce missions for topics in `notYetIntroduced`. Stable topics remain
eligible for revision. Executable practice belongs in `scenarios/`; reusable
explanation belongs in `docs/`.

## Infrastructure safety

Infrastructure work is limited to the two factory guests defined and verified
by `scripts/lab-factory.sh`. `lab-down` must continue to fail closed unless
local Terraform state and live Proxmox metadata agree exactly.

Pod-Professor owns the learner experience. It may use Make targets and
kubectl-visible training state, but it does not inventory or repair Proxmox.

## Change discipline

- Keep runtime state and credentials untracked.
- Do not add a second trainer, progression system, or practical workflow.
- Keep public claims limited to behavior verified in this repository.
- Run trainer tests, scenario validation, shell syntax, and relevant
  infrastructure checks after changes.
- Do not commit, push, or rewrite history unless the user explicitly asks.