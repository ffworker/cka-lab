# AI workflow for the internal handoff

The contract is `docs/cka-shared/handoff.json` inside `cka-lab`.

Before editing it, determine whether the session is theory or practical work:

- theory may update `theoryStatus`, `practicalFocus`, and `lastUpdated`;
- practical work may update `practicalFeedback` and `lastUpdated`.

Never overwrite the other ownership area. Respect `notYetIntroduced`, retain
stable topics for revision, and commit the change once in this repository.
There is no external handoff repository or submodule workflow.
