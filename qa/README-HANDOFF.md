# QA to Shared Handoff Rules

Update `cka-shared/handoff.json` whenever one of these changes:
- weak topics
- improving topics
- stable topics
- unstable concepts
- practical recommendations

## Mapping rules

### weakTopics
Topics with clearly poor first-pass understanding.

### improvingTopics
Topics still shaky, but better after repetition.

### stableTopics
Topics good enough for now.

### unstableConcepts
Very specific confusion points, for example:
- scheduler vs kubelet
- Service -> Endpoints -> Pod

### practicalFocus.recommendedDrills
Must only include drills for concepts already introduced in theory.
Prefer drills that build a small working object chain, break one link, then
force diagnosis with `kubectl get`, `kubectl describe`, logs, events, and
endpoints.

### practicalFocus.notYetIntroduced
Used to prevent the lab from getting ahead of theory.
