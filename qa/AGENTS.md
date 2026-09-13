# AGENTS.md

## Role

This directory is the strict theory and recall area for CKA.

Priorities:
1. exact definitions
2. short answers
3. concept boundaries
4. weak-topic repetition
5. progress tracking

## Allowed work

- quizzes
- repetition
- topic updates
- study status
- recording quiz findings
- writing theory state to `docs/cka-shared/handoff.json`

## System awareness

This directory is part of the self-contained `cka-lab` repository. Theory and
recall live in `qa/`; practical training lives in `labs/`, `exercises/`, and
future `scenarios/` and `trainer/`; the learning-state contract lives at
`docs/cka-shared/handoff.json`.

When theory findings change, update the internal handoff so practical training
can target the right drills.

## Ownership rules

Theory work may update:
- `theoryStatus`
- `practicalFocus`
- `lastUpdated`

Theory work must not overwrite:
- `practicalFeedback`

## Avoid

- practical lab setup
- broad experimentation
- YAML sandbox work
- mixing theory with hands-on clutter
- introducing practical drills for topics listed in `notYetIntroduced`

## Output style

- concise
- critical when needed
- optimize for correctness over comfort
