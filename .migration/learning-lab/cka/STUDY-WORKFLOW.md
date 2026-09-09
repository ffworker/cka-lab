# CKA Study Workflow

## One repository, four concerns

The old repository split is retained only as pinned source snapshots. Day-to-day learning should now happen from this directory.

| Concern | Source material | Purpose |
|---|---|---|
| Theory | `source-snapshots/cka-qa/` | Exact definitions, recall and weak-topic tracking |
| Practice | `source-snapshots/cka-lab/` | Manifest work and controlled break/fix exercises |
| Troubleshooting | `source-snapshots/cka-lab-notes/` | Fast diagnosis paths and kubectl references |
| State | `source-snapshots/cka-shared/handoff.json` | Current focus, unstable concepts and recommended drills |

## Start of a study session

1. Read `source-snapshots/cka-shared/handoff.json`.
2. Select one introduced topic from weak, improving or recommended-practice areas.
3. Review the relevant course note only far enough to establish the correct component boundary.
4. Choose or create one small practical drill.

Do not start with a large multi-service scenario. A drill should test one relationship clearly.

## Default drill shape

1. **Build** — create the smallest working object chain.
2. **Verify** — prove the happy path.
3. **Inspect** — inspect generated/backing objects.
4. **Break** — change one selector, port, label, path, permission or dependency.
5. **Diagnose** — work from symptoms toward the broken link.
6. **Fix** — apply the minimal repair.
7. **Explain** — describe why the failure occurred.

## Preferred troubleshooting order

```text
Node -> Pod -> Container -> Volume -> Network -> Access policy
```

Within a Kubernetes request path, follow the actual object chain. Examples:

```text
Deployment -> ReplicaSet -> Pod
Service -> EndpointSlice/Endpoints -> Pod
Ingress controller -> Ingress rule -> Service -> EndpointSlice/Endpoints -> Pod
PVC -> PV -> StorageClass / backing storage
User or ServiceAccount -> RBAC binding -> Role/ClusterRole -> API object
```

## Evidence commands

Use exam-safe commands before changing anything:

```bash
kubectl get <resource> -A -o wide
kubectl describe <resource> <name> -n <namespace>
kubectl get events -A --sort-by=.lastTimestamp
kubectl logs <pod> -n <namespace>
kubectl get endpoints,endpointslices -A
kubectl get pods -A --show-labels
kubectl auth can-i <verb> <resource> --as <identity>
```

## End of a session

Record:

- what was built
- the exact broken link
- the symptom that exposed it
- the command that proved the root cause
- the minimal fix
- the concept that still needs repetition

The old source snapshots remain read-only references. New consolidated notes and exercises should be added directly under `cka/`.
