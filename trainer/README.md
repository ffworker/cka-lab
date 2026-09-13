# Trainer skeleton

The trainer reads `docs/cka-shared/handoff.json`, discovers future scenario
folders, and stores local progress under ignored `.cka-factory/` runtime state.
Selection modes are `weak`, `improving`, `stable`, `mixed`, `troubleshooting`,
`timed`, `random`, and `mock-exam`. Weighting is intentionally deferred.

Use the repository-root Make targets. `lab-up` and `lab-down` are safe skeleton
responses and do not touch Proxmox yet.
