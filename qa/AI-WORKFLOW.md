# AI workflow for theory and recall

This file applies to AI work inside `qa/` in the standalone `cka-lab`
repository.

## Role

- quiz the learner
- repeat weak and improving topics
- keep definitions precise
- identify unstable concepts
- keep stable topics eligible for spaced revision
- turn introduced theory into practical recommendations

## Read first

- repository-root `AGENTS.md`
- `qa/AGENTS.md`
- `qa/README.md`
- `qa/README-HANDOFF.md`
- `.cka-factory/learner-state.json` when present, otherwise
  `trainer/config/learner-state.default.json`

## Ownership

Theory work may update `theoryStatus`, `practicalFocus`, and `lastUpdated`. It
must not overwrite `practicalFeedback`.

If quiz results change weak topics or unstable concepts, update ignored local
learner state so practical training can adapt. Respect `notYetIntroduced`.

## Repository rule

Keep individual theory state uncommitted. Never require a separate `cka-qa` or
`cka-shared` repository or submodule commit.
