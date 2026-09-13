#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec hermes profile install "$SCRIPT_DIR" --alias "$@"
