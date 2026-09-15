# AGENTS.md

## Role

This repository is the complete CKA learning system. `qa/` owns theory and
recall; practical training lives under `labs/`, `exercises/`, `scenarios/`, and
`trainer/`; automation lives under `infrastructure/`, `ansible/`,
`environments/`, and `scripts/`.

Priorities:
1. hands-on repetition
2. troubleshooting flow
3. kubectl speed
4. manifest accuracy
5. feedback back into theory

## Allowed work

- create lab manifests
- run practical exercises
- inspect objects
- write practical findings to ignored `.cka-factory/learner-state.json`

## System awareness

This is one self-contained repository. There is no operational dependency on
an external `cka-qa` repository, `cka-shared` repository, or submodule.

Before proposing or building practical work, read
`.cka-factory/learner-state.json` when it exists; otherwise use the neutral
`trainer/config/learner-state.default.json`. Respect:
- `weakTopics`
- `improvingTopics`
- `stableTopics` (still eligible for spaced revision)
- `unstableConcepts`
- `recommendedDrills`
- `readyForPractice`
- `notYetIntroduced`
- `practicalFeedback`

## Ownership rules

Personal learner state may update:
- `practicalFeedback`
- `lastUpdated`

Practical work must not overwrite these learner-owned fields:
- `theoryStatus`
- `practicalFocus`

## Avoid

- introducing theory topics not yet covered
- committing personal learner state or findings
- bypassing the learner-state contract

## Lab rule

Every exercise should map back to one of:
- weak topics
- improving topics
- stable topics selected for revision
- unstable concepts
- recommended practical drills
