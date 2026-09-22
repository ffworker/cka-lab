#!/usr/bin/env bash
set -euo pipefail

ACTION=${1:?usage: lab-factory.sh lab-up|lab-down [runtime-dir]}
REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RUNTIME_DIR=${2:-"$REPO/.cka-factory"}

case "$ACTION" in
  lab-up|lab-down) ;;
  *)
    printf 'cka-lab: unsupported factory action: %s\n' "$ACTION" >&2
    exit 1
    ;;
esac

if [[ -n "${PROXMOX_LAB_ROOT:-}" ]]; then
  [[ "$PROXMOX_LAB_ROOT" == /* ]] || {
    printf 'cka-lab: PROXMOX_LAB_ROOT must be an absolute path\n' >&2
    exit 1
  }
  PROXMOX_ROOT=$PROXMOX_LAB_ROOT
else
  PROXMOX_ROOT="$REPO/vendor/proxmox-lab"
fi

FACTORY="$PROXMOX_ROOT/scenarios/cka-kubernetes-proxmox/scripts/lab-factory.sh"
if [[ ! -x "$FACTORY" ]]; then
  printf 'cka-lab: missing Proxmox factory: %s\n' "$FACTORY" >&2
  printf 'Initialize the pinned dependency with: git submodule update --init --recursive\n' >&2
  printf 'Or set PROXMOX_LAB_ROOT to an absolute proxmox-lab checkout path.\n' >&2
  exit 1
fi

exec "$FACTORY" "$ACTION" "$RUNTIME_DIR"
