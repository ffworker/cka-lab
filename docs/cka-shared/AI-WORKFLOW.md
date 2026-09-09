# AI-WORKFLOW.md

## Purpose

This file is for any AI agent working inside `cka-shared`.

This repo is the bridge between:
- `cka-qa`
- `cka-lab`

Its job is not to teach, quiz, or run labs directly.
Its job is to hold the current shared contract between theory and practice.

## What this repo contains

Primary contract file:
- `handoff.json`

Supporting documentation:
- `README.md`
- `WORKFLOW.md`

## Ownership rules

### `cka-qa` writes
- `theoryStatus`
- `practicalFocus`
- `lastUpdated`

### `cka-lab` writes
- `practicalFeedback`
- `lastUpdated`

## Critical system rule

Any AI modifying this repo must preserve the ownership boundary.
Do not let one lab overwrite the other lab's responsibility.

## Expected behavior

If you are updating this file on behalf of `cka-qa`:
- reflect quiz outcomes
- reflect weak or improving topics
- update practical recommendations
- respect `notYetIntroduced`

If you are updating this file on behalf of `cka-lab`:
- record practical findings
- record successful tasks
- record theory follow-up needs
- do not rewrite theory classifications

## Do not do these things

- do not turn this repo into long-form memory
- do not add unrelated notes here
- do not let practical work introduce future theory topics through this file
- do not silently overwrite another repo's owned fields

## Parent repo rule

This repo is used as a git submodule in both:
- `cka-qa`
- `cka-lab`

If you update this repo:
1. commit and push here
2. then update and commit the submodule pointer in the parent repo that made the change

If step 2 is skipped, parent repos will reference stale shared state.
