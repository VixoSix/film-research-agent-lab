from __future__ import annotations

import inspect
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path
from typing import get_type_hints

import pytest

from app.source_retrieval import (
    InvalidRetrievalInputError,
    MalformedProviderResponseError,
    MissingCredentialsError,
    ProviderError,
    RetrievalResult,
    RetrievalTrace,
    RetrievalWarning,
    SourceCandidate,
)


class FakeToolContext:
    def __init__(self, state: dict | None = None):
        self.state = {} if state is None else state


class RaceExposingState:
    """Releases unsynchronized readers together before returning the value."""

    def __init__(self, readers: int):
        self._values = {}
        self._readers = readers
        self._active_readers = 0
        self._active_lock = threading.Lock()
        self._all_readers = threading.Event()

    def get(self, key, default=None):
        with self._active_lock:
            self._active_readers += 1
            if self._active_readers == self._readers:
                self._all_readers.set()

        value = self._values.get(key, default)
        # Unsynchronized implementations release all readers here and make
        # them observe the same stale counter. A locked reservation times out
        # one reader at a time and then observes the updated value.
        self._all_readers.wait(timeout=0.2)
        with self._active_lock:
            self._active_readers -= 1
        return value

    def __setitem__(self, key, value):
        self._values[key] = value


def retrieval_result(*, candidates=None, warnings=None) -> RetrievalResult:
    return RetrievalResult(
        query="normalized query",
        candidates=[] if candidates is None else candidates,
        trace=RetrievalTrace(request_id="request-1", response_time=0.25),
        warnings=[] if warnings is None else warnings,
    )


def candidate() -> SourceCandidate:
    return SourceCandidate(
        url="https://example.com/exact path",
        provider="tavily",
        provider_metadata={"result_position": 1, "relevance_score": 0.9},
        title="Candidate title",
        domain="example.com",
        content="Provider-returned discovery content.",
    )


def test_search_tool_delegates_to_public_source_retrieval(monkeypatch):
    from app.research_agent.tools import search_web

    calls = []

    def fake_search(query, **kwargs):
        calls.append((query, kwargs))
        return retrieval_result()

    monkeypatch.setattr("app.source_retrieval.search_web", fake_search)

    search_web("  focused query  ", FakeToolContext())

    assert calls == [("  focused query  ", {"max_results": 3})]


def test_model_facing_search_tool_schema_exposes_only_query():
    from app.research_agent.tools import search_web

    parameters = inspect.signature(search_web).parameters

    assert set(parameters) == {"query", "tool_context"}
    assert "max_results" not in parameters


def test_search_tool_serializes_normalized_retrieval_data(monkeypatch):
    from app.research_agent.tools import search_web

    warning = RetrievalWarning(
        type="malformed_result_omitted",
        result_position=2,
        message="A result was omitted.",
    )
    monkeypatch.setattr(
        "app.source_retrieval.search_web",
        lambda query, **kwargs: retrieval_result(
            candidates=[candidate()], warnings=[warning]
        ),
    )

    result = search_web("query", FakeToolContext())

    assert result == {
        "status": "ok",
        "normalized_query": "normalized query",
        "candidates": [asdict(candidate())],
        "retrieval_trace": {"request_id": "request-1", "response_time": 0.25},
        "warnings": [asdict(warning)],
        "calls_used": 1,
        "remaining_budget": 1,
    }
    json.dumps(result)


def test_search_tool_represents_empty_result_without_fabrication(monkeypatch):
    from app.research_agent.tools import search_web

    monkeypatch.setattr(
        "app.source_retrieval.search_web", lambda query, **kwargs: retrieval_result()
    )

    result = search_web("query", FakeToolContext())

    assert result["status"] == "empty_result"
    assert result["candidates"] == []
    assert result["normalized_query"] == "normalized query"
    assert result["remaining_budget"] == 1


@pytest.mark.parametrize(
    ("error", "status"),
    [
        (InvalidRetrievalInputError("secret invalid details"), "invalid_input"),
        (MissingCredentialsError("TAVILY_API_KEY=secret"), "missing_credentials"),
        (ProviderError("secret provider details", category="timeout"), "provider_error"),
        (MalformedProviderResponseError("secret response details"), "malformed_response"),
    ],
)
def test_search_tool_maps_project_errors_to_safe_outcomes(monkeypatch, error, status):
    from app.research_agent.tools import search_web

    monkeypatch.setattr(
        "app.source_retrieval.search_web",
        lambda query, **kwargs: (_ for _ in ()).throw(error),
    )

    result = search_web("query", FakeToolContext())

    assert result["status"] == status
    assert result["candidates"] == []
    assert result["remaining_budget"] == 1
    assert "secret" not in json.dumps(result)
    assert "exception" not in json.dumps(result).lower()


def test_search_budget_allows_two_calls_and_blocks_third(monkeypatch):
    from app.research_agent.tools import search_web

    calls = []

    def fake_search(query, **kwargs):
        calls.append(query)
        return retrieval_result()

    monkeypatch.setattr("app.source_retrieval.search_web", fake_search)
    context = FakeToolContext()

    first = search_web("one", context)
    second = search_web("two", context)
    third = search_web("three", context)

    assert first["calls_used"] == 1
    assert first["remaining_budget"] == 1
    assert second["calls_used"] == 2
    assert second["remaining_budget"] == 0
    assert third == {
        "status": "search_budget_exhausted",
        "normalized_query": "three",
        "candidates": [],
        "retrieval_trace": {"request_id": None, "response_time": None},
        "warnings": [],
        "calls_used": 2,
        "remaining_budget": 0,
    }
    assert calls == ["one", "two"]


@pytest.mark.parametrize("retrieval", [lambda: retrieval_result(), lambda: (_ for _ in ()).throw(ProviderError("failed"))])
def test_failed_or_empty_search_consumes_budget(monkeypatch, retrieval):
    from app.research_agent.tools import search_web

    calls = []

    def fake_search(query, **kwargs):
        calls.append(query)
        return retrieval()

    monkeypatch.setattr("app.source_retrieval.search_web", fake_search)
    context = FakeToolContext()

    search_web("one", context)
    search_web("two", context)
    exhausted = search_web("three", context)

    assert exhausted["status"] == "search_budget_exhausted"
    assert calls == ["one", "two"]


def test_budget_reset_is_invocation_scoped():
    from app.research_agent.tools import reset_search_budget, search_web

    context = FakeToolContext()
    reset_search_budget(context)
    context.state["temp:research_agent_search_calls"] = 2

    reset_search_budget(context)

    assert context.state["temp:research_agent_search_calls"] == 0
    assert search_web.__name__ == "search_web"


def test_concurrent_searches_reserve_at_most_two_slots(monkeypatch):
    from app.research_agent.tools import search_web

    source_calls = []
    source_calls_lock = threading.Lock()

    def fake_search(query, **kwargs):
        with source_calls_lock:
            source_calls.append(query)
        return retrieval_result(candidates=[candidate()])

    monkeypatch.setattr("app.source_retrieval.search_web", fake_search)
    context = FakeToolContext(state=RaceExposingState(readers=4))

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda index: search_web(f"query-{index}", context), range(4)))

    assert len(source_calls) == 2
    assert sum(result["status"] == "search_budget_exhausted" for result in results) == 2
    assert all(result["calls_used"] <= 2 for result in results)
    assert all(result["remaining_budget"] >= 0 for result in results)


def test_reset_search_budget_uses_documented_adk_callback_context():
    from google.adk.agents.callback_context import CallbackContext

    from app.research_agent.tools import reset_search_budget

    assert get_type_hints(reset_search_budget)["callback_context"] is CallbackContext


def test_research_agent_package_has_no_direct_tavily_dependency():
    package = Path("app/research_agent")
    source = "\n".join(path.read_text(encoding="utf-8") for path in package.glob("*.py"))

    assert "TavilyClient" not in source
    assert "import tavily" not in source
    assert "TAVILY_API_KEY" not in source


def test_root_agent_configuration():
    from google.adk.models.lite_llm import LiteLlm

    from app.research_agent.agent import root_agent

    assert root_agent.name == "research_agent"
    assert isinstance(root_agent.model, LiteLlm)
    assert root_agent.model.model == "groq/openai/gpt-oss-120b"
    assert root_agent.model._additional_args["include_reasoning"] is False
    assert any(
        getattr(tool, "name", getattr(tool, "__name__", None)) == "search_web"
        for tool in root_agent.tools
    )
    assert root_agent.before_agent_callback


def test_root_agent_instruction_has_grounding_boundaries():
    from app.research_agent.agent import root_agent

    instruction = root_agent.instruction.lower()

    for phrase in (
        "one focused research thread",
        "preliminary research",
        "exact source url",
        "candidate urls",
        "discovery material",
        "not verified evidence",
        "relevance score is not reliability",
        "never invent",
        "model memory",
        "search budget",
        "no final dossier",
        "no verification",
        "no rag",
        "no multi-agent orchestration",
    ):
        assert phrase in instruction


def test_root_agent_instruction_has_output_contract():
    from app.research_agent.agent import root_agent

    instruction = " ".join(root_agent.instruction.lower().split())

    for section in (
        "research thread",
        "search decision",
        "search queries performed",
        "candidate sources",
        "preliminary observations",
        "conflicting or incomplete information",
        "evidence limitations",
        "verification needs",
    ):
        assert section in instruction


def test_root_agent_instruction_hardens_live_grounding_boundaries():
    from app.research_agent.agent import root_agent

    instruction = " ".join(root_agent.instruction.lower().split())

    for phrase in (
        "derive search-budget reporting exclusively from tool-returned calls_used",
        "tool-returned remaining_budget",
        "tool-returned status",
        "never calculate, infer, or guess budget state",
        "only status=search_budget_exhausted or remaining_budget=0",
        "if remaining_budget=1, do not describe the budget as exhausted",
        "do not use qualitative source-quality labels",
        "reputable",
        "credible",
        "reliable",
        "authoritative",
        "low-authority",
        "weak source",
        "strong source",
        "trustworthy",
        "questionable source",
        "provider-returned snippet/content",
        "snippet-level or discovery-level",
        "do not call it verified",
        "do not say a quote is confirmed or directly verified",
        "do not infer roles, identities, dates, relationships, importance, or context",
        "do not state that the page was inspected",
        "specific follow-up source",
        "returned by search_web in the current invocation",
        "explicitly supplied by the user/planner",
        "describe the verification need generically",
        "do not use model memory to name a likely source",
        "model memory cannot introduce specific source names, dates, authors, urls, or publications",
    ):
        assert phrase in instruction
