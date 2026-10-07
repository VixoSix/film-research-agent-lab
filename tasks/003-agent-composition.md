# Task 003 — Configurable agent composition

- **Task ID:** 003
- **Title:** Configurable agent composition
- **Status:** PENDING
- **Suggested branch:** `task/003-agent-composition`
- **Dependencies:** [002](002-model-runtime-boundary.md) DONE and integrated, including its 001 prerequisite: build_model/ModelExecutionError, immutable settings/loader, their tests available in updated develop.
- **Requirement IDs:** [specs/provider-neutral-research-foundation/requirements.md](../specs/provider-neutral-research-foundation/requirements.md): PNRF-REQ-001, PNRF-REQ-002, PNRF-REQ-003, PNRF-REQ-004, PNRF-REQ-009, PNRF-REQ-010, PNRF-REQ-012, PNRF-REQ-013.

The Planner owns this contract, order and dependencies. When assigned on a
branch based on updated `develop`, the Executor verifies Task 002 (and its
integrated prerequisites) is DONE and its outputs are present; if so, it may
promote `PENDING → READY → IN_PROGRESS` by changing operational status only.
Otherwise report BLOCKED. Recommended checkpoint A precedes this migration.

## Goal

Make both existing responsibility agents configurable/injectable without
changing their research instructions, public discovery imports or search tool.

## Context to read

- [AGENTS.md](../AGENTS.md), [progress/current.md](../progress/current.md).
- Referenced requirements; [design §3–5, §8–9](../specs/provider-neutral-research-foundation/design.md#5-agent-composition-and-compatibility).
- Integrated app/config.py and model_runtime exports; Task 002 interfaces.
- `app/research_planner/{agent,__init__}.py`, `app/research_agent/{agent,__init__,tools}.py`.
- `tests/test_research_planner.py`, `tests/test_research_agent.py`.
- Historical specs 002 responsibilities/grounding and 004 §§6,8,11–13,21.

## Implementation constraints

- Each module adds build_agent(config=None, *, model=None)->Agent with §5
  types/precedence. Explicit model bypasses loader; else settings then factory.
- Both root agents use their responsibility constants; no provider/model-ID
  literals or concrete LiteLlm import/credential reads in agent packages.
- Preserve exact instruction strings, descriptions/names, tools/callback and
  both package __init__ contracts. Keep MODEL as root_agent.model alias.
- Build one root_agent per module; factory creates a fresh model/agent by
  default, no global model cache. No new agents or orchestration.
- Existing default configuration assertions retain meanings under controlled
  profile env cleared before module import: defer the planner test's top-level
  agent import into tests under its fixture. For invalid-env injection tests,
  import factory with defaults first, then set invalid env and invoke it.
  Move no budget/serialization logic; do not edit tools.py.

## Expected boundaries/files

- Create: None.
- Modify: two `app/*/agent.py` files; existing two agent test files for factory
  cases and controlled default profile; own record/progress.
- Preserve: instructions byte-for-byte, __init__ exports, tools.py, retrieval,
  settings/runtime contracts, specs and dependencies.

## Acceptance criteria

- [ ] PNRF-REQ-001/004: root imports work with no credentials; default identity/description/model remain original, MODEL aliases each root's model, planner has no tools, researcher retains search_web and reset callback.
- [ ] PNRF-REQ-002/003/012: injecting settings selects the correct independent role binding; swapping one role's model leaves the other unchanged; repeated factory calls are independent.
- [ ] PNRF-REQ-004/012: injected fake BaseLlm is used by identity, does not call loader/factory even with invalid profile env, and requires no Groq key.
- [ ] PNRF-REQ-009/010: unchanged budget/race/schema/payload and grounding/output tests all pass; prompt strings match pre-edit source exactly.
- [ ] PNRF-REQ-013: no concrete runtime/provider imports/hardcodes remain in agents and all required checks pass with scoped diff.

## Verification commands

Activate environment and run baseline. Save/read pre-edit prompt source for
exact comparison; inspect the prompt diff (no line edits permitted).

```sh
python -m pytest -q tests/test_research_planner.py tests/test_research_agent.py tests/test_model_runtime.py
python scripts/verify.py
git diff --check
git diff -- app/research_planner/agent.py app/research_agent/agent.py
git diff
git status --short --branch
```

Expected exits 0; original prompt/behavior assertions plus new composition
assertions pass. Set/clear profile env in tests rather than external setup.
Write failing composition tests, migrate only construction, rerun checks and
record acceptance/branch/dependency evidence. No live invocation or Git integration.

## Out of scope

- Search tool/budget changes, new role/agent, ADK runner or multiagent workflow.
- New model providers, prompt rewriting, output schemas or grounding relaxation.
- Other Task Packets and future features.

## Executor prompt

> Implement `tasks/003-agent-composition.md` following `AGENTS.md`. Do not expand scope.

## Execution record

- Assigned branch / baseline HEAD: Not started.
- Dependency evidence / baseline command and result: Not run.
- Final commands, exit codes and results: Not run.
- Acceptance/diff review: Not performed.
- Decisions within scope / limitations: None recorded.
- Blocker and required resolution / next safe step: None recorded.
