# Debug Lab 05 (Recovery Point Selection)

## Quick Project Snapshot
- **Current active lab:** `main` branch (right now: **Lab 05**)
- **Finished labs:** `lab/01-networking`, `lab/02-readiness`, `lab/03-persistence`, `lab/04-backup-restore`
- **Flow:** finish lab on `main` → push to `lab/NN-*` branch → scaffold next lab on `main`

Your mission: validate multi-backup restore behavior and fix one script-level bug.

## Goal
1. Create two backups at different times
2. Change data between snapshots
3. Restore expected recovery point
4. Verify restored data matches intended snapshot

## Rules (teacher mode)
1. Run scripts as-is first and capture actual behavior.
2. Don’t edit app or DB config first; inspect scripts.
3. Apply a minimal root-cause fix.
4. Verify with SQL output as proof.

## Start
```bash
cd learning-lab-01
sudo docker compose down -v
sudo docker compose up --build -d
```

## Drill commands
```bash
# reset + seed
sudo docker compose exec db psql -U postgres -d labdb -c "DROP TABLE IF EXISTS notes; CREATE TABLE notes(id serial primary key, txt text); INSERT INTO notes(txt) VALUES ('v1');"

# backup #1
./scripts/backup.sh

# update data and take backup #2
sudo docker compose exec db psql -U postgres -d labdb -c "TRUNCATE notes; INSERT INTO notes(txt) VALUES ('v2');"
./scripts/backup.sh

# simulate loss
sudo docker compose exec db psql -U postgres -d labdb -c "DROP TABLE notes;"

# restore (currently buggy)
./scripts/restore.sh

# verify
sudo docker compose exec db psql -U postgres -d labdb -c "SELECT * FROM notes;"
```

## Reporting
```bash
cp LAB_REPORT_TEMPLATE.md reports/lab-05-report.md
```
Fill report + update `LAB_TRACKER.md`.

---

## Quick Lesson Overview (update after each lab)

| Lab | Topic | Bug Type | Key Learning |
|---|---|---|---|
| 01 | Compose networking | Wrong DB host in `DATABASE_URL` | In Compose, use **service name** as hostname (`db`), not DB username (`postgres`). |
| 02 | Startup readiness | App can start before DB is ready | `depends_on` order is not enough; use **healthchecks** + `service_healthy`. |
| 03 | Persistence/volumes | Wrong DB volume mount target | Persistent DB data only survives when volume is mounted to the **actual Postgres data dir**. |
| 04 | Backup/restore | Restore script targeted wrong DB | A backup is useless unless restore is tested against the **correct target database**. |
| 05 | Recovery points | Wrong backup chosen during restore | Recovery depends on selecting the intended backup snapshot. |
