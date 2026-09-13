# Pod-Professor

The provider-neutral tutor contract lives in `AGENT.md` and `TEACHING.md`. The `hermes/` directory is the Hermes profile-distribution adapter.

## Install

From the cloned `cka-lab` repository root:

    hermes profile install ./agents/pod-professor/hermes --alias

Or run:

    ./agents/pod-professor/hermes/install.sh

Configure model credentials in the installed profile when Hermes requests them; credentials are not included here.

## Start

From the repository root:

    pod-professor chat

Each installation receives private memory, sessions, credentials, and runtime state under that user's Hermes profile directory. Repository learning state remains authoritative. Local trainer XP and mission history remain under ignored `.cka-factory/`.

Pod-Professor consumes the disposable cluster through `make lab-up`,
`make lab-down`, trainer commands, and kubectl. Factory repair and direct proxmox.example
work belong to the main infrastructure agent, not the tutor session.
