from __future__ import annotations

import threading
from collections.abc import Mapping
from typing import Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext

from app import source_retrieval
from app.source_retrieval import (
    InvalidRetrievalInputError,
    MalformedProviderResponseError,
    MissingCredentialsError,
    ProviderError,
    RetrievalResult,
)

SEARCH_BUDGET = 2
SEARCH_MAX_RESULTS = 3
SEARCH_CALLS_STATE_KEY = "temp:research_agent_search_calls"
_SEARCH_BUDGET_LOCK = threading.Lock()


def reset_search_budget(callback_context: CallbackContext) -> None:
    """Reset the retrieval counter at the start of an ADK invocation."""
    with _SEARCH_BUDGET_LOCK:
        callback_context.state[SEARCH_CALLS_STATE_KEY] = 0


def search_web(query: str, tool_context: ToolContext) -> dict[str, Any]:
    """Search for candidate sources through the normalized retrieval boundary."""
    reserved, calls_used = _reserve_search_slot(tool_context)
    if not reserved:
        return _empty_outcome(
            status="search_budget_exhausted",
            query=query,
            calls_used=calls_used,
        )

    try:
        retrieved = source_retrieval.search_web(
            query,
            max_results=SEARCH_MAX_RESULTS,
        )
    except InvalidRetrievalInputError:
        return _error_outcome("invalid_input", query, calls_used)
    except MissingCredentialsError:
        return _error_outcome("missing_credentials", query, calls_used)
    except ProviderError as error:
        category = "timeout" if error.category == "timeout" else "provider"
        return _error_outcome("provider_error", query, calls_used, category=category)
    except MalformedProviderResponseError:
        return _error_outcome("malformed_response", query, calls_used)

    return _serialize_result(retrieved, calls_used)


def _reserve_search_slot(tool_context: ToolContext) -> tuple[bool, int]:
    with _SEARCH_BUDGET_LOCK:
        calls_used = int(tool_context.state.get(SEARCH_CALLS_STATE_KEY, 0))
        if calls_used >= SEARCH_BUDGET:
            return False, calls_used

        calls_used += 1
        tool_context.state[SEARCH_CALLS_STATE_KEY] = calls_used
        return True, calls_used


def _serialize_result(result: RetrievalResult, calls_used: int) -> dict[str, Any]:
    candidates = []
    for candidate in result.candidates:
        candidates.append(
            {
                "url": candidate.url,
                "provider": candidate.provider,
                "provider_metadata": _json_safe(candidate.provider_metadata),
                "title": candidate.title,
                "domain": candidate.domain,
                "content": candidate.content,
            }
        )

    payload = {
        "status": "ok" if candidates else "empty_result",
        "normalized_query": result.query,
        "candidates": candidates,
        "retrieval_trace": {
            "request_id": result.trace.request_id,
            "response_time": result.trace.response_time,
        },
        "warnings": [
            {
                "type": warning.type,
                "result_position": warning.result_position,
                "message": warning.message,
            }
            for warning in result.warnings
        ],
    }
    return _with_budget(payload, calls_used)


def _error_outcome(
    status: str,
    query: str,
    calls_used: int,
    *,
    category: str | None = None,
) -> dict[str, Any]:
    payload = _empty_outcome(status=status, query=query, calls_used=calls_used)
    if category is not None:
        payload["category"] = category
    return payload


def _empty_outcome(status: str, query: str, calls_used: int) -> dict[str, Any]:
    return _with_budget(
        {
            "status": status,
            "normalized_query": query.strip() if isinstance(query, str) else "",
            "candidates": [],
            "retrieval_trace": {"request_id": None, "response_time": None},
            "warnings": [],
        },
        calls_used,
    )


def _with_budget(payload: dict[str, Any], calls_used: int) -> dict[str, Any]:
    payload["calls_used"] = calls_used
    payload["remaining_budget"] = max(SEARCH_BUDGET - calls_used, 0)
    return payload


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return str(value)
