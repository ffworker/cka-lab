# AGENTS.md

## Role

This repo is the practical CKA lab.

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
- write practical findings to `cka-shared/handoff.json`

## System awareness

This repo is part of a 3-repo workflow:
- `cka-qa` decides what is weak, improving, stable, or not yet introduced
- `cka-lab` turns those signals into practical work
- `cka-shared` is the contract bridge

Before proposing or building practical work, read `cka-shared/handoff.json` and respect:
- `weakTopics`
- `unstableConcepts`
- `recommendedDrills`
- `notYetIntroduced`

## Ownership rules

This repo may update:
- `practicalFeedback`
- `lastUpdated`

This repo must not overwrite:
- `theoryStatus`
- `practicalFocus`

## Avoid

- introducing theory topics not yet covered
- overwriting theory ownership fields in the shared handoff
- turning this repo into the study tracker

## Lab rule

Every exercise should map back to one of:
- weak topics
- unstable concepts
- recommended practical drills
