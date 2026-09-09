#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups
TS="$(date +%Y%m%d-%H%M%S)"
OUT="backups/labdb-${TS}.sql"
echo "[backup] writing $OUT"
sudo docker compose exec -T db pg_dump -U postgres -d labdb > "$OUT"
echo "[backup] done"
