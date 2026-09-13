# Trainer

The trainer reads `docs/cka-shared/handoff.json`, discovers future scenario
folders, and stores local progress under ignored `.cka-factory/` runtime state.
Selection modes are `weak`, `improving`, `stable`, `mixed`, `troubleshooting`,
`timed`, `random`, and `mock-exam`. Weighting is intentionally deferred.

Use the repository-root Make targets. `lab-up` runs the Proxmox Terraform module,
Ansible kubeadm bootstrap, local API tunnel, and Ready checks. `lab-down` first
verifies the Terraform state and live VM ownership markers, then destroys only
VMs 110 and 111 (`cka-cp01` and `cka-worker01`).

The generated kubeconfig is `.cka-factory/kubeconfig`. Use it with:

    export KUBECONFIG="$PWD/.cka-factory/kubeconfig"
