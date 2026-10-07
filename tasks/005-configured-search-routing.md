# Task 005 — Configured search routing

- **Task ID:** 005
- **Title:** Configured search routing
- **Status:** PENDING
- **Suggested branch:** `task/005-configured-search-routing`
- **Dependencies:** [001](001-runtime-configuration.md) and [004](004-search-capability-adapter.md) DONE and integrated: RuntimeConfig/load_config/ConfigurationError; SearchPort, injectable facade and TavilySearchAdapter with preserved tests in updated develop.
- **Requirement IDs:** [specs/provider-neutral-research-foundation/requirements.md](../specs/provider-neutral-research-foundation/requirements.md): PNRF-REQ-003, PNRF-REQ-006, PNRF-REQ-007, PNRF-REQ-008, PNRF-REQ-009, PNRF-REQ-013.

The Planner owns this contract, order and dependencies. When assigned on a
branch based on updated `develop`, the Executor verifies Tasks 001 and 004 are
DONE, integrated and their outputs are present; if so, it may promote
`PENDING → READY → IN_PROGRESS` by changing operational status only. Otherwise
report BLOCKED. Recommended checkpoint A precedes this migration.

## Goal

Route default retrieval through validated local configuration, with Tavily as
the only supported real implementation and existing safe tool behavior intact.

## Context to read

- [AGENTS.md](../AGENTS.md), [progress/current.md](../progress/current.md).
- Referenced requirements; [design §3, §6–9](../specs/provider-neutral-research-foundation/design.md#6-search-capability-and-tavily-adapter).
- Integrated `app/config.py`, retrieval service/ports/Tavily adapter; packets 001/004 interfaces.
- Retrieval tests/search adapter tests, research tools and budget/error tests.
- Historical spec 003 §§4,7–8 and 004 §§6,8,13.

## Implementation constraints

- Change only no-injection composition path: load_config per operation, select
  search_provider, support exactly tavily. No registry or global config/adapter.
- §6 precedence fixed: validate input, reject conflicting injections, explicit
  searcher, explicit client, then configuration. Injections never load profile.
- Config parse/unsupported selection becomes fixed ProviderError message
  `Source retrieval configuration is invalid.`, category provider, from None.
  Unsupported provider fails before SDK construction/call; no fallback.
- Searcher project errors pass through; SDK/client construction remains in
  adapter, default normalizations/messages unchanged. No new tool statuses.
- Default tests clear/control FILM_RESEARCH_CONFIG. Extend focused retrieval
  tests, not production tools or budgets. No new config parameter on facade.

## Expected boundaries/files

- Create: None.
- Modify: `app/source_retrieval/service.py`, `tests/test_source_retrieval.py`
  (configured default and controlled env); own record/progress.
- Preserve: adapter/port/data/error contracts, config contract, agents/tools,
  their tests, specs and dependencies.

## Acceptance criteria

- [ ] PNRF-REQ-003/007: fake loader-selected tavily yields original SDK request/results, with no-injection defaults unchanged; settings are read per default operation, not import-time/global cached.
- [ ] PNRF-REQ-006: explicit searcher/client with broken profile env still works and does not call loader; both injections remain invalid before any work.
- [ ] PNRF-REQ-008: unknown selected search provider, malformed/missing/blank profile config raises safe ProviderError category provider before SDK construction; no sentinel from config is exposed.
- [ ] PNRF-REQ-008: invalid query/options fail before loader and provider even when profile is broken; empty/success/key/request/constructor/malformed outcomes remain distinct.
- [ ] PNRF-REQ-009: full existing tool/budget/reset/race suite passes through the preserved public boundary; no new tool-facing config status.
- [ ] PNRF-REQ-013: targeted/canonical verification passes and diff stays within boundaries.

## Verification commands

Activate dev environment; run baseline before edits.

```sh
python -m pytest -q tests/test_source_retrieval.py tests/test_search_adapters.py tests/test_research_agent.py tests/test_config.py
python scripts/verify.py
git diff --check
git diff
git status --short --branch
```

Expected exits 0. Patch loader/SDK constructor deterministically; prove call
ordering with counters/failing fakes, not live keys. Write targeted failing
tests, add minimal default selection/translation, rerun gate; inspect diff/new
files and record dependencies/branch/results. No integration operations.

## Out of scope

- Adapter parsing changes, runtime factories, agent prompts/tools/state changes.
- Remote/dynamic config guarantees, additional providers, registry or retry/fallback.
- Other Task Packets and future features.

## Executor prompt

> Implement `tasks/005-configured-search-routing.md` following `AGENTS.md`. Do not expand scope.

## Execution record

- Assigned branch / baseline HEAD: Not started.
- Dependency evidence / baseline command and result: Not run.
- Final commands, exit codes and results: Not run.
- Acceptance/diff review: Not performed.
- Decisions within scope / limitations: None recorded.
- Blocker and required resolution / next safe step: None recorded.
