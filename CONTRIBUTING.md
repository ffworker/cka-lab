# Contributing

CKA Lab favors small changes that improve hands-on repetition, troubleshooting flow, kubectl speed, manifest accuracy, or learning feedback.

## Before changing anything

1. Read `AGENTS.md`.
2. Read `docs/cka-shared/handoff.json` before adding practical work.
3. Keep topics in `notYetIntroduced` out of missions.
4. Preserve ownership boundaries in the learning-state contract.

## Mission changes

A mission needs schema-valid metadata, safe repeatable setup and reset, two progressive hints, a hidden solution, and a validator that checks actual cluster state. Namespace-scope all objects unless a narrowly documented cluster-scoped resource is essential.

Do not submit leaked or reconstructed exam questions. Write equivalent original practice tasks.

## Factory changes

Treat VM IDs, names, pool, bridge, tags, Terraform state, and live ownership checks as one safety boundary. A change to one usually requires corresponding validation and teardown updates. Never broaden destroy behavior for convenience.

## Verify

Run the cheapest relevant checks:

```bash
python3 -m pytest -q
terraform -chdir=infrastructure/proxmox fmt -check
terraform -chdir=infrastructure/proxmox validate
ANSIBLE_CONFIG=ansible/ansible.cfg \
  ansible-playbook -i ansible/inventory.example.yml ansible/site.yml --syntax-check
```

For documentation changes, check relative links and render Mermaid blocks on GitHub before merging.

## Pull requests

Explain what learner or operator problem the change fixes, what you ran, and any behavior that remains experimental. Keep runtime files, credentials, local Terraform variables, state, kubeconfig, and learner profiles out of the diff.

## License note

The repository does not currently have a repository-wide license. Discuss licensing with the maintainer before contributing substantial reusable code.
