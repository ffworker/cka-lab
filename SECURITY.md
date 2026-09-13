# Security policy

CKA Lab controls disposable virtual machines and executes scripts against a Kubernetes cluster. Treat factory credentials and local runtime files as sensitive.

## Report a vulnerability

Do not open a public issue for a credential leak, unsafe teardown path, command-injection bug, or scenario reset that can affect resources outside its ownership boundary.

Use GitHub's private vulnerability reporting for this repository when available. If that option is unavailable, contact the repository owner through their GitHub profile and disclose only enough detail to establish a private channel. Do not include live tokens, private keys, kubeconfig, Terraform state, or host details in the first message.

## Sensitive local files

Never commit:

- `.cka-factory/`;
- `.env` or auth files;
- Terraform state or local tfvars;
- kubeconfig and generated inventory;
- SSH private keys or generated known-host files;
- Hermes memory, sessions, logs, or state databases.

If a real secret reaches Git, revoke it first. Removing the current file does not erase it from Git history.

## Safety invariants

Factory teardown must remain limited to the exact two owned CKA guests. Scenario reset must remain limited to the scenario's owned namespace or explicitly documented cluster-scoped object. Changes that weaken either invariant should be treated as security-sensitive.

## Supported versions

There is no formal security-support or release-version policy yet. The default branch is the maintained line while the project remains pre-release.
