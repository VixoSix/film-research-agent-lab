# Development Harness — Implementation Plan

> For this Task 000 implementation, execute the steps directly on the assigned
> current branch. The user's current-branch/no-commit instructions govern the work.

**Goal:** Deliver the development harness without changing research behavior.
**Architecture:** Versioned Markdown contracts and memory, plus one Makefile.
**Tech stack:** Existing Python, pytest and Ruff; optional GNU Make wrapper.
**Spec:** [requirements](requirements.md) and [design](design.md).

## Global constraints

- Only `task/000-development-harness`; no branch creation/switch, commit, push,
  merge, PR or destructive Git operation.
- Leave `app/`, `tests/`, `pyproject.toml` and historical `specs/` unchanged.
- No new Python dependencies, application architecture or future backlog.
- Task 000 includes spec authoring explicitly; later implementation packets do
  not acquire permission to change specs from this exception.

## Review focus

- Wrong Python environment or missing project dev tools: document the portable
  interpreter selection; verification must fail visibly when tooling is absent.
- Failure in either verification command: prove nonzero exit with temporary
  substitute commands, with no application edits.
- Dependency DONE but absent from checkout: execution must remain blocked.
- Skill advice to commit/switch branches: repository/user safety rules prevail.
- Specs, packet, progress and README: links, statuses and boundaries must agree.

## Task 000: One cohesive harness (REQ-001–REQ-008)

**Task Packet:** [000 — Development Harness](../../tasks/000-development-harness.md).

**Files:** The artifact table in [design](design.md#decision-and-layout) lists
every new/modified file; there are no production interfaces to change.
**Consumes:** Existing packaging, modules, tests/specs and the user's scope.
**Produces:** A usable Executor contract, memory convention and portable verification runner.

- [x] Read repository/Git state and run pre-edit tests, Ruff and dependency check.
  Expected: clean task branch, 62 passing tests, Ruff and dependencies healthy.
- [x] Write this feature's requirements/design/plan and inspect for scope gaps.
- [x] Write `AGENTS.md`, one steering document and the packet template; create
  Task 000 as IN_PROGRESS with traceable acceptance and a bounded prompt.
- [x] Initialize progress memory with baseline/active branch; update README's
  workflow/setup without presenting planned research capabilities as complete.
- [x] Add `scripts/verify.py` as the canonical runner and make `make verify` a
  wrapper. Test both failure paths using temporary commands and verify successful
  real runner/wrapper runs. Expected: each simulated failure exits nonzero;
  pytest failure stops Ruff; both real commands exit 0 when Make is available.
- [x] Inspect every new document and `git diff --check`, `git diff` and
  `git status --short --branch`; compare branch/HEAD and protected paths to baseline.
  Expected: consistent links/contracts, <=60-line AGENTS, no scope violations.
- [x] Only after the checks pass, mark the packet DONE, clear current work and
  append completion/evidence to history. Report results and environment limits.

The checked reconnaissance steps are completed evidence, not new Task Packets.
No later architecture tasks are generated here.
