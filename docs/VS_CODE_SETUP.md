# VS Code Setup

## Goal

Use this repo as the practical IDE workspace tied to GitHub.

## Recommended setup

- open `cka-lab` as the VS Code folder
- connect it to its own GitHub repo
- initialize the `cka-shared` git submodule after cloning
- use chat inside the IDE for practical tasks only

## Important

The IDE agent should read `cka-shared/handoff.json` before suggesting drills.

## Good prompts in the IDE

- build a lab for debugging a Service with no endpoints
- create a manifest set that demonstrates Deployment -> ReplicaSet -> Pods
- create a small troubleshooting exercise for ClusterIP vs NodePort
- act as my CKA practical coach: ask one checkpoint at a time, wait for my command/output, then correct me

## Avoid prompts

- teach me entirely new theory topics not in the handoff
- ignore the notYetIntroduced list

## Input review loop (for coaching mode)

When you want the IDE assistant to review your work and guide you step-by-step:

1. Ask it to run in **checkpoint mode**:
   - one task
   - one expected command/output
   - one correction
   - next step only after your reply
2. After each step, paste one of:
   - the manifest diff
   - the exact `kubectl` command you ran
   - the terminal output you got
3. Require feedback in this order:
   - correctness (right/wrong)
   - why (root cause or concept tie-in)
   - fix command or YAML patch
   - quick re-check command

Suggested prompt:

`Use cka-shared/handoff.json and run a strict checkpoint coaching loop. I will paste output after each step. Correct me immediately and continue only when the current checkpoint is correct.`
