# Shared Workflow

## Purpose

`cka-shared` keeps theory and practice aligned.

- `cka-qa` writes theory status and practical focus
- `cka-lab` writes practical feedback

The preferred learning loop is build/break/fix/explain. Theory should not stay
abstract once a topic is introduced.

## Required read-before-work rule

Before work begins:
- `cka-qa` should read current `practicalFeedback`
- `cka-lab` should read current `theoryStatus` and `practicalFocus`

This prevents drift.

## Ownership summary

### cka-qa writes
- `theoryStatus`
- `practicalFocus`
- `lastUpdated`

### cka-lab writes
- `practicalFeedback`
- `lastUpdated`

## Submodule workflow

Because `cka-shared` is a submodule in both parent repos:

1. edit inside `cka-shared`
2. commit and push inside `cka-shared`
3. return to parent repo
4. commit updated submodule pointer
5. push parent repo

## Failure mode to avoid

If you update `cka-shared` but do not commit the parent repo pointer, the parent repo still points to the old shared revision.

## Practical meaning

- theory changes should produce new practical drills
- practical findings should produce smarter quizzes and repeats
- neither repo should act as if it is standalone
- practical drills should use normal CKA-safe commands and avoid vendor-specific
  shortcuts unless the learner explicitly chooses a personal lab detour
