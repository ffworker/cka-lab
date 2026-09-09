# Lab 04 Report

## Metadata
- Lab: 04 (Backup & Restore Drill)
- Date: 2026-03-16
- Duration: ~10 min

## Objective
Validate backup + restore flow end-to-end and repair the restore failure.

## Symptom
Backup completed, but restore did not recover expected data into the target database.

## Investigation steps
1. Reviewed backup and restore scripts side-by-side.
2. Compared dump source database with restore target database.
3. Confirmed mismatch in restore target.

## Root cause
`restore.sh` restored into `appdb` while backups were created from `labdb`.

## Fix
- File: `scripts/restore.sh`
- Before: `... psql -U postgres -d appdb`
- After: `... psql -U postgres -d labdb`
- Why: restore target must match backup source database.

## Verification
Restore now targets the correct database and completes against `labdb`.

## Learning
- Technical: Backup and restore scripts must be validated as a pair.
- Process: Always compare source and target identifiers, not only command success.
- Reusable rule: A backup is only real when restore is tested to the correct destination.
