# AI-WORKFLOW.md

## Purpose

This file is for any AI agent working inside `cka-lab`.

This repository is the standalone CKA learning system. Theory and recall live
in `qa/`; practical work lives in `labs/`, `exercises/`, `scenarios/`, and
`trainer/`; the machine-readable contract is
`trainer/config/learner-state.default.json`; an optional personalized copy lives
at ignored `.cka-factory/learner-state.json`. No external learning repository or
submodule is required.

## Your role in this repo

If you are the AI working in `cka-lab`, your job is to:
- read `.cka-factory/learner-state.json` when present, otherwise use the neutral default
- build practical work from weak topics and unstable concepts
- avoid getting ahead of theory
- record practical findings only in ignored local learner state
- prefer build/break/fix drills over passive explanation

## You must read first

Before proposing exercises or editing lab files, read:
- `AGENTS.md`
- `README.md`
- `docs/WORKFLOW.md`
- `.cka-factory/learner-state.json` when present, otherwise
  `trainer/config/learner-state.default.json`

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
- do not ignore learner state and improvise an unrelated lab
- do not commit individual assessments or practical findings

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

Generic curriculum and automation changes are committed in this repository.
Individual theory classifications and practical feedback remain local and
ignored. Never instruct the learner to commit or push personal state.
