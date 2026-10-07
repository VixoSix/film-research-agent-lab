# Task 002 — Model runtime and safe errors

- **Task ID:** 002
- **Title:** Model runtime and safe errors
- **Status:** PENDING
- **Suggested branch:** `task/002-model-runtime-boundary`
- **Dependencies:** [001](001-runtime-configuration.md) DONE and integrated: `app/config.py` ModelConfig, RuntimeConfig/defaults and ConfigurationError; settings tests green in updated develop.
- **Requirement IDs:** [specs/provider-neutral-research-foundation/requirements.md](../specs/provider-neutral-research-foundation/requirements.md): PNRF-REQ-004, PNRF-REQ-005, PNRF-REQ-012, PNRF-REQ-013.

The Planner owns this contract, order and dependencies. When assigned on a
branch based on updated `develop`, the Executor verifies Task 001 is DONE,
integrated and present; if so, it may promote `PENDING → READY → IN_PROGRESS`
by changing operational status only. Otherwise report BLOCKED.

## Goal

Provide one ADK-compatible model factory with Groq/LiteLLM transport and safe
execution errors while the current agents remain unchanged and functional.

## Context to read

- [AGENTS.md](../AGENTS.md), [progress/current.md](../progress/current.md).
- Referenced requirements; [design §2–4, §8, §10–11](../specs/provider-neutral-research-foundation/design.md#4-model-boundary-and-errors).
- Task 001 interfaces and integrated `app/config.py`, `tests/test_config.py`.
- Current model declarations in both agent modules; existing default-model tests.
- Pinned local ADK `models/base_llm.py`, `models/lite_llm.py` (constructor and
  generate_content_async only); LiteLLM `exceptions.py` relevant classes.

## Implementation constraints

- Export build_model(ModelConfig)->BaseLlm and ModelExecutionError; §4 fixes
  the private `_ProjectLiteLlm(LiteLlm)` subclass and exact async method.
- Groq only; unsupported provider/double groq prefix is ConfigurationError
  before SDK construction. Compose groq/{model_id}; family never routes.
- Pass reasoning option only if supplied. No LanguageModelPort/custom responses.
- At iteration start check env GROQ_API_KEY, then delegate/yield unchanged.
  Import/construction requires no key and makes no completion call.
- §4 table fixes safe messages/categories. Catch Exception in generation,
  preserve project error, suppress provider cause; do not catch BaseException.
- Preserve stream flag, request, tools, function calls, usage and response order.
  Midstream failure is terminal, no retry/replay/final fallback.
- asyncio.run and pytest suffice; no new async test dependency. No product logs.

## Expected boundaries/files

- Create: `app/model_runtime/{__init__,errors,litellm}.py`, `tests/test_model_runtime.py`.
- Modify: own execution record/progress only.
- Preserve: existing agents/retrieval/config contract, old tests and dependencies/specs.

## Acceptance criteria

- [ ] PNRF-REQ-004: default factory builds a LiteLlm-compatible BaseLlm with exact original Groq route/reasoning; construction succeeds without key; unsupported provider/double prefix fails before constructor.
- [ ] PNRF-REQ-012: distinct model IDs produce distinct selected routes; family-only changes do not change SDK args; None reasoning is omitted.
- [ ] PNRF-REQ-005: fake generation receives original request and stream flag and yields original response objects in order for both stream values, including function/usage content.
- [ ] PNRF-REQ-005: missing/blank key prevents delegate iteration; actual LiteLLM Timeout/AuthenticationError/RateLimitError and generic failure produce fixed category/message without sentinel secrets in str/fields or displayed cause.
- [ ] PNRF-REQ-005: one partial response followed by failure raises terminal project error without synthetic output/retry; already-project errors and asyncio cancellation propagate correctly.
- [ ] PNRF-REQ-013: existing agents remain unmigrated and all verification/diff checks pass.

## Verification commands

Activate existing dev environment; run canonical baseline before edits.

```sh
python -m pytest -q tests/test_model_runtime.py tests/test_config.py
python scripts/verify.py
git diff --check
git diff
git status --short --branch
```

Expected all exits 0, safe async cases pass and old tests/Ruff remain green.
Patch superclass generation with async fakes; never invoke live completion.
Inspect new files. Isolate private _additional_args assertions in adapter tests.
Write/run failing tests, implement §4, rerun targeted and canonical checks.
Record branch/dependency outputs/commands and completion locally only.

## Out of scope

- Migrating agents (003), search, providers other than Groq, model catalogs/endpoints.
- Retry/fallback, runner/UI error rendering, inference evaluation, new dependencies.
- Other Task Packets and future features.

## Executor prompt

> Implement `tasks/002-model-runtime-boundary.md` following `AGENTS.md`. Do not expand scope.

## Execution record

- Assigned branch / baseline HEAD: Not started.
- Dependency evidence / baseline command and result: Not run.
- Final commands, exit codes and results: Not run.
- Acceptance/diff review: Not performed.
- Decisions within scope / limitations: None recorded.
- Blocker and required resolution / next safe step: None recorded.
