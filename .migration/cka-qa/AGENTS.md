# AGENTS.md

## Role

This repo is the strict theory lab for CKA.

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
- writing to `cka-shared/handoff.json`

## System awareness

This repo is part of a 3-repo workflow:
- `cka-qa` owns theory tracking
- `cka-lab` owns practical execution feedback
- `cka-shared` is the contract bridge

When theory findings change, update `cka-shared/handoff.json` so the practical lab can target the right drills.

## Ownership rules

This repo may update:
- `theoryStatus`
- `practicalFocus`
- `lastUpdated`

This repo must not overwrite:
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
