# Task 006 — Architecture and offline compatibility gates

- **Task ID:** 006
- **Title:** Architecture and offline compatibility gates
- **Status:** PENDING
- **Suggested branch:** `task/006-architecture-compatibility-gates`
- **Dependencies:** [003](003-agent-composition.md) and [005](005-configured-search-routing.md) DONE and integrated, including 001/002/004: both build_agent factories/root compatibility, settings/model boundary and configured normalized search facade/adapters, all prior tests available in updated develop.
- **Requirement IDs:** [specs/provider-neutral-research-foundation/requirements.md](../specs/provider-neutral-research-foundation/requirements.md): PNRF-REQ-001, PNRF-REQ-002, PNRF-REQ-004, PNRF-REQ-006, PNRF-REQ-009, PNRF-REQ-010, PNRF-REQ-011, PNRF-REQ-012, PNRF-REQ-013, PNRF-REQ-014.

The Planner owns this contract, order and dependencies. When assigned on a
branch based on updated `develop`, the Executor verifies Tasks 003 and 005 (and
their integrated prerequisites) are DONE and their outputs are present; if so,
it may promote `PENDING → READY → IN_PROGRESS` by changing operational status
only. Otherwise report BLOCKED. Final mechanical acceptance is followed by
recommended High B.

## Goal

Make the new dependency boundaries executable guardrails and demonstrate
offline composed compatibility, with exact operating/extension documentation.

## Context to read

- [AGENTS.md](../AGENTS.md), [progress/current.md](../progress/current.md).
- Referenced requirements; [design §2–10](../specs/provider-neutral-research-foundation/design.md#8-testing-and-architecture-enforcement), especially §8 rules/test seams.
- [DAG/checkpoints](../specs/provider-neutral-research-foundation/tasks.md#selective-high-checkpoints).
- All new settings/runtime/search interface files, both agent factories/tools
  and their relevant existing tests (only boundaries, not all historical context).
- README setup/workflow; .env.example; test_app.py and source retrieval dataclasses.

## Implementation constraints

- AST guard rules and allowed files are fixed in §8: provider SDK imports only
  in designated adapters; core contracts/config stay provider-independent;
  model adapter no agent/retrieval; agents no concrete adapter/key/model route.
- Test helper stays in tests/test_architecture.py. Walk aliases/local imports,
  exact default route/ID and credential-name string literals; allow Tavily
  mentions in grounding content. Test helper with violating/allowed samples.
- Offline flow uses fake BaseLlm plus normalized SearchPort fake. Real public
  facade plus real research tool is exercised; save original facade before
  monkeypatch delegation to avoid recursion. No ADK runner/inference required.
- Block socket connections and live LiteLLM completion entry points during
  composed checks, recording attempts and asserting zero even when a library
  suppresses an exception. Prove fresh default imports offline with no keys/profile
  in a subprocess using sys.executable, rather than only cached imports.
- Use pytest/stdlib only. Existing tests remain; no global mutation framework,
  coverage gate, security sandbox or speculative eval engine.
- README documents §3 example/precedence, keys/defaults, snapshots/restarts,
  explicit settings/model/searcher seams, errors, extension steps and limits.
  Free-first does not promise current pricing or select a paid alternative.

## Expected boundaries/files

- Create: `tests/test_architecture.py`, `tests/test_provider_neutral_flow.py`.
- Modify: `README.md` configuration/architecture/operation guidance;
  own packet/progress records.
- Preserve: all production modules, existing tests/dependencies/specs.
  A real violation requires BLOCKED evidence and Planner decision, not scope expansion.

## Acceptance criteria

- [ ] PNRF-REQ-011/004/006: AST checks pass for actual app and reject aliased/local forbidden imports, route/key literal violations; allowed framework/core/prompt examples pass.
- [ ] PNRF-REQ-001/002/012: independent fake model injection builds both role agents offline; controlled fresh root imports need no keys/network and retain original identities/defaults/exports.
- [ ] PNRF-REQ-006/009/010: composed real tool/facade with normalized fake preserves query, exact candidate URLs/content/metadata, trace/warnings and JSON payload; successful/empty/error calls consume slots and third call never reaches fake search.
- [ ] PNRF-REQ-011: tests fail if any guarded path attempts a live socket/completion; no credential/network/provider quota is needed by the full gate.
- [ ] PNRF-REQ-014/012: README gives exact runnable TOML selection example and Python factory/search injection usage, error semantics, default Groq/Tavily support, unsupported-provider failures, later adapter seams and free-first/manual-eval limits.
- [ ] PNRF-REQ-013: all prior acceptance behavior remains green, new tests and Ruff pass, no product/spec/dependency edits in this packet; record feature checkpoint B recommendation.

## Verification commands

Activate environment; canonical baseline before edits.

```sh
python -m pytest -q tests/test_architecture.py tests/test_provider_neutral_flow.py
python scripts/verify.py
git diff --check
git diff
git status --short --branch
```

Expected exits 0, guard sample/actual-source checks and offline subprocess/flow
pass, all prior tests green. Manually check README local links and examples
against settled interfaces (pytest/Ruff do not validate prose). Read new files.
Write/run failing guard/flow tests, implement test-only checks and documentation,
rerun final gate and inspect full scope. Record commands/results, clear active
work; DONE remains local, not feature integration or provider-quality approval.

## Out of scope

- Product-code fixes/redesign, model-quality claims, live smoke tests/evaluations.
- CI platform setup, new lint/security framework, billing or future provider pipelines.
- Other Task Packets and future features.

## Executor prompt

> Implement `tasks/006-architecture-compatibility-gates.md` following `AGENTS.md`. Do not expand scope.

## Execution record

- Assigned branch / baseline HEAD: Not started.
- Dependency evidence / baseline command and result: Not run.
- Final commands, exit codes and results: Not run.
- Acceptance/diff review: Not performed.
- Decisions within scope / limitations: None recorded.
- Blocker and required resolution / next safe step: None recorded.
