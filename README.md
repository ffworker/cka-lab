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
├── scenarios/
├── trainer/
├── infrastructure/
├── ansible/
└── docs/
```

Read `qa/README.md` for theory work, `README.md` files under `notes/` and
`labs/debug-labs/` for their workflows, and `docs/cka-shared/handoff.json`
for the current machine-readable study state. Shared state is intentionally
stored directly in this repository; there is no submodule dependency.

This is a learning workspace, not a product repository. Use Linear for
requested learning work, but do not route it through normal product CD.

## Training Factory skeleton

The reusable skeleton includes a stopped-by-default two-node Proxmox definition,
kubeadm Ansible role boundaries, a scenario contract, a local trainer/profile,
and Make targets. It contains no curriculum or real CKA scenarios yet.

Run `make status`, `make mission`, or `make profile` locally. Infrastructure
targets remain non-operative skeleton responses until explicit provisioning is
wired in.
