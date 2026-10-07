# Development Harness — Requirements

## Objective

Think expensive once. Execute cheap many times. A capable development Planner
records decisions so a faster Executor can implement one bounded task without
reconstructing the project from conversation. These are development roles,
separate from the application's Research Planner and Research Agent.

Requirement IDs are local to this spec. Task Packets must cite both this spec's
path and the IDs they satisfy.

## Requirements and acceptance

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| REQ-001 | Preserve the existing prototype, dependencies, historical specs and user work. Task 000 runs only on the current local branch, without commit, push, merge, PR or destructive Git operations. | Final diff leaves `app/`, `tests/`, `pyproject.toml` and `specs/` unchanged; branch and HEAD match the baseline. |
| REQ-002 | Provide a short root `AGENTS.md` with universal execution rules and links to detailed guidance. | At most 60 lines; an Executor can start with only a packet path and `AGENTS.md`. |
| REQ-003 | Record significant planned changes as identifiable requirements, design and tasks, with traceability into Task Packets. Small changes may use a packet alone. | This feature has `requirements.md`, `design.md` and `tasks.md`; Task 000 references the applicable IDs. Existing specs remain in place. |
| REQ-004 | Define a reusable Task Packet contract, status lifecycle and dependency policy. One packet is one cohesive, verifiable unit on one local task branch. | Template includes ID, title, status, suggested branch, dependencies, goal, requirement IDs, context, constraints, acceptance, verification, boundaries, exclusions and Executor prompt. All five statuses have explicit meanings. |
| REQ-005 | Separate development planning from execution; keep execution context narrow and surface genuine design blockers rather than improvising architecture. | Steering defines each role, reading order, architecture-change conditions, dependency checks and a concrete BLOCKED report/resumption process. |
| REQ-006 | Keep minimal external development memory in versioned files. | `progress/current.md` identifies the active task or explicitly says none; `progress/history.md` records completions/relevant events. Update timing and evidence location are defined. |
| REQ-007 | Provide a portable canonical runner, `python scripts/verify.py`, that runs existing deterministic tests and Ruff through the same Python interpreter; keep `make verify` as a convenience wrapper. | Successful runner and wrapper exit 0; a failure in either check produces a nonzero exit and stops the sequence. GNU Make is not required by the verification contract. |
| REQ-008 | Document setup and the full workflow with deterministic checks first and selective model review at checkpoints. | README links the harness and describes Python/dev extras plus optional GNU Make convenience. No new project dependencies, automatic checkpoints, task scheduler or memory service are added. |

## Scope

Task 000 creates the harness documentation, its own spec and packet, progress
files and a portable verification entry point. README changes are limited to setup and the
development workflow. Additional harness tests are warranted only if
the implementation introduces logic that needs them.

Provider abstraction, new providers, new research agents, research behavior
changes, RAG, embeddings/vector storage, APIs, containers and automated agent
orchestration belong to later planning sessions. This task creates no backlog
for those features.
