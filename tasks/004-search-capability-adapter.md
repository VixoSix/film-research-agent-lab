# Task 004 — Normalized search capability and Tavily adapter

- **Task ID:** 004
- **Title:** Normalized search capability and Tavily adapter
- **Status:** READY
- **Suggested branch:** `task/004-search-capability-adapter`
- **Dependencies:** None. Existing retrieval dataclasses/errors/facade are the foundation; Task 000 harness already exists.
- **Requirement IDs:** [specs/provider-neutral-research-foundation/requirements.md](../specs/provider-neutral-research-foundation/requirements.md): PNRF-REQ-006, PNRF-REQ-007, PNRF-REQ-008, PNRF-REQ-010, PNRF-REQ-013.

The Planner owns this contract; Executor updates only status, acceptance and
execution record. Independent READY packet; 001 remains recommended first.

## Goal

Separate normalized search from raw Tavily behavior, preserving existing
retrieval semantics and client injection while adding a normalized fake seam.

## Context to read

- [AGENTS.md](../AGENTS.md), [progress/current.md](../progress/current.md).
- Referenced requirements; [design §1–2, §6–8](../specs/provider-neutral-research-foundation/design.md#6-search-capability-and-tavily-adapter).
- `app/source_retrieval/{__init__,service,models,errors}.py`, `tests/test_source_retrieval.py`.
- `app/research_agent/tools.py`, its retrieval delegation/payload/error tests.
- Historical spec 003 §§4–8,12; pinned Tavily constructor/search only if needed.

## Implementation constraints

- Introduce/export §6 SearchPort Protocol; existing normalized dataclasses and
  errors are its outputs, no raw envelope or second request/result schema.
- TavilySearchAdapter(*, client=None).search has port signature. Constructor
  performs no network/key work; real client constructed lazily on search.
- Move SDK import/key/depth mapping/raw normalizers/timeout helper to adapter.
  Service retains public validation, facade and composition, not raw parsing.
- Extend facade with keyword-only searcher=None; validate first, reject both
  client/searcher, prefer explicit normalized searcher then legacy client.
- For this packet ONLY, no-injection path constructs Tavily adapter directly;
  configuration routing is 005. This transitional choice must stay green.
- Wrap client construction and search errors; missing key and malformed envelope
  remain distinct outside SDK-error translator. Keep current messages/category
  and cause chaining. No keyless mode/retry/fallback or provider behavior changes.
- Update tests' TavilyClient patch target to adapter; do not weaken assertions.
  Keep research tool calls and monkeypatch seam app.source_retrieval.search_web.

## Expected boundaries/files

- Create: `app/source_retrieval/ports.py`,
  `app/source_retrieval/adapters/{__init__,tavily}.py`, `tests/test_search_adapters.py`.
- Modify: retrieval service/__init__, `tests/test_source_retrieval.py` for moved
  patch targets and new seam cases; own execution record/progress.
- Preserve: models.py/errors.py identities and exports, both agents/tools,
  their tests, all specs and dependencies. No settings import in this packet.

## Acceptance criteria

- [ ] PNRF-REQ-006: fake normalized searcher receives trimmed query and public options and returns RetrievalResult by identity; no key/SDK needed; legacy client path remains compatible.
- [ ] PNRF-REQ-006/008: both non-None injections raise InvalidRetrievalInputError before either call; invalid query/options precede all provider construction/calls.
- [ ] PNRF-REQ-007: all existing option/default/range/normalization/exact URL/order/deduplication/optional-field/trace/warning assertions retain their meaning and pass through extracted adapter.
- [ ] PNRF-REQ-008: missing/blank key prevents construction; fake SDK constructor timeout and generic failure now become same safe ProviderError categories as request failures; malformed envelopes remain their own errors.
- [ ] PNRF-REQ-008: injected searcher's project errors pass through unchanged; successful empty remains distinct from failure and malformed data.
- [ ] PNRF-REQ-010: metadata/content remain unmodified discovery material; unchanged tool serialization/grounding tests pass; no reliability or inspection state added.
- [ ] PNRF-REQ-013: service has no Tavily SDK import/key/raw result parsing; canonical/focused checks and scope review pass.

## Verification commands

Activate existing dev environment; canonical baseline before edits.

```sh
python -m pytest -q tests/test_source_retrieval.py tests/test_search_adapters.py tests/test_research_agent.py
python scripts/verify.py
git diff --check
git diff
git status --short --branch
```

Expected exits 0, original retrieval values and tool tests unchanged in meaning,
Ruff green. New contract tests use fake normalized searcher; adapter tests use
fake SDK client/constructor, never real API. Write/run failing extraction/seam
and constructor-error tests, move minimal existing logic, rerun checks. Inspect
new files plus diff, record branch/baseline/acceptance and clear active work.

## Out of scope

- Configured provider selection (005), model runtime/agents/budget refactors.
- New search providers, ranking/scoring, URL canonicalization, response caps,
  document fetching/inspection, output sanitization redesign or credentials policy change.
- Other Task Packets and future features.

## Executor prompt

> Implement `tasks/004-search-capability-adapter.md` following `AGENTS.md`. Do not expand scope.

## Execution record

- Assigned branch / baseline HEAD: Not started.
- Dependency evidence / baseline command and result: Not run.
- Final commands, exit codes and results: Not run.
- Acceptance/diff review: Not performed.
- Decisions within scope / limitations: None recorded.
- Blocker and required resolution / next safe step: None recorded.
