# Practical Workflow

## Start of every lab session

1. Open `../cka-shared/handoff.json`
2. Read:
   - `theoryStatus.weakTopics`
   - `theoryStatus.unstableConcepts`
   - `practicalFocus.recommendedDrills`
   - `practicalFocus.notYetIntroduced`
3. Choose only a drill that fits already introduced theory

## End of every lab session

Update `practicalFeedback` in `../cka-shared/handoff.json`:
- `recentPracticeFindings`
- `successfulTasks`
- `theoryFollowupNeeded`

## Example practical findings
- forgot endpoints check before port checks
- mixed scheduler and kubelet in explanation
- correctly traced Deployment to ReplicaSet to Pod
