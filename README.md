# cka-lab

Practical CKA lab workspace.

## Purpose

Use this repo for:
- kubectl reps
- manifest practice
- troubleshooting drills
- YAML changes
- controlled break/fix exercises

## Connected shared state

Read from:
- `cka-shared/handoff.json` via the git submodule

Write back to:
- `cka-shared/handoff.json` under `practicalFeedback`

## Important rule

Do not practice topics listed in `notYetIntroduced`.

## Recommended workflow

1. Read `cka-shared/handoff.json`
2. Pick one `recommendedDrill`
3. Do the practical task
4. Write findings back into `practicalFeedback`
5. Commit `cka-shared` if shared data changed
6. Commit the updated submodule pointer in `cka-lab`

## System role

This repo should never invent practical work in isolation.
It should derive work from the theory state produced in `cka-qa` and stored in `cka-shared`.

## AI agents

Any future AI agent working in this repo must read:
- `AI-WORKFLOW.md`
- `AGENTS.md`
- `cka-shared/handoff.json`
