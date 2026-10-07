# Task <NNN> — <Title>

- **Task ID:** <NNN>
- **Title:** <Title>
- **Status:** PENDING
- **Suggested branch:** `task/<NNN>-<slug>`
- **Dependencies:** None / <packet path and ID, exact required outputs>
- **Requirement IDs:** <spec path>: <REQ IDs> / None — <small-change reason>

Replace every placeholder before READY. A packet may begin as PENDING when its
contract is complete but dependencies are not integrated. Once assigned, its
Executor may promote it mechanically to READY and then IN_PROGRESS only after
verifying every dependency is DONE, integrated in the `develop` branch used as
the base, and its required outputs are present in the checkout. See
[packet usage and states](../docs/development/workflow.md#specs-and-task-packets).
The Planner owns the contract, order and dependencies. The Executor may update
operational status, acceptance checkboxes and execution record only; promotion
does not authorize changes to requirements, design, dependencies, scope or
acceptance criteria. If a prerequisite is absent, report BLOCKED. This template
is not an executable backlog item.

## Goal

<One cohesive, observable outcome.>

## Context to read

- [AGENTS.md](../AGENTS.md).
- <Referenced requirements path and IDs; relevant design path/sections.>
- <Relevant steering sections and implementation/test paths.>

## Implementation constraints

- <Settled interfaces/behavior, exact values and dependency constraints.>
- <Specific compatibility/security requirements or None.>

## Expected boundaries/files

- Create: <paths or None>.
- Modify: <paths and purpose or None>.
- Preserve: <contracts/files that must remain unchanged>.

## Acceptance criteria

- [ ] <REQ ID when applicable>: <observable behavior/result and how to check it>.
- [ ] Every required verification command passes and the diff stays in scope.

## Verification commands

Run from the repository root with the development environment prepared:

```sh
python scripts/verify.py
git diff --check
git diff
git status --short --branch
```

Expected: verification/whitespace checks exit 0; diff/status match the assigned
branch and file boundaries. Read new/untracked files too. Add concrete targeted
commands and expected results here when acceptance needs more than this gate.
If GNU Make is available, `make verify` is an equivalent convenience wrapper.

## Out of scope

- <Adjacent behavior/architecture explicitly deferred.>
- Other Task Packets and future features.

## Executor prompt

> Implement `tasks/<NNN>-<slug>.md` following `AGENTS.md`.

## Execution record

- Assigned branch / baseline HEAD: Not started.
- Dependency evidence / baseline command and result: Not run.
- Final commands, exit codes and results: Not run.
- Acceptance/diff review: Not performed.
- Decisions within scope / limitations: None recorded.
- Blocker and required resolution / next safe step: None recorded.
