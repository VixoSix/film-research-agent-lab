# Film Research Agent Lab

A learning project for deep film research using AI agents, source retrieval, RAG and evidence-based synthesis.

## Purpose

Film Research Agent Lab explores how AI agents can assist with deeper film research by discovering, organizing and verifying information from interviews, first-hand accounts, production stories and specialized sources.

The goal is not to replace basic film databases or search engines, but to investigate information that often requires deeper research and source comparison.

## Status

Early development.

## Phase 1

The first phase will explore:

- AI agents with Google ADK.
- Film metadata and external research tools.
- Interview and first-hand source discovery.
- Source verification and evidence tracking.
- Retrieval-Augmented Generation (RAG).
- Local embeddings and vector search.
- Automated agent evaluations.
- FastAPI.
- Docker.
- GitHub Actions.

The project is designed to run using free or local tools whenever possible.

## Development Workflow

Think expensive once. Execute cheap many times.

A capable development Planner records significant features as requirements,
design and tasks in `specs/<feature>/`, then prepares small execution
contracts using [tasks/TEMPLATE.md](tasks/TEMPLATE.md). Historical research
specifications remain in `specs/`; these planning artifacts do not imply that
future research capabilities have been implemented.

The user prepares one local `task/<NNN>-<slug>` branch from integrated `develop`
per Task Packet. A faster Executor follows [AGENTS.md](AGENTS.md), checks
dependencies, runs a baseline, implements only the packet and runs verification.
Status/evidence lives in the packet; `progress/current.md` and `history.md` keep
minimal development memory. DONE means verified locally. Commits, pushes,
merges, PRs and integration into `develop` are separate user-controlled actions;
agents never perform them automatically. `main` remains the stable release line.

See [development workflow](docs/development/workflow.md) for statuses,
BLOCKED handling, context and review policy, and the
[Development Harness spec](specs/development-harness/requirements.md) for
Task 000. A future execution prompt can be as short as:

```text
Implement tasks/007-example.md following AGENTS.md.
```

That path illustrates the prompt format; no Task 007 is created by Task 000.

## Development Setup

Prerequisites: Python >=3.11 and the existing project dependencies. GNU Make is
optional; it is only a convenience wrapper on Windows and is not required by the
canonical verification command.

Create the environment if absent, then install the existing dev extras:

```sh
python -m venv .venv
```

Activate it (`.venv\Scripts\Activate.ps1` in PowerShell, or
`source .venv/bin/activate` on POSIX), then run:

```sh
python -m pip install -e ".[dev]"
python scripts/verify.py
```

`python scripts/verify.py` runs `python -m pytest -q` then `python -m ruff check .`
with the same interpreter that launched the runner, stops on the first failure
and returns nonzero. If GNU Make is installed, `make verify` delegates to the
same runner; `make verify PYTHON=<executable>` selects the interpreter used by
the wrapper.
The existing automated tests use fake providers: no API keys, live Groq/Tavily
requests or provider quota are required. Live research smoke tests are separate,
manually authorized checks. This gate verifies deterministic code behavior and
linting; it does not evaluate research-model quality or Markdown consistency.

## License

This project is licensed under the MIT License.
