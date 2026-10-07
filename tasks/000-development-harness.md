# Task 000 — Development Harness

- **Task ID:** 000
- **Title:** Development Harness
- **Status:** DONE
- **Suggested branch:** `task/000-development-harness`
- **Dependencies:** None; existing prototype/tests/dev tools are the baseline.
- **Requirement IDs:** [specs/development-harness/requirements.md](../specs/development-harness/requirements.md): REQ-001–REQ-008.

## Goal

Provide a minimal, versioned development contract so future implementation can
start with a packet path and AGENTS.md, without repeated project explanations.

## Context to read

- [AGENTS.md](../AGENTS.md).
- Harness [requirements](../specs/development-harness/requirements.md),
  [design](../specs/development-harness/design.md) and
  [implementation plan](../specs/development-harness/tasks.md).
- [Development workflow](../docs/development/workflow.md).
- [README](../README.md), [pyproject.toml](../pyproject.toml).
- Task 000 reconnaissance reads all tracked application/test/spec files; this
  broader Planner scope is not required of future Executors.

## Implementation constraints

- Use the user's current branch only; no new branch/worktree, switching, commit,
  push, merge, PR, remote change or destructive Git operation.
- Markdown and existing pytest/Ruff tooling only; no new Python dependencies.
- Keep historical specs and functional code/tests unchanged.
- This combined planning/implementation Task 000 explicitly authors its own
  harness spec. It is an exception to the normal Executor rule against spec edits.
- No requirement to commit or integrate before DONE; retain reviewable local files.

## Expected boundaries/files

- Create: `AGENTS.md`, `Makefile`, `scripts/verify.py`, `docs/development/workflow.md`,
  `specs/development-harness/{requirements,design,tasks}.md`,
  `tasks/{TEMPLATE,000-development-harness}.md`, `progress/{current,history}.md`.
- Modify: `README.md` setup/development workflow only.
- Preserve: `app/`, `tests/`, `specs/`, `pyproject.toml`, all other tracked files
  and any pre-existing user work.

## Acceptance criteria

- [x] REQ-001: Final Git inspection confirms original branch/HEAD and preserved paths.
- [x] REQ-002: AGENTS is <=60 lines and maps to relevant execution guidance.
- [x] REQ-003: Harness requirements/design/tasks are traceable; historical specs remain intact.
- [x] REQ-004: Template contains every required field; lifecycle and dependency semantics are explicit.
- [x] REQ-005: Planner/Executor, context, architecture limits and actionable BLOCKED handling are documented.
- [x] REQ-006: Current/history files and their update timing are coherent with packet status.
- [x] REQ-007: Real `python scripts/verify.py` and `make verify` pass; temporary failures in either check return nonzero and pytest failure stops Ruff.
- [x] REQ-008: README explains setup/workflow; deterministic checks precede selective review; no extra services/tools/backlog.

## Verification commands

From the root with the prepared environment:

```sh
python scripts/verify.py
git diff --check
git diff -- app tests specs pyproject.toml
git diff
git status --short --branch
git branch --show-current
git rev-parse --short HEAD
```

Expected: verification exits 0, existing tests pass and Ruff reports
`All checks passed!`; no whitespace errors or protected-path diff;
branch `task/000-development-harness`, HEAD `d57bc78`. Read all new files and
check Markdown links, requirement coverage and documentation consistency. If
GNU Make is available, `make verify` must produce the same result through the
portable runner; the portable command remains sufficient when Make is absent.
Exercise pytest and Ruff failure separately via temporary substitute commands:
each must return nonzero; the pytest failure must stop Ruff.
The temporary probe is not application code or an additional project dependency.

## Out of scope

Research functionality/refactors, provider ports/registry/new providers, YouTube,
RAG/embeddings/vector storage, new research agents, APIs, Docker, large dependency
changes, automated task/checkpoint systems and future architectural Task Packets.

## Executor prompt

> Implement `tasks/000-development-harness.md` following `AGENTS.md`. For this
> Task 000 only, perform the documented reconnaissance and author the harness
> spec before implementation; preserve the current branch and prototype.

## Execution record

- Assigned branch / baseline HEAD: `task/000-development-harness` / `d57bc78`;
  clean starting tree; dependencies: none.
- Baseline: `.venv/Scripts/python.exe -m pytest -q` → exit 0, 62 passed,
  2 warnings (Google GenAI deprecation; pytest cache write warning).
  `.venv/Scripts/python.exe -m ruff check .` → exit 0, All checks passed!
  Same environment's `python -m pip check` → exit 0, no broken requirements.
- `make verify` → exit 0, 62 passed, 2 baseline warnings; Ruff: All checks passed!
  Both temporary failure probes → Make exit 2; pytest failure stops Ruff.
- `git diff --check` → exit 0; protected-path diff empty; branch/HEAD unchanged.
  `git diff` / `git status --short --branch` inspected, including all new files.
- Acceptance/diff review: original seven requirements remain satisfied; AGENTS 52 lines;
  all 10 Markdown documents and their local links/anchors checked, no trailing whitespace.
  Independent read-only review found no P1/P2 issue; its missing plan-to-packet
  link was added and checked. No production code, tests, dependency or old spec changes.
- Decisions: one steering file; retain historical specs; this checkpoint makes
  `scripts/verify.py` canonical and keeps Make as convenience.
- Environment: GNU Make was absent from normal PATH; a verified portable copy
  was used temporarily only to check the wrapper. Executors need Python plus
  project dev tools, not GNU Make.
- Limitations: both baseline warnings remain; Markdown review and provider/model
  quality are outside pytest/Ruff. No persistent runner test is needed; failure
  probes are temporary.
- Blocker: none. Completed 2026-10-07, verified locally and uncommitted. No active
  execution task; the next architecture planning session is separate.
