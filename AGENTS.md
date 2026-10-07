# Coding agent entry point

Think expensive once. Execute cheap many times. This harness governs development,
not the application's film-research agents.

## Start an execution task

1. Read this file and the assigned `tasks/<NNN>-<slug>.md` before other context.
2. Read only its referenced requirements, relevant design/steering sections and
   necessary implementation/tests. Read `progress/current.md` to detect active
   work/blockers; consult history only when needed.
3. Check task status/dependencies, required outputs in this checkout, Python/dev
   tools and `git status --short --branch`. Preserve existing user changes.
4. If the assigned packet is `PENDING`, verify mechanically that every listed
   dependency is `DONE`, its required outputs are present in this checkout, and
   the branch was created from the updated integrated `develop`. If all checks
   pass and the packet contract is complete, update only its status to `READY`
   and then `IN_PROGRESS`; otherwise record/report `BLOCKED` before editing.
5. Run `python scripts/verify.py` as the pre-edit baseline. If prerequisites or
   the baseline prevent execution within scope, record/report BLOCKED before
   changing code.

## Git safety

- Implementation starts conceptually from `develop`. One Task Packet maps to one
  independent local `task/<NNN>-<slug>` branch, prepared by the user or under
  explicit instruction. Stay on the assigned current branch throughout execution.
- Do not create/switch branches or worktrees unless explicitly instructed.
- Never push automatically, merge automatically or open a PR automatically.
- Do not commit unless the user explicitly requests it. Never modify remotes.
- Avoid destructive Git operations (`reset --hard`, `clean`, forced checkout,
  branch deletion, force push). Do not discard, stash or overwrite user work.
- Explicit user task instructions take priority over generic skill workflows
  proposing other branches, commits, publishing or extra approval ceremonies.

## Execute and finish

- Follow the packet's settled design and scope. Do not redesign architecture,
  choose new providers, add unplanned dependencies or implement future tasks.
- Do not edit specs in `specs/` during execution. Update only
  your packet's status/acceptance/execution record, not its implementation contract.
- If the spec/packet is insufficient, impossible or contradictory, stop and
  report BLOCKED with evidence and the minimum Planner decision needed.
- Use existing patterns/tools and the smallest cohesive change. Add meaningful
  deterministic tests for changed logic; do not add tools without a task need.
- Run `python scripts/verify.py` and every additional packet check, inspect `git diff --check`,
  `git diff` and `git status`, and check scope before declaring completion.
- DONE requires all acceptance criteria and verification to pass. Failed or
  unavailable verification cannot be waived; DONE does not imply Git integration.
- Update your packet and progress at start, interruption/blockage and completion.
  Report commands/results, changed files and remaining limitations.

## Context map

- [Workflow](docs/development/workflow.md): roles, specs, statuses,
  dependencies, blockers, context, memory and verification (read relevant sections).
- [Packet template](tasks/TEMPLATE.md); [setup and commands](README.md#development-setup).
- Product, architecture and historical research contracts: `specs/`.
