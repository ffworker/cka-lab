# IN PLANNING: Raspberry Pi 5 media-stack migration to Kubernetes

## Goal

Later, use `cka-lab` to turn the user's old Docker Compose based media-stack on a Raspberry Pi 5 into a cleaner Kubernetes setup.

## Desired direction

- use current Kubernetes manifests as the starting point
- improve them toward better practice
- document the reasoning and architecture clearly
- use the practical lab as the place where learning meets the real stack

## Why this matters

This project can become the bridge between:
- theory learned in `cka-qa`
- practical implementation in `cka-lab`

## Planned outcomes

- review current manifests
- identify anti-patterns and weak spots
- improve manifests toward maintainable best practice
- document services, dependencies, secrets/config, storage, and exposure
- use the stack as a long-term learning lab

## Not for now

This is intentionally marked as planning only.
Do not start building this until the user asks to begin the migration work.

## Future drill alignment

When the user is ready, practical work should tie back to studied topics such as:
- Deployments
- Services
- Secrets
- Config via env vars
- Multi-container Pods or init containers when justified
- Resource requests/limits
- Scaling concepts where relevant
- Backup and restore thinking
