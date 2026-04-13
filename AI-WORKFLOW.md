# AI-WORKFLOW.md

## Purpose

This file is for any AI agent working inside `cka-lab`.

This repo is not standalone.
It is one part of a 3-repo CKA learning system:
- `cka-qa` for theory, quizzes, repetition, and tracked weak points
- `cka-lab` for practical labs and IDE-based hands-on work
- `cka-shared` for the shared handoff contract

## Your role in this repo

If you are the AI working in `cka-lab`, your job is to:
- read the current theory state from `cka-shared/handoff.json`
- build practical work from weak topics and unstable concepts
- avoid getting ahead of theory
- record practical findings back into the shared handoff

## You must read first

Before proposing exercises or editing lab files, read:
- `AGENTS.md`
- `README.md`
- `docs/WORKFLOW.md`
- `cka-shared/handoff.json`

## Ownership rules

You may update:
- `practicalFeedback`
- `lastUpdated`

You must not overwrite:
- `theoryStatus`
- `practicalFocus`

## Critical system rule

You must derive practical work from the theory state.
Do not invent practical work in isolation.

Priority sources are:
- `theoryStatus.weakTopics`
- `theoryStatus.unstableConcepts`
- `practicalFocus.recommendedDrills`
- `practicalFocus.notYetIntroduced`

## Do not do these things

- do not practice topics listed in `notYetIntroduced`
- do not rewrite theory classifications
- do not ignore the shared handoff and improvise an unrelated lab
- do not treat practical findings as local-only information

## Expected feedback behavior

After practical work, write back things like:
- recurring mistakes
- what drills succeeded
- what theory needs reinforcement

Examples:
- forgot to inspect endpoints before checking targetPort
- still mixes scheduler and kubelet in explanations
- correctly traced Deployment to ReplicaSet to Pod

## Submodule rule

`cka-shared` is a git submodule.
If you change `cka-shared/handoff.json`:
1. commit and push in `cka-shared`
2. then commit the updated submodule pointer in `cka-lab`

If you skip step 2, `cka-lab` still points to the old shared state.
