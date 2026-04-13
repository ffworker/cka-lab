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

1. Read `../cka-shared/handoff.json`
2. Pick one `recommendedDrill`
3. Do the practical task
4. Write findings back into `practicalFeedback`
