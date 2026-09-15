# Trainer

The trainer prefers ignored `.cka-factory/learner-state.json` and falls back to
the neutral `trainer/config/learner-state.default.json`. It discovers scenario
folders and stores personal progress under ignored `.cka-factory/` runtime
state. The default's readiness list describes curriculum eligibility for the
bundled missions, not an individual's assessed readiness.
Selection prioritizes weak and unstable topics, excludes `notYetIntroduced`
topics, and avoids immediate repetition. Modes are `weak`, `improving`, `stable`, `mixed`,
`troubleshooting`, `timed`, `random`, and `mock-exam`.

Use the repository-root Make targets. `lab-up` runs the Proxmox Terraform module,
Ansible kubeadm bootstrap, local API tunnel, and Ready checks. `lab-down` first
verifies the Terraform state and live VM ownership markers, then destroys only
VMs 110 and 111 (`cka-cp01` and `cka-worker01`).

The generated kubeconfig is `.cka-factory/kubeconfig`. Use it with:

    export KUBECONFIG="$PWD/.cka-factory/kubeconfig"

## Game loop

    make mission
    make validate
    make hint
    make solution
    make reset
    make profile

`mission` injects one task, records an active timer, and prints only the
briefing and success criteria. `validate` checks live Kubernetes state and
records attempts. A PASS awards the scenario's XP, evaluates the existing
achievement catalogue, updates streak and rank, records history, and prints the
next recommendation. `reset` is repeatable; on a completed mission it removes
the practice objects and active runtime state while retaining earned profile
history.
