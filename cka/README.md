# CKA Learning Workspace

This directory consolidates the former CKA repositories into one learning area without changing the existing Docker/debug labs in the repository root.

## What lives here

```text
cka/
├── README.md
├── STUDY-WORKFLOW.md
├── SOURCE-MIGRATION.md
└── source-snapshots/
    ├── cka-qa/          # theory, recall, quizzes and focus tracking
    ├── cka-lab/         # practical build/break/fix exercises
    ├── cka-lab-notes/   # troubleshooting notes and kubectl cheatsheets
    ├── cka-shared/      # machine-readable study handoff state
    └── course-notes/    # full KodeKloud CKA course notes
```

The `source-snapshots` entries are pinned Git submodules. They preserve the exact source repositories at the commits used during consolidation, including the large course-notes repository, without copying tens of megabytes into this repository.

## Clone with all CKA material

```bash
git clone --recurse-submodules https://github.com/ffworker/learning-lab.git
```

For an existing clone:

```bash
git submodule update --init --recursive
```

## Recommended entry points

- Theory and current focus: `source-snapshots/cka-qa/`
- Practical exercises: `source-snapshots/cka-lab/exercises/`
- Troubleshooting and cheat sheets: `source-snapshots/cka-lab-notes/`
- Shared learning state: `source-snapshots/cka-shared/handoff.json`
- Full course notes: `source-snapshots/course-notes/docs/`

## Consolidated learning method

Use the same loop for each introduced topic:

1. Define the component precisely.
2. Build the smallest working example.
3. Inspect the objects and their relationships.
4. Break exactly one link deliberately.
5. Diagnose using normal CKA-safe commands.
6. Fix the root cause.
7. Explain the component boundary without notes.

See [STUDY-WORKFLOW.md](STUDY-WORKFLOW.md).

## Repository status

The former standalone CKA repositories are preserved as source snapshots and can be archived. `learning-lab` is now the single active home for CKA learning material.
