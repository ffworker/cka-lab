# Lab Tracker

| Lab | Status | Main Bug Type | Time | Key Learning | Next Focus |
|---|---|---|---|---|---|
| 01 | ✅ Archived | Compose DNS host mismatch | ~30-40 min | Service name is DB host | startup readiness |
| 02 | ✅ Archived | startup timing/readiness | ~25-35 min | depends_on order != readiness; use healthcheck | persistence |
| 03 | ✅ Closed | wrong volume mount target | ~15-20 min | Mount volume to real DB data dir (`/var/lib/postgresql/data`) | backup + restore drill |
| 04 | ✅ Archived | restore script targets wrong DB | ~10 min | backup is only valid if restore works on correct target | failure recovery discipline |
| 05 | 🚧 In Progress | restore selects wrong recovery point |  | newest valid backup must be selected intentionally | incident rollback confidence |

## Notes
- Lab 01 branch: `lab/01-networking`
- Lab 02 branch: `lab/02-readiness`
- Keep healthchecks as default baseline for service dependencies.
- `main` always contains the active lab.
