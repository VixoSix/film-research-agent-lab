# Research Agent Specification

## 1. Purpose

The Research Agent is the first Google ADK research agent after the Research
Planner. It accepts one focused research thread, decides whether external
retrieval is needed, uses the existing `search_web` source-retrieval boundary
when appropriate, and organizes preliminary source-backed research for later
verification.

The agent helps turn a planner thread into a small, inspectable research trail.
It preserves source attribution, original URLs, uncertainty, retrieval
warnings, and evidence limitations. Its output is preliminary research, not a
verified claim set or a final research dossier.

The initial agent handles one focused thread per invocation. It does not
maintain conversational research state across invocations.

## 2. Position in the Research Workflow

The components have separate responsibilities:

- **Research Planner:** transforms a user's broad request into focused,
  prioritized research threads, search directions, and evidence needs. It does
  not search or retrieve sources.
- **Source Retrieval layer:** accepts a focused query and retrieves normalized
  `RetrievalResult` and `SourceCandidate` values through Tavily. It does not
  interpret claims, select what is true, or call an LLM.
- **Research Agent:** decides whether a supplied thread needs retrieval,
  formulates bounded focused queries, and organizes returned candidates into
  preliminary observations with explicit attribution and limitations.
- **Future Verification Agent:** inspects retrieved source material and tests
  claims, quotations, attribution, chronology, and source independence. It is
  not part of Issue #9.
- **Final Research Dossier generation:** synthesizes verified findings,
  conflicts, evidence, and limitations into the structured dossier defined by
  the Core Research Agent specification. It is not part of Issue #9.

The Research Agent may use the planner's directions, but it must not modify the
Research Planner or silently expand one thread into a general film profile.

## 3. Responsibilities

The Research Agent shall:

- accept one focused research thread at a time;
- determine whether the thread requires external source discovery;
- formulate a small number of faithful search queries when retrieval is needed;
- invoke the existing `search_web` capability through an ADK tool boundary;
- preserve normalized candidate source data and provider traceability;
- organize candidate sources by relevance to the thread and availability of
  first-hand material, without assigning reliability scores;
- distinguish provider-returned snippets/content from inspected or verified
  evidence;
- record preliminary observations only when their source support or
  uncertainty is explicit; and
- report empty results, warnings, failures, and evidence gaps without
  fabrication.

## 4. Non-Responsibilities

The Research Agent shall not:

- perform final claim verification;
- act as the Verification Agent;
- decide which contradictory account is true;
- assign source reliability, authority, truthfulness, or evidentiary-strength
  scores;
- produce the final Research Dossier;
- perform RAG, embeddings, or vector search;
- use TMDB;
- orchestrate multiple agents;
- expose a FastAPI endpoint; or
- change the Research Planner's output or behavior.

The agent may state that a candidate appears relevant to the thread or that a
first-hand source should receive inspection priority. Those are retrieval and
workflow observations, not findings about truth or source quality.

## 5. Input Contract

One invocation receives a focused research-thread object containing:

| Field | Required | Meaning |
| --- | --- | --- |
| `research_question` | Yes | The focused question to investigate. It must be non-empty and should be answerable through a bounded source-discovery pass. |
| `why_it_matters` | Yes | A concise explanation of how the thread serves the user's research request. This provides priority context, not evidence. |
| `entities_and_terms` | No | User- or planner-supplied film titles, people, roles, events, periods, locations, phrases, or languages to use when forming queries. Each item remains an investigation term, not an established fact unless explicitly identified as user-provided. |
| `evidence_needs` | No | The kinds of material the later workflow should seek, such as a quotation, chronology, first-hand account, production decision, or comparison of accounts. |
| `preferred_source_types` | No | Source categories supplied by the planner or user, such as interviews, production documents, trade reporting, or specialist criticism. These guide search formulation and do not assert that such sources exist. |

The contract should remain small. It must not require Tavily parameters,
provider result fields, API keys, model settings, or a retrieval endpoint.

User-provided premises and planner hypotheses must remain distinguishable from
facts to establish. An input may include an unverified premise, but it must be
represented as a premise to investigate rather than as a confirmed event or
relationship.

## 6. ADK Tool Contract

The agent accesses web retrieval through the existing public `search_web`
function from `app.source_retrieval`. The ADK agent configuration exposes that
capability as a tool, directly or through a thin adapter whose only purpose is
to make the normalized result serializable to the agent runtime.

The tool boundary must preserve the following separation:

- the agent supplies a focused query and, only when justified by the public
  retrieval contract, provider-neutral retrieval options;
- the source-retrieval layer validates input, reads credentials, maps depth,
  calls Tavily, normalizes candidates, and raises project-defined errors;
- the agent receives `RetrievalResult`, `SourceCandidate`, trace metadata, and
  warnings rather than Tavily response objects; and
- candidate URLs, titles, content, and provider metadata remain attributed to
  the normalized retrieval result.

The Research Agent must not instantiate `TavilyClient`, import Tavily SDK
internals, read `TAVILY_API_KEY`, inspect `.env` files, or call any Tavily API
directly. It must not bypass `search_web` or depend on Tavily's response shape.

The tool adapter must not silently convert retrieval errors to an empty result,
invent a fallback candidate, or hide warnings. Tool failures must be returned
to the agent as explicit, safe error states that can be represented in the
preliminary output.

## 7. Deciding Whether to Retrieve

The agent should call `search_web` when the thread depends on external evidence,
including when:

- the question asks what happened, who said something, when a production event
  occurred, or how a creative decision was made;
- the user or planner explicitly requests sources, interviews, documents, or
  supporting evidence;
- the thread contains a factual production-history question that cannot be
  answered from the supplied thread context alone; or
- source discovery is needed to identify competing accounts, chronology, or
  first-hand material.

The agent should not call `search_web` when:

- the thread is only a request to restate or organize information already
  supplied, with no request for external evidence;
- the input is too ambiguous to form a faithful query and the agent can instead
  report the clarification needed; or
- the search budget for the invocation has been exhausted.

Model knowledge may help interpret wording or form a query, but it must not be
reported as evidence and must not be used to avoid retrieval for a question
that requires external support.

## 8. Search Budget and Termination

The initial application-level policy permits at most **two `search_web` tool
calls per Research Agent invocation**. This is a Research Agent policy,
independent of Tavily's `max_results` limit. Two calls allow one initial query
and one targeted refinement while keeping behavior predictable for a learning
project and preserving Tavily quota.

The budget must be enforced by invocation-scoped agent/tool state, not only by
an instruction that the model might ignore. Every attempted `search_web` call,
including one that fails or returns no candidates, consumes one budget unit.

The agent should stop before the second call when the first result set contains
enough relevant candidates to organize the thread, or when the first result
clearly shows that the query needs no refinement. It may use the second call
only for a materially narrower query faithful to the same thread, such as a
named participant, time period, or source type already supplied by the input.

When the budget is exhausted, the agent must stop searching and state that the
preliminary result is bounded by the two-call search budget. It must not retry
indefinitely, broaden into unrelated searches, or fabricate missing evidence.

## 9. Search Query Generation

Queries must:

- remain faithful to `research_question` and `evidence_needs`;
- use supplied entities, roles, periods, and terms when they improve source
  discovery;
- be focused enough to retrieve sources for one thread rather than a general
  film overview;
- preserve uncertainty in the question; and
- avoid adding unsupported factual premises.

If a thread contains an unverified premise, the query must be conditional or
comparative. For example, a query may seek accounts of whether a reported
on-set incident affected a creative decision, or compare accounts of the
alleged incident. It must not turn “I heard that an incident changed the scene”
into “the incident that changed the scene” as if causation were established.

The agent may generate a query that includes a person or role supplied by the
planner, but it must not invent a participant, date, publication, interview
title, event, or quotation to make the query more specific.

## 10. Handling Tool Results

The agent receives normalized retrieval values and must:

- preserve each candidate's exact original URL;
- preserve candidate title, domain, provider text, and trace metadata when
  available without rewriting them as verified facts;
- keep a clear relationship between every source-dependent observation and one
  or more candidate URLs;
- distinguish provider snippets/content from source material that a future
  agent has actually inspected;
- treat a Tavily relevance score only as retrieval-ranking metadata, never as
  reliability, authority, truthfulness, or evidentiary strength;
- not claim that a page, interview, quotation, or document was fully inspected
  merely because a candidate or snippet was returned;
- retain missing fields, warnings, uncertainty, and competing accounts; and
- retain the search query that produced each candidate set.

The agent may group or prioritize sources by apparent relevance to the thread
and by availability of first-hand material. Such prioritization must be labeled
as a research-follow-up priority, not as a reliability judgment.

## 11. Preliminary Research Output Contract

Each invocation returns a structured preliminary research result with these
sections:

1. **Research thread** — the focused question, why it matters, and any
   relevant supplied scope or premises.
2. **Search decision** — whether retrieval was needed and a concise reason. If
   no search occurred, state the missing clarification or non-retrieval reason.
3. **Search queries performed** — the exact normalized queries issued, in
   order, with the number of calls used and the remaining/exhausted budget.
4. **Candidate sources** — normalized candidates grouped by query, retaining
   exact URLs, titles, domains, provider text, provider metadata, and retrieval
   warnings where available.
5. **Preliminary observations** — tentative organization of what the candidate
   material appears to address. Every source-dependent observation must include
   one or more candidate URLs. Observations based only on snippets must be
   labeled as snippet-level or discovery-level observations.
6. **Conflicting or incomplete information** — materially different accounts,
   missing metadata, unverified premises, empty results, or unresolved
   chronology. Do not resolve a contradiction as true or false.
7. **Evidence limitations** — retrieval failures, inaccessible or uninspected
   pages, provider warnings, budget limits, missing source types, and the fact
   that retrieval is not verification.
8. **Verification needs** — claims, quotations, dates, identities, causal links,
   or source passages that a future Verification Agent should inspect.

The result must not be called a verified dossier, verified findings, or a final
answer. A source-dependent observation without a candidate URL is invalid. If
no candidate URL exists, the result may report a search outcome or limitation,
but it must not present an unsupported factual observation.

## 12. Grounding Boundaries

The agent must never:

- invent sources, URLs, interviews, quotations, people, dates, incidents, or
  claims;
- claim that a source was retrieved when `search_web` did not return it;
- present a provider snippet or returned content as verified fact;
- claim to have opened or fully inspected a page based only on retrieval;
- resolve contradictions as true or false;
- assign reliability, authority, truthfulness, or evidentiary-strength scores;
- fabricate fallback evidence after empty results or retrieval failure; or
- use model memory as hidden evidence.

Model knowledge may help understand the user's wording and formulate focused
queries. It must remain invisible as evidence: any factual statement in the
preliminary result must either be tied to candidate URLs or be explicitly
identified as a user/planner premise, a search limitation, or a future
verification need.

## 13. Empty Results and Errors

The agent must preserve the distinction among these outcomes:

- **Successful retrieval with zero candidates:** report that the bounded search
  returned no usable candidates for the query. Do not infer that no sources
  exist and do not fabricate a substitute.
- **Partial results with retrieval warnings:** retain valid candidates, show
  the warning and affected provider result position, and state that the result
  set may be incomplete.
- **Invalid retrieval input:** surface an explicit retrieval limitation. The
  agent should not repeatedly issue the same invalid query; it may reformulate
  once only if the reformulation remains faithful and within the remaining
  budget.
- **Missing credentials:** state that source retrieval could not run because
  credentials were unavailable. Do not expose the key or claim that no sources
  exist.
- **Provider timeout or error:** state that the provider request failed or
  timed out, preserve any safe category, and do not convert the failure to an
  empty successful result.
- **Malformed provider response:** state that the provider response could not
  be normalized. Do not guess fields or return fabricated candidates.

All of these limitations must appear in **Evidence limitations** and, where
they affect the thread, in **Verification needs**.

## 14. Source Organization and Prioritization

The agent may organize candidates for follow-up using only transparent,
question-specific criteria such as:

- direct relevance to the focused research question;
- whether the candidate appears to be an interview, first-hand account,
  production document, trade report, specialist source, or another requested
  source type; and
- whether the candidate contains provider-returned text useful for deciding
  what a future agent should inspect.

These criteria are retrieval priorities, not source reliability or truthfulness
assessments. Relevance ranking must not be presented as proof, corroboration,
authority, or evidentiary weight.

## 15. Multi-Turn Behavior

Issue #9 requires one focused research thread per invocation only. The initial
implementation does not promise multi-turn continuity, persistent search
history, cross-invocation deduplication, or resumption of an exhausted budget.

The output's search queries, candidates, warnings, and limitations provide the
research trail that a later invocation or agent may consume explicitly. Any
future multi-turn design must define how prior evidence is supplied and must
not assume hidden conversational state.

## 16. Testing Expectations

Automated tests must not call Groq, Tavily, or any live external provider.

Deterministic tests should cover:

- ADK agent configuration includes the Research Agent identity, instructions,
  and the retrieval tool boundary;
- `search_web` is exposed as the tool, directly or through a transparent
  adapter, and the agent configuration does not instantiate `TavilyClient`;
- grounding instructions prohibit fabrication, hidden model evidence,
  unqualified snippet claims, reliability scoring, and verification claims;
- the preliminary output contract contains all required sections and requires
  source URLs for source-dependent observations;
- one focused thread is accepted and unrelated multi-thread orchestration is
  not required;
- the invocation-scoped search budget allows no more than two tool calls;
- a first-call result can stop further searching when sufficient candidates are
  available, while an explicitly narrower refinement can consume the second
  call;
- empty results, warnings, invalid input, missing credentials, provider
  failures, timeouts, and malformed responses can be represented safely
  without an LLM or live provider; and
- search queries preserve an unverified premise conditionally rather than
  converting it into an asserted fact.

Tests should verify the tool boundary and deterministic orchestration policy,
not brittle wording or the exact prose that a future model may generate.
Model quality, source relevance, and nuanced research usefulness belong in
future agent evaluations and manual review.

## 17. Manual Live Smoke Test

Before merge, one authorized manual smoke test may run the configured ADK
Research Agent against a focused film-research thread with valid Groq and
Tavily credentials. The test must confirm that:

1. ADK invokes the exposed `search_web` tool rather than a direct Tavily
   client.
2. Tavily returns normalized candidates through the existing source-retrieval
   layer.
3. The agent produces preliminary research organized around the supplied
   thread.
4. Original candidate URLs remain visible in the output.
5. Returned snippets/content are labeled as discovery material and are not
   presented as verified evidence.
6. The agent performs no more than two retrieval calls for the invocation.

The smoke test is manual and is not part of automated test execution. It must
not be used to justify claims about source truthfulness or final verification.

## 18. Out of Scope

The following are explicitly outside Issue #9:

- final claim verification;
- a Verification Agent;
- source reliability scoring or truthfulness classification;
- RAG;
- embeddings or a vector database;
- TMDB or routine film metadata retrieval;
- multi-agent orchestration;
- final Research Dossier generation;
- FastAPI or another web API; and
- multi-turn continuity or persistent agent memory.

## 19. Acceptance Criteria

Issue #9 is satisfied when an implementation can:

1. Accept exactly one focused research thread with the question, importance,
   optional entities/terms, evidence needs, and preferred source types.
2. Keep the Research Agent distinct from the Research Planner, Source
   Retrieval layer, future Verification Agent, and final dossier generator.
3. Decide whether external retrieval is required without presenting model
   memory as evidence.
4. Expose the existing public `search_web` capability through ADK tool calling
   without direct `TavilyClient` construction, API-key access, `.env` access,
   or Tavily response-shape dependencies in the agent.
5. Generate focused queries faithful to the research thread and supplied
   terms, including conditional wording for unverified premises.
6. Enforce no more than two `search_web` calls per invocation and stop with an
   explicit budget limitation when the budget is exhausted.
7. Preserve exact candidate URLs, provider attribution, trace metadata,
   warnings, and uncertainty from normalized retrieval results.
8. Never treat snippets/content as inspected or verified evidence and never
   treat relevance ranking as reliability, authority, truthfulness, or
   evidentiary strength.
9. Produce preliminary output with the required thread, query, candidate,
   observation, conflict/incompleteness, limitation, and verification sections.
10. Tie every source-dependent observation to one or more candidate URLs.
11. Represent empty results, partial warnings, invalid input, missing
    credentials, provider failures/timeouts, and malformed responses explicitly
    without fabricating sources or fallback evidence.
12. Avoid final verification, reliability scoring, RAG, embeddings/vector
    search, TMDB, multi-agent orchestration, final dossier generation, FastAPI,
    and multi-turn continuity.
13. Provide deterministic tests for configuration, tool exposure, grounding
    instructions, output structure, bounded search behavior, and safe retrieval
    failure representation without live Groq or Tavily calls.
14. Pass one manual smoke test demonstrating ADK tool calling, normalized
    candidates, visible URLs, preliminary sourced organization, and explicit
    non-verification of retrieved content.

## 20. Examples

### 20.1 Normal thread requiring web search

**Input thread:**

> Investigate how the production changed the film's visual approach. This
> matters because the user wants the cinematographer's account and the
> production reasons for the change. Search terms supplied by the planner:
> film title, cinematographer, visual approach, production changes. Prefer
> interviews and first-hand production accounts.

**Expected behavior:**

- Decide that external evidence is required.
- Call `search_web` with a focused query using the supplied film title and
  question, with no invented production event.
- Organize returned candidates and preserve each exact URL.
- State that snippets are discovery material requiring inspection.
- Record verification needs for the cinematographer's wording, dates, and any
  claimed causal link.

### 20.2 Thread containing an unverified premise

**Input thread:**

> Investigate whether a specific on-set incident caused the final scene to be
> changed. The incident is something the user heard about, not an established
> fact. Compare first-hand accounts if they exist.

**Expected behavior:**

- Form a conditional query such as a search for accounts discussing whether the
  reported incident and scene change are connected.
- Do not query or report “the incident that caused the scene change” as a fact.
- Preserve any candidates as attributed reports or discovery leads.
- Identify the incident's existence, participants, date, and causal link as
  verification needs.

### 20.3 Empty retrieval result

**Result:** `search_web` succeeds with zero candidates.

**Expected output:**

> No usable candidate sources were returned for the focused query. This is a
> retrieval limitation, not evidence that no sources exist. No
> source-dependent observation is made. A follow-up may refine the query within
> the remaining search budget, but the agent will not invent a source.

### 20.4 Provider failure

**Result:** `search_web` returns a timeout or provider error.

**Expected output:**

> Source retrieval failed for this query with a provider timeout. No candidate
> source is available from this call, and no factual conclusion is drawn. The
> failure is recorded under Evidence limitations; the agent may make one
> bounded, faithful refinement only if one budget call remains.

### 20.5 Search budget exhausted

**Result:** Two retrieval calls have been attempted, with incomplete or
conflicting candidate material.

**Expected output:**

> The two-call retrieval budget is exhausted. The candidate list and
> preliminary observations are limited to these queries and remain unverified.
> Conflicting accounts and missing source passages are recorded as verification
> needs. No additional search or fabricated fallback evidence is produced.

## 21. Explicit Design Decisions

- The initial agent handles one focused thread per invocation and does not
  provide multi-turn continuity.
- The application-level retrieval budget is two `search_web` calls per
  invocation, including failed and empty calls.
- `search_web` is the only web-retrieval boundary. Tavily credentials and SDK
  details remain exclusively in the source-retrieval layer.
- Source prioritization may use thread relevance and apparent first-hand source
  type, but never reliability, truthfulness, or evidentiary-strength scoring.
- Preliminary output must preserve exact URLs and require URL traceability for
  every source-dependent observation.
- Empty results and retrieval errors are explicit limitations, never successful
  fabricated fallbacks.
- No unresolved design questions remain for the initial Issue #9 scope. Future
  work may revisit multi-turn state, verification, and dossier synthesis as
  separate specifications.
