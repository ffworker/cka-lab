# Quick start

CKA Lab's current backend provisions two kubeadm nodes on Proxmox VE. The setup is deliberately opinionated and requires local configuration before the first run.

## 1. Check the prerequisites

The bundled installer in step 2 installs the local tools below through the
detected `apt-get`, `dnf`, `pacman`, or `zypper` package manager. If your
distribution does not package Terraform or kubectl, it prints the official
installation page for the missing command.

The Linux workstation needs:

- Bash, Python 3, GNU Make, and OpenSSH
- Terraform
- Ansible
- kubectl
- Git
- Hermes Agent `>=0.21.0` only if you want Pod-Professor

On Proxmox, prepare:

- a cloud-init Linux template with the QEMU guest agent and SSH server (the example uses VM ID `9000`);
- storage available to the factory (the example uses `local-lvm`);
- an isolated bridge named `vmbr1` with outbound routing and DNS reachability;
- a pool named `cka-factory`;
- unused VM IDs `110` and `111`;
- a scoped token named `cka-factory@pve!terraform`;
- enough free capacity for roughly 3 vCPU, 4 GiB RAM, and two 24 GiB virtual disks.

The factory currently expects an SSH host alias named `proxmox`. Configure it in `~/.ssh/config` so `ssh proxmox` reaches the Proxmox host without interactive authentication.

The guest names, pool, bridge, and destination VM IDs are safety boundaries in
the current implementation, not generic defaults. Template ID, datastore, node
name, addresses, and admin username are local inputs. Read
[the factory guide](PROXMOX-FACTORY.md) before changing enforced values.

## 2. Clone and configure

```bash
git clone https://github.com/ffworker/cka-lab.git
cd cka-lab
make requirements
make requirements-check
```

The installer creates the ignored `terraform.tfvars` and `.cka-factory/proxmox.env`
templates. Edit the `terraform.tfvars` file. Review the endpoint, Proxmox node,
template, datastore, and guest username, then replace every placeholder with
values from your isolated lab network and the public SSH key that should be
installed in the guests. The example deliberately contains no working address
or key.

Create the ignored runtime directory and token file:

```bash
mkdir -p .cka-factory
chmod 700 .cka-factory
install -m 600 /dev/null .cka-factory/proxmox.env
$EDITOR .cka-factory/proxmox.env
chmod 600 .cka-factory/proxmox.env
```

Add exactly one line in the editor:

```text
TF_VAR_proxmox_api_token=cka-factory@pve!terraform=REPLACE_WITH_TOKEN_SECRET
```

Replace only `REPLACE_WITH_TOKEN_SECRET`. Do not put this value in Terraform
variables, shell history, issues, or commits.

The token needs enough scoped Proxmox permissions to clone the configured
template, use the configured storage and `vmbr1`, read guest-agent data, and
manage guests in the `cka-factory` pool. Token and ACL creation are currently
operator-managed; the repository does not automate them.

To keep individual study state local, optionally create a personal copy of the
neutral curriculum baseline:

```bash
cp trainer/config/learner-state.default.json \
  .cka-factory/learner-state.json
```

The trainer prefers this ignored local file when it exists and otherwise uses
the tracked neutral default.

## 3. Provision the cluster

```bash
make lab-up
make status
```

`lab-up` initializes Terraform, verifies its ownership boundary, creates or reconciles the two VMs, runs Ansible, opens a local API tunnel, and waits for both Kubernetes nodes, Flannel, and CoreDNS.

The generated kubeconfig is `.cka-factory/kubeconfig`. To work directly:

```bash
export KUBECONFIG="$PWD/.cka-factory/kubeconfig"
kubectl get nodes -o wide
```

## 4. Start training

Without an AI tutor:

```bash
make mission
# Work in another terminal with kubectl or YAML.
make validate
make hint       # only when wanted
make solution   # explicit spoiler
make reset
make profile
```

With Pod-Professor:

```bash
hermes profile install ./agents/pod-professor/hermes --alias
pod-professor chat
```

Then say `Start a mission`.

## 5. Tear down safely

```bash
make lab-down
```

Teardown proceeds only when Terraform state and live Proxmox metadata identify exactly the two factory VMs. It refuses partial, extra, untracked, or mismatched state.

## Troubleshooting boundary

Pod-Professor owns the learner experience, not Proxmox repair. If `make lab-up` itself fails, leave the tutor session and diagnose the factory with an infrastructure-capable agent or operator. Do not broaden Pod-Professor's access to the host.
