# Practical Workflow

## Start of every lab session

1. Open `cka-shared/handoff.json`
2. Read:
   - `theoryStatus.weakTopics`
   - `theoryStatus.unstableConcepts`
   - `practicalFocus.recommendedDrills`
   - `practicalFocus.notYetIntroduced`
3. Choose only a drill that fits already introduced theory

## Drill shape

Use this shape by default:

1. build the object chain
2. verify the happy path
3. inspect the backing objects
4. break exactly one thing
5. diagnose from symptoms to root cause
6. repair it
7. explain the component boundary

For networking, the preferred chain is:

```text
Ingress controller exposure -> Ingress rule -> Service -> Endpoints -> Pods
```

## End of every lab session

Update `practicalFeedback` in `cka-shared/handoff.json`:
- `recentPracticeFindings`
- `successfulTasks`
- `theoryFollowupNeeded`

## Example practical findings
- forgot endpoints check before port checks
- mixed scheduler and kubelet in explanation
- correctly traced Deployment to ReplicaSet to Pod
- routed traffic through the ingress controller NodePort but explained that the
  Ingress backend points to a Service, not directly to Pods
