# Scenarios

The first mission pack contains eight original CKA-style practical tasks based
on the learner-state contract and ready-for-practice topics. Each directory contains
schema-valid metadata, an idempotent injector, a cluster-state validator, a
namespace-scoped reset, two progressive hints, and an explicit solution.

Mission briefings contain symptoms, objectives, and success criteria but never
the diagnosis or repair commands. Runtime selection excludes anything listed in
`notYetIntroduced`, prioritizes weak and unstable topics, and avoids immediate
scenario repetition.

Scenario scripts must operate only on their named `cka-mission-*` namespace.
The taints mission is the sole node-scoped exception; its reset removes only the
exact `training` taint it owns from `cka-worker01`.
