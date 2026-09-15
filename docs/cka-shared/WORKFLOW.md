# Learner-state workflow

At the start of theory or practical work, read ignored
`.cka-factory/learner-state.json` when present; otherwise use
`trainer/config/learner-state.default.json`.

Theory work reads practical feedback and may update only theory-owned fields.
Practical work reads weak, improving, stable, and unstable topics plus practical
focus, then may update only practical feedback.

Use build/break/fix/explain once a topic is introduced. `notYetIntroduced`
remains a hard boundary. Keep individual state local; commit only generic
curriculum or project changes.
