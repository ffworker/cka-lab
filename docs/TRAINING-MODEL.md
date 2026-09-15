# Training model

CKA Lab treats practical fluency as the result of repeated build, inspect, break, diagnose, and repair loops.

## The loop

1. The trainer reads ignored `.cka-factory/learner-state.json` when present,
   otherwise the neutral `trainer/config/learner-state.default.json`.
2. It excludes `notYetIntroduced` topics.
3. It prioritizes weak and unstable areas, with occasional stable-topic revision.
4. It avoids selecting the exact same scenario twice in a row.
5. The injector creates a controlled failure in the disposable cluster.
6. The learner works with normal Kubernetes tools.
7. The validator checks the live Kubernetes API and records the attempt.
8. A pass updates local XP, rank, achievements, streak, timing, and mission history.

Selection is intentionally simple and deterministic. The accepted CLI modes influence priority, but there is no complex recommendation model or full mock-exam session engine yet.

## Just-in-time theory

The default experience is not a broad quiz. Pod-Professor waits for an attempt, explains the smallest relevant boundary, and returns the learner to the active task. Two scenario hints provide increasing direction. The solution remains hidden until explicitly requested.

## Learning-state ownership

The learner-state contract has two ownership areas. Individual updates belong
only in ignored `.cka-factory/learner-state.json`:

- theory work updates `theoryStatus` and `practicalFocus`;
- practical work updates `practicalFeedback`.

Agents must preserve the other side's fields. Stable topics remain available for spaced revision, while `notYetIntroduced` is a hard boundary.

## Mission contract

Every playable scenario provides:

- a command-line objective with no multiple choice;
- success criteria that do not reveal the repair;
- an idempotent setup script;
- a validator for actual cluster state;
- a safe reset;
- exactly two progressive hints;
- an explicit solution file;
- an XP value and optional target time.

The current mission pack is original CKA-style practice. It does not reproduce proprietary exam questions and does not claim complete exam-domain coverage.
