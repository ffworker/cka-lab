#!/usr/bin/env bash
set -euo pipefail
LATEST="$(ls -1tr backups/labdb-*.sql | head -n1)"
if [[ -z "${LATEST:-}" ]]; then
  echo "[restore] no backup file found"
  exit 1
fi
echo "[restore] restoring from $LATEST"
# INTENTIONAL LAB BUG: restore targets wrong database name
cat "$LATEST" | sudo docker compose exec -T db psql -U postgres -d labdb
echo "[restore] done"
