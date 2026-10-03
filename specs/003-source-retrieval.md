# Source Retrieval Specification

## 1. Purpose

The Source Retrieval layer accepts a focused research query and retrieves
candidate web sources through Tavily. It returns normalized source candidates
that later research agents can inspect, compare, and verify.

This layer is a retrieval boundary, not a research or reasoning agent. It
discovers candidate material and preserves enough information to trace each
candidate back to the provider response. It does not establish that a claim is
true, assess source reliability, or produce a research conclusion.

The layer should be reusable by the Research Planner's downstream research
threads and by later research agents without requiring those consumers to
depend on Tavily's response shape.

## 2. Responsibilities

The Source Retrieval layer shall:

- accept a focused, non-empty research query;
- accept optional retrieval controls within documented bounds;
- use Tavily as the configured web-search provider through Tavily's official
  Python SDK and `TavilyClient`;
- convert provider results into a normalized candidate-source structure;
- preserve original provider URLs and traceability metadata;
- handle duplicate, incomplete, empty, malformed, timed-out, and failed
  provider responses explicitly; and
- report insufficient retrieval without inventing a candidate or filling a
  missing field from memory or inference.

## 3. Non-Responsibilities and Boundaries

The layer shall not:

- verify claims or quotations;
- rate source reliability, authority, or evidentiary strength;
- decide what is true or resolve conflicting accounts;
- summarize multiple sources into findings or conclusions;
- perform retrieval-augmented generation (RAG);
- call an LLM;
- modify the Research Planner or generate research threads;
- implement a Research Agent; or
- silently replace a failed retrieval with model knowledge, cached prose, or a
  fabricated source.

A snippet or provider-returned content is a discovery aid only. It is not
verified evidence merely because retrieval succeeded.

## 4. Input Contract

The public input should use provider-neutral terminology. A request contains:

| Field | Required | Contract |
| --- | --- | --- |
| `query` | Yes | A focused research question or search phrase. It must be a non-empty string after trimming whitespace. The layer must pass the user's query semantically intact and must not add unsupported facts. |
| `max_results` | No | A positive integer in the inclusive range `1..10` limiting the number of candidates requested. If omitted, the application default is `5`. These are application-level limits independent of Tavily's broader provider limits. |
| `search_depth` | No | A provider-neutral retrieval-depth value: `standard` or `deep`. If omitted, the default is `standard`. Unsupported values, including `fast` and `ultra-fast`, are invalid input. |

The request may later be extended with other provider-neutral controls, but a
consumer must not need to supply Tavily-specific parameter names, endpoint
details, or response fields.

Input validation occurs before a provider call. Implementations must reject
missing requests, missing or blank queries, non-integer or out-of-range
`max_results` values, and unsupported `search_depth` values with an explicit
invalid-input error.

The initial implementation maps the provider-neutral depth values to Tavily as
follows:

| Public value | Tavily value |
| --- | --- |
| `standard` | `basic` |
| `deep` | `advanced` |

These Tavily values are implementation details and must remain behind the
retrieval boundary. The initial implementation must request
`include_answer=False`. Provider-generated answers are not part of this
retrieval contract; the layer retrieves source candidates only.

## 5. Output Contract

### 5.1 Retrieval result

A successful operation returns a retrieval result containing:

- the original normalized query used for the request;
- the effective retrieval options, when relevant;
- an ordered list of zero or more normalized source candidates; and
- retrieval trace metadata sufficient to identify the provider operation,
  subject to the provider's available metadata and privacy constraints.

An empty candidate list is a successful, explicit no-results outcome. It is
not permission to generate a likely source.

### 5.2 Candidate source

Each candidate source has the following fields:

| Field | Required for a returned candidate | Meaning |
| --- | --- | --- |
| `url` | Yes | The original, non-empty URL returned by the provider. It must be preserved rather than rewritten, canonicalized destructively, or guessed. |
| `provider` | Yes | The provider identifier, currently `tavily`. |
| `provider_metadata` | Yes | An opaque, serializable record that always includes `result_position` and preserves provider result metadata when supplied, including `result_id`, provider relevance score, and `published_date`. |
| `title` | No | The provider-returned title, when present and valid. |
| `domain` | No | A domain derived mechanically from the preserved URL using URL parsing. If a usable domain cannot be derived, this field remains absent. It must never be inferred from a title or snippet. Tavily need not provide a separate domain field. |
| `snippet` or `content` | No | Provider-returned discovery text, such as a snippet or available content. The original text and its provenance must be retained; the layer must not paraphrase or enrich it. |

The implementation may expose a single optional text field or separate
`snippet` and `content` fields, but it must distinguish provider text from
generated text and must document the chosen representation. A missing optional
field remains absent; it must not be replaced with an empty claim, inferred
title, invented domain, or generated summary.

The candidate structure may include additional non-semantic trace fields or
provider fields, provided they do not obscure the normalized contract and do
not claim verification. A Tavily relevance score is retrieval-ranking
metadata only. It is not a measure of source reliability, authority,
truthfulness, or evidentiary strength.

Retrieval-level trace metadata should preserve, when available:

- `request_id`;
- `response_time`; and
- safe provider-operation diagnostics needed for traceability.

### 5.3 Ordering and status

Candidates retain provider order unless the implementation documents a
deterministic normalization step. The layer must not reorder candidates by an
invented reliability score. A result should make the outcome distinguishable
among successful candidates, successful empty results, and explicit errors.

## 6. Source Identity and Traceability

The following rules are mandatory:

- Preserve the original URL returned by Tavily in the candidate's `url` field.
- Never invent a URL, title, domain, snippet, content, provider identifier, or
  provider metadata.
- Every returned candidate's `provider_metadata` must include its
  provider-ordered `result_position`.
- Preserve `result_id`, provider relevance score, and `published_date` when
  supplied by Tavily. If any are not supplied, leave them absent; do not
  invent them.
- Preserve retrieval-level `request_id` and `response_time` when available.
- A provider relevance score is ranking metadata only, not source reliability,
  authority, truthfulness, or evidentiary strength.
- Do not treat a URL, title, or snippet as proof that the page was opened,
  inspected, or verified.
- Do not silently normalize a URL in a way that loses query parameters,
  fragments, redirects, or other identity information.

### Duplicate results

Duplicate candidates should be collapsed deterministically within one retrieval
operation when they represent the same original URL under the provider's
returned URL value. The first provider-ordered occurrence is retained, and
trace metadata for subsequent duplicate occurrences is preserved where the
contract allows it.

Implementations must not merge different URLs merely because their titles,
domains, or snippets look similar. URL canonicalization may be used only as a
separate comparison key if it is documented and lossless for traceability; the
original URL must still be returned. Duplicates across separate retrieval
operations are a consumer/storage concern unless a later layer defines a
cross-request identity policy.

### Malformed provider results

A provider item is malformed when it cannot supply the required identity and
traceability needed for a candidate, especially a missing, blank, or invalid
URL. The layer must not manufacture replacement fields. The implementation
must use one consistent, documented policy: either omit the malformed item and
return a structured warning in retrieval trace metadata, or fail the whole
operation with a malformed-provider-response error. It must never return the
malformed item as a normal candidate or silently conceal the condition.

For this project, the recommended policy is to omit malformed individual items
while preserving a warning/count in the result when the remaining provider
response is structurally usable. If the response envelope or required result
collection is malformed, fail explicitly rather than returning a partial list
that could be mistaken for a complete provider response.

## 7. Credentials and Error Behavior

Errors are explicit and typed or otherwise machine-distinguishable. They must
include a safe human-readable message and must not expose the API key.

### Missing `TAVILY_API_KEY`

If the configured `TAVILY_API_KEY` is missing or blank, retrieval must fail
before making a provider call with a missing-credentials error. The layer must
not return an empty result, use another key implicitly, or fabricate candidates.

### Invalid input

Invalid requests fail before a provider call with an invalid-input error. The
error identifies the invalid field(s) without treating user input as evidence.

### Empty result set

When Tavily successfully returns no usable candidates, retrieval returns an
explicit successful empty result. This outcome must remain distinguishable from
missing credentials, timeout, provider failure, and malformed response.

### Provider timeout or provider error

A timeout, authentication failure reported by Tavily, rate-limit response, or
other provider failure returns an explicit provider-error outcome with the
category and safe diagnostic metadata when available. It must not be converted
to an empty result or retried indefinitely. Retry behavior, if later added,
must be bounded, documented, and must preserve the final error when retries are
exhausted.

### Malformed provider response

If the provider response envelope or required result collection cannot be
parsed or does not match the provider contract, retrieval fails explicitly with
a malformed-provider-response error. The layer must never guess the response
shape, return fabricated defaults, or claim that omitted data was unavailable
from the source page.

### Partial usable response

Individual malformed items may be omitted under the policy in Section 6. A
partially usable response must include an explicit warning or diagnostic count.
If the implementation cannot establish that the response envelope is usable,
it must fail rather than return a misleading partial success.

## 8. Grounding and Research Boundaries

This layer follows the grounding philosophy of the Core Research Agent and
Research Planner specifications:

- retrieved material is candidate evidence, not verified evidence;
- provider snippets and content retain attribution to the provider and source
  URL;
- later agents must inspect and verify source-dependent claims before using
  them in a dossier;
- absence of a result means only that this retrieval operation returned no
  usable candidate, not that the researched claim is false; and
- uncertainty, missing metadata, and provider limitations remain visible to
  downstream consumers.

The layer must remain independent of an LLM, RAG pipeline, claim database,
reliability classifier, synthesis prompt, and Research Planner implementation.

## 9. Testing Expectations

Unit tests shall use mocks, fakes, or deterministic provider fixtures. They
must not call Tavily or consume Tavily quota.

Tests should cover at least:

- valid focused query with default options;
- valid query with explicit `max_results` and supported retrieval depth;
- preservation and normalization of required and optional candidate fields;
- preservation of original URLs and provider trace metadata;
- deterministic duplicate handling without merging distinct URLs;
- omission/reporting of malformed individual items;
- failure for malformed response envelopes or result collections;
- missing `TAVILY_API_KEY` without a provider call;
- invalid query and invalid option values without a provider call;
- successful empty results;
- provider timeout/error and safe error reporting; and
- proof that no LLM, claim verification, source rating, or conclusion
  generation is performed by this layer.

A single live Tavily smoke test may be performed manually before merge to
confirm configuration and provider connectivity. It is not a substitute for
unit tests and must not be required for deterministic test execution.

## 10. Acceptance Criteria

Issue #7 is satisfied when an implementation can:

1. Accept a focused non-empty research query and optional bounded retrieval
   controls through a provider-neutral input contract.
2. Enforce `max_results` in the inclusive range `1..10`, defaulting to `5`,
   independently of Tavily's broader provider limits.
3. Support only public `search_depth` values `standard` and `deep`, defaulting
   to `standard`, and map them to Tavily `basic` and `advanced` respectively.
   Reject `fast`, `ultra-fast`, and other unsupported values.
4. Retrieve candidates through Tavily's official Python SDK and `TavilyClient`
   when valid credentials and input are available, with
   `include_answer=False`.
5. Return a normalized candidate structure with required `url`, `provider`,
   and `provider_metadata.result_position` fields, plus optional title,
   mechanically derived domain, provider text, and supplied trace metadata.
6. Preserve original provider URLs and never invent missing source metadata or
   content.
7. Preserve retrieval-level `request_id` and `response_time` when available,
   and preserve candidate `result_id`, relevance score, and `published_date`
   when supplied.
8. Treat Tavily relevance scores as ranking metadata only, never as source
   reliability, authority, truthfulness, or evidentiary strength.
9. Distinguish successful candidates, successful empty results, invalid input,
   missing credentials, provider failures/timeouts, and malformed responses.
10. Handle duplicate results deterministically and never merge distinct URLs
   solely on similarity of title, domain, or text.
11. Handle malformed individual provider items according to the documented
   omission-and-warning policy, and fail explicitly for unusable response
   envelopes or required collections.
12. Use only mocked, fake, or fixture-backed provider interactions in automated
   tests; no automated test consumes Tavily quota.
13. Never verify claims, rate source reliability, resolve truth, synthesize
    conclusions, perform RAG, call an LLM, modify the Research Planner, or
    implement a Research Agent.
14. Fail explicitly and never fabricate results when credentials, input,
    provider availability, or provider response structure is insufficient.
15. Remain consistent with the Core Research Agent's requirements for source
    traceability, uncertainty, insufficient evidence, and separation of user
    interpretation from evidence-based research.

## 11. Examples

### 11.1 Successful retrieval

**Input**

```text
query: "interviews with the cinematographer about the visual changes in Example Film"
max_results: 5
search_depth: standard
```

**Result**

```text
status: success
trace:
  provider: "tavily"
  request_id: "provider-request-id-123"
  response_time: 0.42
candidates:
  - title: "Example Film: A Conversation with ..."
    url: "https://publication.example/interview"
    domain: "publication.example"
    snippet: "Provider-returned discovery text..."
    provider: "tavily"
    provider_metadata:
      result_position: 1
      result_id: "provider-result-id-1"
      relevance_score: 0.91
      published_date: "2026-01-15"
```

The title, domain, and snippet above are returned only because the provider
supplied them, except that the domain is mechanically derived from the
preserved URL. The relevance score is retrieval-ranking metadata, not a source
reliability or truthfulness assessment. The retrieval layer does not claim that
the interview supports any particular research claim.

### 11.2 Empty result set

```text
status: success
candidates: []
trace:
  provider: "tavily"
  result_count: 0
```

This means that the operation found no usable candidates. It does not mean the
topic has no sources and does not authorize a guessed result.

### 11.3 Missing credentials

```text
input:
  query: "production interview about Example Film"
error:
  type: missing_credentials
  message: "TAVILY_API_KEY is required for source retrieval."
```

No provider request is made, and no candidate list is returned as if retrieval
had succeeded.

### 11.4 Malformed provider result

If Tavily returns one valid item and one item without a usable URL, the valid
item may be returned and the malformed item omitted:

```text
status: success_with_warnings
candidates:
  - url: "https://publication.example/article"
    provider: "tavily"
    provider_metadata:
      result_position: 1
warnings:
  - type: malformed_result_omitted
    result_position: 2
```

If the response has no usable result collection at all, the operation instead
returns `malformed_provider_response` and returns no candidates.

### 11.5 Provider failure

```text
error:
  type: provider_error
  category: timeout
  message: "Tavily source retrieval timed out."
  provider: "tavily"
```

This is not converted into an empty result. The caller can report that source
retrieval failed and decide whether a later bounded retry or another workflow
is appropriate; the retrieval layer does not fabricate a fallback source.

## 12. Explicit Design Decisions

- The public retrieval-depth contract exposes only `standard` and `deep`, with
  `standard` as the default. They map to Tavily `basic` and `advanced`,
  respectively. `fast` and `ultra-fast` are not exposed. Unsupported values
  are invalid input.
- `max_results` defaults to `5` and accepts only `1..10`. The maximum of `10`
  is an application-level limit independent of Tavily's broader provider
  limits.
- The initial implementation uses Tavily's official Python SDK and
  `TavilyClient`, while keeping those client details behind the retrieval
  boundary.
- The initial implementation requests `include_answer=False`. Provider-
  generated answers are excluded from the contract; only source candidates
  are retrieved.
- Retrieval-level trace metadata preserves `request_id` and `response_time`
  when available. Every candidate always includes `result_position`; supplied
  `result_id`, provider relevance score, and `published_date` are preserved.
- Tavily does not need to provide a separate domain. The implementation derives
  it mechanically from the preserved URL and leaves it absent when parsing
  cannot produce a usable domain. It never infers a domain from title or
  content.
- Individual malformed items are omitted with an explicit warning when the
  response envelope is usable; malformed envelopes or required collections
  fail explicitly.
