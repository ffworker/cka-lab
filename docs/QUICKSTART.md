# Quick start

CKA Lab uses the dedicated CKA scenario from
[`ffworker/proxmox-lab`](https://github.com/ffworker/proxmox-lab) for
infrastructure lifecycle. This repository owns training and learner state; the
pinned submodule owns Terraform, Cloud-Init, Ansible, and guarded teardown.

## 1. Prepare Proxmox

The scenario requires an operator-managed foundation:

- a Debian Cloud-Init template with SSH and QEMU Guest Agent support;
- VM storage;
- an isolated bridge with outbound routing and DNS;
- pool `cka-factory`;
- unused VM IDs 320 and 321;
- a scoped Proxmox API token;
- an SSH alias named `proxmox` that reaches the host non-interactively;
- capacity for about 3 vCPU, 4 GiB RAM, and two 24 GiB virtual disks.

Read the [factory guide](PROXMOX-FACTORY.md) before changing enforced IDs,
names, pool, tags, or teardown checks.

## 2. Clone both repositories

```bash
git clone --recurse-submodules https://github.com/ffworker/cka-lab.git
cd cka-lab
make requirements
make requirements-check
```

If the repository was cloned without submodules:

```bash
git submodule update --init --recursive
```

For side-by-side development, use an absolute local checkout instead:

```bash
export PROXMOX_LAB_ROOT=/absolute/path/to/proxmox-lab
```

## 3. Configure local inputs

`make requirements` creates ignored templates at:

```text
vendor/proxmox-lab/scenarios/cka-kubernetes-proxmox/terraform/terraform.tfvars
.cka-factory/proxmox.env
```

When `PROXMOX_LAB_ROOT` is set, the Terraform file is created under that
checkout instead of the submodule.

Edit `terraform.tfvars` and replace every placeholder with your endpoint, node,
template, datastore, bridge, gateway, DNS, guest addresses, administrator name,
and SSH public key.

The token file must have mode `0600` and exactly one assignment:

```text
TF_VAR_proxmox_api_token=cka-factory@pve!terraform=REPLACE_WITH_TOKEN_SECRET
```

Replace only the placeholder secret. Do not put the value in Terraform
variables, shell history, issues, or commits.

To keep individual study state local, optionally create:

```bash
cp trainer/config/learner-state.default.json \
  .cka-factory/learner-state.json
```

## 4. Provision

```bash
make lab-up
make status
```

The adapter delegates to proxmox-lab. The factory initializes Terraform, rejects
untracked collisions, creates exactly two VMs, records trusted SSH host keys,
waits for Cloud-Init, runs Ansible, opens a local API tunnel, and requires both
nodes, Flannel, and CoreDNS to become ready.

The generated kubeconfig is `.cka-factory/kubeconfig`:

```bash
export KUBECONFIG="$PWD/.cka-factory/kubeconfig"
kubectl get nodes -o wide
```

## 5. Train

```bash
make mission
make validate
make hint
make solution
make reset
make profile
```

Optional tutor:

```bash
hermes profile install ./agents/pod-professor/hermes --alias
pod-professor chat
```

## 6. Tear down

```bash
make lab-down
```

Teardown proceeds only when Terraform state and live Proxmox metadata agree on
exactly VM 320 `cka-cp01` and VM 321 `cka-worker01` with the expected pool and
tag. Partial, extra, untracked, or mismatched state fails closed.

## Troubleshooting boundary

Pod-Professor owns the learner experience, not Proxmox repair. If `make lab-up`
fails, diagnose the factory in `proxmox-lab` with an infrastructure-capable
operator or agent. Do not broaden the tutor's host access.
