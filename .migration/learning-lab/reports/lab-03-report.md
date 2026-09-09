# Lab 03 Report

## Metadata
- Lab: 03
- Date: 2026-03-13
- Duration: ~15-20 min

## Objective
Validate persistence and fix wrong volume mapping for Postgres.

## Symptom
Data did not reliably persist across container recreation because the volume was mapped to a non-data directory.

## Investigation steps
1. Ran persistence test flow (insert row, down/up, verify).
2. Inspected `docker-compose.yml` db volume target.
3. Compared target with expected Postgres data directory.

## Root cause
`db_data` volume mounted to `/var/lib/postgresql/backup` instead of `/var/lib/postgresql/data`.

## Fix
- File: `docker-compose.yml`
- Before: `db_data:/var/lib/postgresql/backup`
- After: `db_data:/var/lib/postgresql/data`
- Why: Postgres stores live DB files in `/var/lib/postgresql/data`.

## Verification
- Health endpoint remained healthy.
- Persistence test passed after `down` + `up` (without `-v`).

## Learning
- Technical: Volume target path must match actual app data directory.
- Process: Always verify persistence with a write → restart → read loop.
- Reusable rule: "If persistence fails, verify the mount target path before anything else."
