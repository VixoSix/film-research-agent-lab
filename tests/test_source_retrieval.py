from __future__ import annotations

from dataclasses import asdict

import pytest

from app.source_retrieval import (
    InvalidRetrievalInputError,
    MalformedProviderResponseError,
    MissingCredentialsError,
    ProviderError,
    search_web,
)


class FakeClient:
    _missing = object()

    def __init__(self, response=_missing, error=None):
        self.response = {"results": []} if response is self._missing else response
        self.error = error
        self.calls = []

    def search(self, query, **kwargs):
        self.calls.append((query, kwargs))
        if self.error:
            raise self.error
        return self.response


def result(url="https://example.com/article", **extra):
    return {"url": url, **extra}


def test_default_request_options_and_standard_mapping():
    client = FakeClient()

    search_web("  focused query  ", client=client)

    assert client.calls == [
        (
            "focused query",
            {"max_results": 5, "search_depth": "basic", "include_answer": False},
        )
    ]


def test_deep_maps_to_advanced():
    client = FakeClient()

    search_web("query", search_depth="deep", client=client)

    assert client.calls[0][1]["search_depth"] == "advanced"


def test_explicit_max_results_is_forwarded():
    client = FakeClient()

    search_web("query", max_results=10, client=client)

    assert client.calls[0][1]["max_results"] == 10


@pytest.mark.parametrize("query", ["", "   ", None, 42])
def test_invalid_query_fails_before_provider_call(query):
    client = FakeClient()

    with pytest.raises(InvalidRetrievalInputError):
        search_web(query, client=client)

    assert client.calls == []


@pytest.mark.parametrize("max_results", [True, False, 0, -1, 11, 1.5, "5"])
def test_invalid_max_results_fails_before_provider_call(max_results):
    client = FakeClient()

    with pytest.raises(InvalidRetrievalInputError):
        search_web("query", max_results=max_results, client=client)

    assert client.calls == []


@pytest.mark.parametrize("search_depth", ["fast", "ultra-fast", "basic", "", None, [], {}])
def test_invalid_search_depth_fails_before_provider_call(search_depth):
    client = FakeClient()

    with pytest.raises(InvalidRetrievalInputError):
        search_web("query", search_depth=search_depth, client=client)

    assert client.calls == []


def test_missing_credentials_fails_before_client_creation(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)

    class UnexpectedClient:
        def __init__(self, *_args, **_kwargs):
            raise AssertionError("TavilyClient must not be created")

    monkeypatch.setattr("app.source_retrieval.service.TavilyClient", UnexpectedClient)

    with pytest.raises(MissingCredentialsError):
        search_web("query")


def test_blank_credentials_fail_before_client_creation(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "   ")

    class UnexpectedClient:
        def __init__(self, *_args, **_kwargs):
            raise AssertionError("TavilyClient must not be created")

    monkeypatch.setattr("app.source_retrieval.service.TavilyClient", UnexpectedClient)

    with pytest.raises(MissingCredentialsError):
        search_web("query")


def test_normal_result_normalization_and_trace_metadata():
    client = FakeClient(
        {
            "request_id": "request-1",
            "response_time": 0.25,
            "results": [
                result(
                    title="Article",
                    content="Provider content",
                    result_id="result-1",
                    score=0.9,
                    published_date="2026-01-15",
                )
            ],
        }
    )

    retrieved = search_web("query", client=client)
    candidate = retrieved.candidates[0]

    assert candidate.url == "https://example.com/article"
    assert candidate.provider == "tavily"
    assert candidate.title == "Article"
    assert candidate.content == "Provider content"
    assert candidate.domain == "example.com"
    assert candidate.provider_metadata == {
        "result_position": 1,
        "result_id": "result-1",
        "relevance_score": 0.9,
        "published_date": "2026-01-15",
    }
    assert asdict(retrieved.trace) == {"request_id": "request-1", "response_time": 0.25}


def test_optional_fields_remain_absent():
    retrieved = search_web("query", client=FakeClient({"results": [result()]}))
    candidate = retrieved.candidates[0]

    assert candidate.title is None
    assert candidate.content is None
    assert candidate.domain == "example.com"
    assert candidate.provider_metadata == {"result_position": 1}


def test_non_string_optional_provider_text_is_absent():
    retrieved = search_web(
        "query",
        client=FakeClient({"results": [result(title={"not": "text"}, content=["not text"])]}),
    )

    candidate = retrieved.candidates[0]
    assert candidate.title is None
    assert candidate.content is None


def test_domain_is_derived_from_exact_url():
    retrieved = search_web(
        "query", client=FakeClient({"results": [result("https://www.example.com:443/path")]} )
    )

    assert retrieved.candidates[0].domain == "www.example.com"
    assert retrieved.candidates[0].url == "https://www.example.com:443/path"


def test_unusable_domain_is_absent():
    retrieved = search_web("query", client=FakeClient({"results": [result("https://")]}))

    assert retrieved.candidates == []
    assert retrieved.warnings[0].result_position == 1


def test_exact_url_duplicates_keep_first_and_preserve_order():
    client = FakeClient(
        {
            "results": [
                result("https://one.example", title="first"),
                result("https://one.example", title="second"),
                result("https://two.example", title="third"),
            ]
        }
    )

    retrieved = search_web("query", client=client)

    assert [candidate.url for candidate in retrieved.candidates] == [
        "https://one.example",
        "https://two.example",
    ]
    assert retrieved.candidates[0].title == "first"


def test_distinct_urls_are_not_merged():
    retrieved = search_web(
        "query",
        client=FakeClient(
            {
                "results": [
                    result("https://one.example", title="same"),
                    result("https://two.example", title="same"),
                ]
            }
        ),
    )

    assert len(retrieved.candidates) == 2


def test_malformed_individual_items_are_omitted_with_warning():
    retrieved = search_web(
        "query",
        client=FakeClient(
            {
                "results": [
                    {"title": "missing url"},
                    result("ftp://example.com/file"),
                    result("https://valid.example"),
                ]
            }
        ),
    )

    assert [candidate.url for candidate in retrieved.candidates] == ["https://valid.example"]
    assert [warning.result_position for warning in retrieved.warnings] == [1, 2]


@pytest.mark.parametrize("response", [None, [], {"results": "not-a-list"}, {"data": []}])
def test_malformed_response_fails(response):
    client = FakeClient(response=response)

    with pytest.raises(MalformedProviderResponseError):
        search_web("query", client=client)


def test_empty_results_are_successful():
    retrieved = search_web("query", client=FakeClient({"results": []}))

    assert retrieved.candidates == []
    assert retrieved.warnings == []


def test_timeout_becomes_safe_provider_error():
    client = FakeClient(error=TimeoutError("secret request details"))

    with pytest.raises(ProviderError, match="timed out") as raised:
        search_web("query", client=client)

    assert raised.value.category == "timeout"
    assert "secret" not in str(raised.value)


def test_generic_provider_failure_becomes_safe_provider_error():
    client = FakeClient(error=RuntimeError("secret provider response"))

    with pytest.raises(ProviderError, match="provider request failed") as raised:
        search_web("query", client=client)

    assert raised.value.category == "provider"
    assert "secret" not in str(raised.value)
