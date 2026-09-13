# Internal learning-state contract

`docs/cka-shared/handoff.json` aligns theory and practical training inside the
single `cka-lab` repository. It is an ordinary tracked file, not a repository or
submodule.

## Ownership

- Theory work in `qa/` updates `theoryStatus` and `practicalFocus`.
- Practical work updates `practicalFeedback`.
- Either side may update `lastUpdated` with the corresponding change.

Preserve the other side's fields. Keep the contract compact and
machine-readable. Stable topics remain eligible for spaced revision.

All updates are committed once at the `cka-lab` repository root.
