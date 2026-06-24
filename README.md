# cka-lab

Practical CKA lab workspace.

## Purpose

Use this repo for:
- kubectl reps
- manifest practice
- troubleshooting drills
- YAML changes
- controlled break/fix exercises

## Current learning mode

CKA study now uses a theory plus practice loop. Every introduced component
should become a small lab as soon as possible:

1. build the smallest working example
2. inspect the objects and relationships
3. break one link deliberately
4. diagnose with normal exam-safe commands
5. fix it
6. explain the component boundary in plain language

The priority is exam readiness and durable understanding. Keep vendor-specific
experiments outside the main drill path unless explicitly requested.

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
3. Build, inspect, break, fix, and explain the practical task
4. Write findings back into `practicalFeedback`
5. Commit `cka-shared` if shared data changed
6. Commit the updated submodule pointer in `cka-lab`

## Guided practice in VS Code

Use:
- `docs/VS_CODE_SETUP.md` for coaching-mode prompt pattern
- `exercises/vscode-guided-practices.md` for checkpoint-based drills mapped to `handoff.json`

## System role

This repo should never invent practical work in isolation.
It should derive work from the theory state produced in `cka-qa` and stored in `cka-shared`.

## AI agents

Any future AI agent working in this repo must read:
- `AI-WORKFLOW.md`
- `AGENTS.md`
- `cka-shared/handoff.json`
