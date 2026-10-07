# Development Harness — Design

## Basis: reconnaissance before edits

On 2026-10-07 the clean branch `task/000-development-harness` was at `d57bc78`,
also the local `develop` tip. The tracked repository was read in full, including
README, packaging/configuration, application modules, tests and four specs.

- Python >=3.11, setuptools; existing `.venv` uses Python 3.14.3.
- Runtime dependencies: Google ADK 2.10.0, LiteLLM 1.101.2, Tavily SDK 0.8.4.
  Existing dev extras are pytest and Ruff; no lockfile or CI verification exists.
- `app/research_planner/agent.py` configures an ADK agent without tools.
- `app/research_agent/` configures a separate ADK agent with a serialized search
  tool and a two-call invocation budget. Both agents use LiteLLM with Groq.
- `app/source_retrieval/` validates queries, calls Tavily, normalizes dataclasses
  and exposes typed errors; tests fake provider interactions.
- `specs/001` describes the wider research goal; `specs/002`–`004` describe the
  planner, retrieval and preliminary research boundaries. Wider goals are not
  proof of implemented features. `knowledge/` and `evals/` contain placeholders.
- No existing `AGENTS.md`, Makefile or development-harness convention.
  README's `feature/*`/PR workflow needs alignment with local Task Packets.

Baseline: `.venv/Scripts/python.exe -m pytest -q` exited 0: **62 passed,
2 warnings** (Google GenAI deprecation and a pytest cache write warning).
`.venv/Scripts/python.exe -m ruff check .` exited 0: **All checks passed!**
`python -m pip check` in the same environment reported no broken requirements.
GNU Make was absent from PATH; this checkpoint makes it optional rather than a
verification prerequisite. No credentials or live provider calls are part of verification.

## Decision and layout

Use plain Markdown plus a small Makefile. Keeping everything in `AGENTS.md`
would overload every Executor's context; adding a task runner/database would
create maintenance before a demonstrated need. One steering file carries the
operational details; no plugin is required to use the harness.

| Artifact | Responsibility |
| --- | --- |
| `AGENTS.md` | Short entry point, universal rules and context map. |
| `docs/development/workflow.md` | Roles, Git safety, spec workflow, statuses/dependencies, context, memory and verification policy. |
| `specs/development-harness/{requirements,design,tasks}.md` | Contract, rationale and implementation plan for this harness. |
| `tasks/TEMPLATE.md` | Reusable contract; placeholders do not constitute backlog items. |
| `tasks/000-development-harness.md` | Actual Task 000, including acceptance and execution evidence. |
| `progress/current.md` / `history.md` | Active-task pointer/resumption state and concise durable events. |
| `scripts/verify.py` | Portable deterministic verification entry point. |
| `Makefile` | Convenience wrapper delegating to `scripts/verify.py`. |
| `README.md` | Setup and short workflow introduction with links. |

Historical `specs/` files stay where they are; new substantial features use
`specs/<feature>/`. No migration or duplicate rewrite is needed.

## Operational contract

The development Planner records requirements/design and prepares packets with
decisions, relevant context, dependencies and measurable acceptance. The user
prepares one local `task/<NNN>-<slug>` branch from `develop`; an Executor checks
the assigned packet and current branch, then runs baseline, implements and
verifies. A dependency's DONE status alone does not mean its changes are
integrated into `develop`; required outputs must exist in the current checkout.

Specs are planning artifacts. Executors may update only their own packet's
status, acceptance checkboxes and execution record, plus progress memory; they
do not edit specs or another task's contract. A genuine missing/contradictory
design or unavailable prerequisite is reported BLOCKED, with evidence and the
minimum decision needed. A Planner resolves design issues in a separate
planning pass; execution resumes only once the contract is executable.

DONE means acceptance and every required check passed on the task branch.
It does not mean committed, merged, pushed or reviewed by a model. Deterministic
checks are the first gate; the user schedules capable-model reviews at cohesive
checkpoints or architectural decisions. No automatic review system is built.

## Verification design

`python scripts/verify.py` runs `sys.executable -m pytest -q`, then
`sys.executable -m ruff check .` sequentially from the repository root. It
stops and returns the first nonzero exit code. The runner has no installation,
auto-fix, provider or shell dependency. `make verify` delegates to this runner;
`PYTHON` can select the interpreter used to start the runner, but GNU Make is
not part of the canonical Executor prerequisite.

Validate the successful path against the real suite and exercise both failure
paths with a temporary substitute interpreter, without touching application
code. Markdown contracts also require a final manual traceability/link/scope
review; pytest/Ruff do not establish prose consistency or LLM research quality.

## Task 000 process decisions

The user's explicit scope takes priority over generic workflow suggestions:
author this spec and implement inline without approval pauses, a new
branch/worktree or commits. This spec's `tasks.md` is the plan, and `progress/`
is the memory. Future Executors can use this repository with the versioned
harness documents and project dependencies alone.
