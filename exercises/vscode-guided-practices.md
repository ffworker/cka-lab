# VS Code Guided Hands-on Practices (from `handoff.json`)

This practice pack is derived from:

- `theoryStatus.weakTopics`
- `theoryStatus.unstableConcepts`
- `practicalFocus.recommendedDrills`
- `practicalFocus.notYetIntroduced`

Source file: `cka-shared/handoff.json`.

---

## How to run this in VS Code

1. Open this repo in VS Code.
2. Open terminal in repo root.
3. Ensure cluster access works (`kubectl get nodes`).
4. Open chat and paste:

```text
Act as my strict CKA coach. Use exercises/vscode-guided-practices.md.
Run one checkpoint at a time. Wait for my pasted command/output/YAML.
Correct me with: (1) verdict, (2) why, (3) fix, (4) re-check command.
Do not introduce topics from notYetIntroduced.
```

---

## Rules for all drills

- Namespace for all tasks: `lab-guided`.
- Always show current context before changing objects.
- Prefer imperative command first, then verify with `-o wide` / `-o yaml`.
- Every checkpoint requires proof from terminal output.

Bootstrap once:

```bash
kubectl create namespace lab-guided
kubectl config set-context --current --namespace=lab-guided
```

---

## Drill 1 — Trace Deployment -> ReplicaSet -> Pods

**Maps to:**
- weak topic: Deployments
- unstable concept: current replicas vs available replicas
- recommended drill: trace Deployment -> ReplicaSet -> Pods

### Task setup

```bash
kubectl create deployment web --image=nginx:1.25 --replicas=3
```

### Checkpoint flow (coach waits after each)

1. Show Deployment summary and explain `READY` vs desired count.
   - expected command: `kubectl get deploy web`
2. Find owning ReplicaSet name.
   - expected command: `kubectl get rs`
3. Show Pods with ownership chain.
   - expected command: `kubectl get pods -o wide --show-labels`
4. Explain in one sentence:
   - Deployment responsibility
   - ReplicaSet responsibility
   - Pod responsibility
5. Simulate rollout stress:
   - command: `kubectl set image deploy/web nginx=nginx:1.26`
   - verify rollout: `kubectl rollout status deploy/web`
6. Prove old vs new ReplicaSet behavior:
   - expected command: `kubectl get rs -w` (short watch, then stop)

### Typical mistakes to catch

- mixing Deployment desired replicas with currently available replicas
- not proving ownership chain from output
- explanations that describe scheduler work as Deployment work

---

## Drill 2 — Debug Service with no Endpoints

**Maps to:**
- weak topic: Kubernetes Components (through troubleshooting flow)
- unstable concept: Service -> Endpoints -> Pod
- recommended drill: debug a Service with no endpoints

### Task setup (intentional break)

```bash
kubectl create deployment api --image=nginx:1.25 --replicas=2
kubectl expose deployment api --name api-svc --port=80 --target-port=80
kubectl patch svc api-svc -p '{"spec":{"selector":{"app":"wrong-label"}}}'
```

### Checkpoint flow

1. Confirm Service exists and selector value.
   - expected command: `kubectl get svc api-svc -o yaml`
2. Check Endpoints object.
   - expected command: `kubectl get endpoints api-svc -o yaml`
3. Inspect Pod labels and compare with selector.
   - expected command: `kubectl get pods --show-labels`
4. Apply minimal fix (change selector, not full recreate).
   - expected command: patch selector to correct label
5. Re-check Endpoints now populated.
   - expected command: `kubectl get endpoints api-svc`
6. Validate from inside cluster (optional bonus):
   - run temporary pod and `wget`/`curl` service DNS

### Typical mistakes to catch

- jumping to port checks before endpoints
- changing too many fields at once (harder root cause tracking)
- not comparing exact label key/value pairs

---

## Drill 3 — Scheduler vs Kubelet (symptom patterns)

**Maps to:**
- weak topic: Kubernetes Components
- unstable concept: scheduler vs kubelet
- recommended drill: differentiate scheduler vs kubelet from symptom patterns

### Scenario cards (answer in VS Code chat)

For each case, provide:
1. likely component
2. one confirming command
3. one immediate operator action

#### Case A
- Pod stays `Pending`
- events mention `0/1 nodes available: insufficient cpu`

#### Case B
- Pod assigned to node, then `ImagePullBackOff`

#### Case C
- Pod assigned, then `CrashLoopBackOff` with failing container command

#### Case D
- Pod pending due to unmatched `nodeSelector`

### Expected direction

- Scheduler concerns: placement decisions (`Pending`, no suitable node)
- Kubelet concerns: node-level pod execution after scheduling

### Typical mistakes to catch

- saying kubelet chooses the node
- saying scheduler handles image pulls or container runtime failures

---

## Drill 4 — ClusterIP vs NodePort troubleshooting chain

**Maps to:**
- recommended drill: compare ClusterIP vs NodePort with exact troubleshooting chain
- unstable concept: Service -> Endpoints -> Pod (applies to both types)

### Task setup

```bash
kubectl create deployment shop --image=nginx:1.25 --replicas=2
kubectl expose deployment shop --name shop-clusterip --port=80 --type=ClusterIP
kubectl expose deployment shop --name shop-nodeport --port=80 --type=NodePort
```

### Checkpoint flow

1. Show both Services and identify type-specific access path.
2. Verify selectors and endpoints for both Services.
3. Troubleshooting chain for ClusterIP failure:
   - Service object -> Endpoints -> Pod ready state -> targetPort/containerPort
4. Troubleshooting chain for NodePort failure:
   - all ClusterIP checks +
   - node IP reachability +
   - NodePort value and external path to node
5. Write a 5-line “under pressure” checklist.

### Typical mistakes to catch

- treating NodePort as bypassing endpoint selection
- skipping readiness when endpoints exist but traffic still fails

---

## Session wrap-up template (write back to shared handoff)

After completing any drill, collect practical findings and update:
- `practicalFeedback.recentPracticeFindings`
- `practicalFeedback.successfulTasks`
- `practicalFeedback.theoryFollowupNeeded`

Keep ownership boundaries:
- allowed to update: `practicalFeedback`, `lastUpdated`
- do not overwrite: `theoryStatus`, `practicalFocus`
