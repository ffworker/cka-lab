#!/usr/bin/env bash
set -euo pipefail
repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
learner_state="$repo_root/.cka-factory/learner-state.json"
if [[ -f "$learner_state" ]]; then
    exec cat "$learner_state"
fi
exec cat "$repo_root/trainer/config/learner-state.default.json"
