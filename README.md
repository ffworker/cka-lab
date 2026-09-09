# cka-lab

Consolidated CKA learning workspace for theory, practical exercises,
troubleshooting notes, and disposable debug labs.

## Structure

```text
cka-lab/
├── labs/
├── exercises/
├── qa/
├── notes/
├── environments/
├── scripts/
└── docs/
```

Read `qa/README.md` for theory work, `README.md` files under `notes/` and
`labs/debug-labs/` for their workflows, and `docs/cka-shared/handoff.json`
for the current machine-readable study state. Shared state is intentionally
stored directly in this repository; there is no submodule dependency.

This is a learning workspace, not a product repository. Use Linear for
requested learning work, but do not route it through normal product CD.
