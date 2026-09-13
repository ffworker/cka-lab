# AI-WORKFLOW.md

## Purpose

This file is for any AI agent working inside `cka-lab`.

This repository is the standalone CKA learning system. Theory and recall live
in `qa/`; practical work lives in `labs/`, `exercises/`, `scenarios/`, and
`trainer/`; the machine-readable contract is
`docs/cka-shared/handoff.json`. No external learning repository or submodule
is required.

## Your role in this repo

If you are the AI working in `cka-lab`, your job is to:
- read the current theory state from `docs/cka-shared/handoff.json`
- build practical work from weak topics and unstable concepts
- avoid getting ahead of theory
- record practical findings back into the shared handoff
- prefer build/break/fix drills over passive explanation

## You must read first

Before proposing exercises or editing lab files, read:
- `AGENTS.md`
- `README.md`
- `docs/WORKFLOW.md`
- `docs/cka-shared/handoff.json`

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
- `theoryStatus.improvingTopics`
- `theoryStatus.stableTopics` for spaced revision
- `theoryStatus.unstableConcepts`
- `practicalFocus.recommendedDrills`
- `practicalFocus.readyForPractice`
- `practicalFocus.notYetIntroduced`
- `practicalFeedback`

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
- which link was broken and which command proved it

Examples:
- forgot to inspect endpoints before checking targetPort
- still mixes scheduler and kubelet in explanations
- correctly traced Deployment to ReplicaSet to Pod
- confused the ingress controller NodePort with the backend application Service

## Repository rule

Changes to theory, practical feedback, automation, and the handoff contract are
committed once in this repository. Never instruct the learner to commit or push
a separate `cka-qa` or `cka-shared` repository.
