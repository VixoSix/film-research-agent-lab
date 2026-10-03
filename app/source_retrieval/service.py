from __future__ import annotations

import os
from collections.abc import Mapping
from urllib.parse import urlparse

from tavily import TavilyClient

from .errors import (
    InvalidRetrievalInputError,
    MalformedProviderResponseError,
    MissingCredentialsError,
    ProviderError,
)
from .models import RetrievalResult, RetrievalTrace, RetrievalWarning, SourceCandidate

_DEPTH_MAP = {"standard": "basic", "deep": "advanced"}
_MAX_RESULTS = 10


def search_web(
    query: str,
    *,
    max_results: int = 5,
    search_depth: str = "standard",
    client=None,
) -> RetrievalResult:
    normalized_query = _validate_input(query, max_results, search_depth)
    if client is None:
        api_key = os.environ.get("TAVILY_API_KEY", "").strip()
        if not api_key:
            raise MissingCredentialsError("TAVILY_API_KEY is required for source retrieval.")
        client = TavilyClient(api_key=api_key)

    try:
        response = client.search(
            normalized_query,
            max_results=max_results,
            search_depth=_DEPTH_MAP[search_depth],
            include_answer=False,
        )
    except Exception as exc:
        if _is_timeout(exc):
            raise ProviderError("Tavily source retrieval timed out.", category="timeout") from exc
        raise ProviderError("Tavily provider request failed.", category="provider") from exc

    return _normalize_response(normalized_query, response)


def _validate_input(query: str, max_results: int, search_depth: str) -> str:
    if not isinstance(query, str) or not query.strip():
        raise InvalidRetrievalInputError("query must be a non-empty string.")
    if isinstance(max_results, bool) or not isinstance(max_results, int):
        raise InvalidRetrievalInputError("max_results must be an integer from 1 through 10.")
    if not 1 <= max_results <= _MAX_RESULTS:
        raise InvalidRetrievalInputError("max_results must be an integer from 1 through 10.")
    if not isinstance(search_depth, str) or search_depth not in _DEPTH_MAP:
        raise InvalidRetrievalInputError("search_depth must be 'standard' or 'deep'.")
    return query.strip()


def _normalize_response(query: str, response) -> RetrievalResult:
    if not isinstance(response, Mapping) or not isinstance(response.get("results"), list):
        raise MalformedProviderResponseError("Tavily returned a malformed response.")

    candidates = []
    warnings = []
    seen_urls = set()
    for position, item in enumerate(response["results"], start=1):
        candidate = _candidate_from_item(item, position)
        if candidate is None:
            warnings.append(
                RetrievalWarning(
                    type="malformed_result_omitted",
                    result_position=position,
                    message="Provider result omitted because it lacked a usable HTTP or HTTPS URL.",
                )
            )
            continue
        if candidate.url in seen_urls:
            continue
        seen_urls.add(candidate.url)
        candidates.append(candidate)

    trace = RetrievalTrace(
        request_id=response.get("request_id"),
        response_time=response.get("response_time"),
    )
    return RetrievalResult(query=query, candidates=candidates, trace=trace, warnings=warnings)


def _candidate_from_item(item, position: int) -> SourceCandidate | None:
    if not isinstance(item, Mapping):
        return None
    url = item.get("url")
    parsed = _parse_http_url(url)
    if parsed is None:
        return None

    metadata = {"result_position": position}
    if "result_id" in item:
        metadata["result_id"] = item["result_id"]
    elif "id" in item:
        metadata["result_id"] = item["id"]
    if "score" in item:
        metadata["relevance_score"] = item["score"]
    if "published_date" in item:
        metadata["published_date"] = item["published_date"]

    return SourceCandidate(
        url=url,
        provider="tavily",
        provider_metadata=metadata,
        title=item.get("title") if isinstance(item.get("title"), str) else None,
        domain=parsed.hostname,
        content=item.get("content") if isinstance(item.get("content"), str) else None,
    )


def _parse_http_url(url):
    if not isinstance(url, str) or not url.strip() or url != url.strip():
        return None
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or not parsed.hostname:
            return None
    except ValueError:
        return None
    return parsed


def _is_timeout(error: Exception) -> bool:
    return isinstance(error, TimeoutError) or "timeout" in type(error).__name__.lower()
