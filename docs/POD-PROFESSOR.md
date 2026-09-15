# Pod-Professor

Pod-Professor is CKA Lab's learner-facing tutor. The repository owns its teaching contract, so the tutor follows the same learning state and mission rules as the CLI.

## Install

The current adapter targets Hermes Agent `>=0.21.0`:

```bash
hermes profile install ./agents/pod-professor/hermes --alias
```

The included wrapper performs the same installation:

```bash
./agents/pod-professor/hermes/install.sh
```

Configure model credentials in the installed profile when Hermes requests them. No credentials ship with this repository.

Start from the repository root:

```bash
pod-professor chat
```

## Practical-first behavior

Phrases such as `practice`, `mission`, `let's train`, `CKA task`, `hands on`, and `continue` send Pod-Professor into the trainer loop. It:

1. reads ignored local learner state when present, otherwise the neutral
   tracked default, plus the local trainer profile;
2. checks cluster status;
3. uses `make lab-up` only when the lab is absent;
4. starts or resumes a mission;
5. presents only the briefing and success criteria;
6. lets the learner operate the cluster;
7. validates when asked;
8. reveals hints progressively;
9. reports trainer-owned XP, achievements, rank, and recommendations.

The tutor can discuss pasted commands and output, but it should not silently solve an active mission. It gives short theory repairs after an attempt and then returns to practice.

## Privacy

The distribution source contains behavior only. Each installed Hermes profile keeps its auth, memory, sessions, logs, and model configuration outside the repository. Trainer XP and mission history stay in ignored `.cka-factory/` runtime files.

## Infrastructure boundary

Pod-Professor may call the documented factory commands and inspect kubectl-visible training state. It must not inventory or manually configure the Proxmox host. If `make lab-up` breaks, factory repair moves to a main infrastructure-agent session.

The provider-neutral contract is in `agents/pod-professor/AGENT.md` and `agents/pod-professor/TEACHING.md`. Hermes is the only adapter shipped today.
