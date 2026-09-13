# Disposable Proxmox cluster factory

This module defines two stopped VMs: `cka-cp01` (2 vCPU, 2 GiB) and
`cka-worker01` (1 vCPU, 2 GiB). It targets a dedicated cloud-init template and
never references or manages existing training VMs.

Copy `terraform.tfvars.example` to an ignored local `.tfvars` file, replace the
documentation-only addresses and template ID, and provide the token only through
`TF_VAR_proxmox_api_token`. Provisioning is intentionally not wired into the
trainer skeleton yet.
