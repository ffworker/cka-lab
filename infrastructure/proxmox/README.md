# Disposable Proxmox cluster factory

This module defines two VMs: `cka-cp01` (2 vCPU, 2 GiB) and
`cka-worker01` (1 vCPU, 2 GiB). It targets a dedicated cloud-init template and
never references or manages existing training VMs.

Local values live in ignored `terraform.tfvars`; the API token is loaded from
ignored mode-0600 `.cka-factory/proxmox.env`. The configured `admin_username`
is used consistently for cloud-init, SSH, and Ansible. The module uses dedicated
pool
`cka-factory`, template 9000, bridge `vmbr1`, and reserved IDs 110 and 111.

Do not import unrelated VMs into this state. `scripts/lab-factory.sh` refuses
collisions and teardown unless state, names, IDs, pool, and `cka-factory` tags
agree.

The dedicated `cka-factory@pve!terraform` token needs the existing scoped
Terraform node, pool, storage, clone, guest-agent audit, and `vmbr1` SDN-use
permissions. Keep the token only in `.cka-factory/proxmox.env`; never place it
in tfvars or Git.

Public setup instructions and current limitations are documented in
[`docs/PROXMOX-FACTORY.md`](../../docs/PROXMOX-FACTORY.md).
