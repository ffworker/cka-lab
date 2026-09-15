# Internal learning-state contract

`trainer/config/learner-state.default.json` is the neutral contract that aligns
theory and practical training inside this repository. A personalized copy may
live at ignored `.cka-factory/learner-state.json`; it must never be committed.

## Ownership

- Theory work in `qa/` updates local `theoryStatus` and `practicalFocus`.
- Practical work updates local `practicalFeedback`.
- Either side may update `lastUpdated` with the corresponding change.

Preserve the other side's fields. Keep the contract compact and
machine-readable. Stable topics remain eligible for spaced revision.

Only generic contract changes are committed. Individual assessments and
feedback remain local.
