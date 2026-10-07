# Task 001 — Validated runtime configuration

- **Task ID:** 001
- **Title:** Validated runtime configuration
- **Status:** READY
- **Suggested branch:** `task/001-runtime-configuration`
- **Dependencies:** None. Task 000 harness outputs already exist in this checkout.
- **Requirement IDs:** [specs/provider-neutral-research-foundation/requirements.md](../specs/provider-neutral-research-foundation/requirements.md): PNRF-REQ-002, PNRF-REQ-003, PNRF-REQ-013.

The Planner owns this contract; Executor updates only status, acceptance and
execution record. READY is a planning handoff, not permission to switch branches.

## Goal

Provide validated, immutable local settings that select role/provider/model
independently, without yet changing runtime agents or retrieval.

## Context to read

- [AGENTS.md](../AGENTS.md), [progress/current.md](../progress/current.md).
- Referenced requirements and [design sections 1–3, 8–10](../specs/provider-neutral-research-foundation/design.md#3-configuration-contract).
- [Workflow: states/dependencies, execution, memory](../docs/development/workflow.md#status-and-dependencies).
- `README.md` Development Setup; `pyproject.toml`; `app/__init__.py`;
  the model declarations in the two existing agent modules.

## Implementation constraints

- Follow design §3 exactly: frozen ModelConfig/RuntimeConfig,
  ConfigurationError, DEFAULT_CONFIG, model_for and load_config signatures.
- Stdlib only (dataclasses/pathlib/tomllib/os, re for identifier validation);
  no SDK or settings dependency.
- Defaults: provider groq, ID openai/gpt-oss-120b, family gpt-oss,
  include_reasoning False for both roles; search tavily. Declare default once.
- Loader precedence explicit path > env FILM_RESEARCH_CONFIG > defaults;
  explicit invalid/blank paths fail. Present role is a whole replacement with
  required provider/model_id, absent role uses default. Unknown fields fail.
- Validate programmatic dataclasses as well as TOML; providers are syntactic
  identifiers here, actual support is checked by later capability factories.
- No credentials, .env loading, logging of file contents/values or global cache.
- Existing application behavior remains untouched. No committed required profile.

## Expected boundaries/files

- Create: `app/config.py`, `tests/test_config.py`.
- Modify: this packet's execution fields and progress only.
- Preserve: all current agents/retrieval/tests, deps, root exports, historical/new specs.

## Acceptance criteria

- [ ] PNRF-REQ-002: defaults and two distinct injected bindings preserve role/provider/model/family dimensions; model_for rejects unknown role safely.
- [ ] PNRF-REQ-003: tests prove default/env/explicit-path precedence (including relative cwd), missing/unreadable/malformed file failure and no fallback on invalid explicit path.
- [ ] PNRF-REQ-003: absent tables/defaults, complete binding replacement, optional None fields, empty file and invalid empty present tables follow §3 exactly.
- [ ] PNRF-REQ-003: unknown keys/roles, non-table sections, blank/untrimmed strings, invalid provider identifiers and model whitespace, invalid bool/numeric reasoning and invalid injected bindings fail with safe ConfigurationError; frozen assignment fails.
- [ ] PNRF-REQ-003: error strings do not echo a test sentinel embedded in path/file/unknown values; no provider key is required or consumed.
- [ ] PNRF-REQ-013: every required command passes, old tests unchanged, and diff stays within boundaries.

## Verification commands

Use prepared environment from repository root (PowerShell:
`. .venv/Scripts/Activate.ps1`); baseline `python scripts/verify.py` before edits.

```sh
python -m pytest -q tests/test_config.py
python scripts/verify.py
git diff --check
git diff
git status --short --branch
```

Expected: all exits 0; focused settings assertions pass, existing 62 cases remain
passing and Ruff reports All checks passed. Read new/untracked files too.
Record actual test count, branch/HEAD, warnings and scope review.

Implementation sequence: write focused failing tests for §3, run targeted suite
to establish failure, implement exact interfaces, rerun focused/final checks.
Update packet/progress at start and completion; no commit/integration step.

## Out of scope

- Runtime factory, agent migration, search routing, SDK errors and README overhaul.
- Registries, UI, config database, remote/dynamic config, new providers/dependencies.
- Other Task Packets and future features.

## Executor prompt

> Implement `tasks/001-runtime-configuration.md` following `AGENTS.md`. Do not expand scope.

## Execution record

- Assigned branch / baseline HEAD: Not started.
- Dependency evidence / baseline command and result: Not run.
- Final commands, exit codes and results: Not run.
- Acceptance/diff review: Not performed.
- Decisions within scope / limitations: None recorded.
- Blocker and required resolution / next safe step: None recorded.
