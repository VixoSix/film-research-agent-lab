from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceCandidate:
    url: str
    provider: str
    provider_metadata: dict[str, Any]
    title: str | None = None
    domain: str | None = None
    content: str | None = None


@dataclass(frozen=True)
class RetrievalTrace:
    request_id: str | None = None
    response_time: float | None = None


@dataclass(frozen=True)
class RetrievalWarning:
    type: str
    result_position: int
    message: str


@dataclass(frozen=True)
class RetrievalResult:
    query: str
    candidates: list[SourceCandidate] = field(default_factory=list)
    trace: RetrievalTrace = field(default_factory=RetrievalTrace)
    warnings: list[RetrievalWarning] = field(default_factory=list)
