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

## Training Factory

The factory provisions an isolated, disposable two-node kubeadm cluster on
`proxmox.example`, bootstraps it with Ansible, and exposes its kubeconfig through the
local runtime directory. Eight practical missions are available through the
trainer.

Run `make lab-up` to create or reconcile the cluster and `make lab-down` to
destroy only factory-owned resources. The main infrastructure agent owns
factory maintenance and failures; tutor sessions consume the resulting cluster.

Use `make mission`, `make validate`, `make hint`, `make solution`, `make reset`,
and `make profile` for the playable loop. Pod-Professor owns the learner
experience and normally drives these commands; it delegates broken factory
infrastructure back to the main infrastructure agent.
