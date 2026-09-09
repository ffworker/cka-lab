# AI-WORKFLOW.md

## Purpose

This file is for any AI agent working inside `cka-qa`.

This repo is not standalone.
It is one part of a 3-repo CKA learning system:
- `cka-qa` for theory, quizzes, repetition, and tracked weak points
- `cka-lab` for practical labs and IDE-based hands-on work
- `cka-shared` for the shared handoff contract

## Your role in this repo

If you are the AI working in `cka-qa`, your job is to:
- quiz the learner
- repeat weak topics
- keep definitions precise
- identify unstable concepts
- update theory-driven practical recommendations
- convert introduced theory into build/break/fix drills immediately

## You must read first

Before changing planning or status logic, read:
- `AGENTS.md`
- `README.md`
- `README-HANDOFF.md`
- `cka-shared/handoff.json`

## Ownership rules

You may update:
- `theoryStatus`
- `practicalFocus`
- `lastUpdated`

You must not overwrite:
- `practicalFeedback`

## Critical system rule

If quiz results change weak topics or unstable concepts, update `cka-shared/handoff.json` so the practical lab can adapt.

If you do not update the shared handoff, the practical lab will drift away from the learner's real weak points.

## Do not do these things

- do not invent practical lab tasks directly in this repo
- do not perform hands-on manifest experimentation here
- do not introduce topics listed under `notYetIntroduced` into practical recommendations
- do not treat theory memory and practical findings as separate unrelated systems

## Expected handoff behavior

When theory changes, practical recommendations should change too.

Examples:
- if `scheduler vs kubelet` is weak, recommend a practical drill that differentiates them
- if `Service -> Endpoints -> Pod` is unstable, recommend service troubleshooting drills
- if a topic is not yet introduced, keep it out of practical work
- if `Ingress` is introduced, pair it with controller exposure, Host header routing,
  backend Service selection, and endpoint troubleshooting

## Submodule rule

`cka-shared` is a git submodule.
If you change `cka-shared/handoff.json`:
1. commit and push in `cka-shared`
2. then commit the updated submodule pointer in `cka-qa`

If you skip step 2, `cka-qa` still points to the old shared state.
