# AI workflow for learner state

Use ignored `.cka-factory/learner-state.json` when present; otherwise start from
the neutral `trainer/config/learner-state.default.json` contract.

Before editing local learner state, determine whether the session is theory or
practical work:

- theory may update `theoryStatus`, `practicalFocus`, and `lastUpdated`;
- practical work may update `practicalFeedback` and `lastUpdated`.

Never overwrite the other ownership area. Respect `notYetIntroduced`, retain
stable topics for revision, and keep individual updates local and uncommitted.
There is no external learner-state repository or submodule workflow.
