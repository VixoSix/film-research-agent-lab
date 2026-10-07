# Provider-Neutral Research Foundation — Requirements

## Objective and scope

Make the existing film-research prototype configurable and replaceable without
changing its research responsibilities or evidence rules. This is a planned
evolution, not deployed functionality. Stable IDs belong to this spec; packets
cite this path and the applicable IDs. The longer-term aim is to reconstruct
the history around a film through interviews, testimony, production records,
specialist press and other traceable sources, not merely film metadata.

## Requirements

| ID | Observable requirement | Acceptance evidence |
| --- | --- | --- |
| PNRF-REQ-001 | Preserve the two existing agent responsibilities, identities, prompts, tools/callbacks and public ADK entry points. | Existing grounding/output tests pass; factory/import tests show planner has no tools and researcher retains only bounded search. |
| PNRF-REQ-002 | Represent role, provider, model ID and optional model family separately. Family is descriptive and never selects transport. | Two role bindings can differ; tests changing family alone leave routing unchanged; no provider/model names become agent identities. |
| PNRF-REQ-003 | Provide explicit local configuration and deterministic programmatic injection, with documented precedence and safe invalid-configuration failures. Credentials remain outside configuration. | Default, file, environment-path, injected settings, malformed/unknown fields, blank values and missing files are tested without APIs. |
| PNRF-REQ-004 | Centralize model construction/runtime details outside agents. Keep Google ADK and LiteLLM, with Groq as the sole implemented model provider. | Default still selects `groq/openai/gpt-oss-120b` with `include_reasoning=False`; agents contain no LiteLLM construction or Groq credential access; a fake ADK model can replace it. |
| PNRF-REQ-005 | Model execution failures cross the project boundary as safe project errors, preserving machine-readable categories without provider payloads or credentials. | Offline async tests cover missing key, timeout, authentication, rate limit, other failure, partial-stream failure and cancellation. |
| PNRF-REQ-006 | Consumers access normalized search capability without depending on a provider SDK or raw response shape. Preserve the public retrieval facade and injectable legacy client path. | Fake normalized search works through the facade; legacy `client=` tests retain behavior; incompatible injection is rejected before a provider call. |
| PNRF-REQ-007 | Keep Tavily as the sole real search implementation, with the existing request mapping and normalization semantics. | Fake SDK tests prove `standard/basic`, `deep/advanced`, `include_answer=False`, defaults/ranges, exact URLs/order/deduplication, optional fields, warnings and trace metadata. |
| PNRF-REQ-008 | Preserve explicit retrieval errors and safe model-facing outcomes, including failures during SDK client creation. | Invalid input precedes credentials/provider work; missing key, timeout, provider failure and malformed envelope stay distinguishable; no failure becomes empty success or fabricated material. |
| PNRF-REQ-009 | Preserve the invocation budget: two attempts, three results requested per tool call, failed/empty calls consumed, third call blocked and concurrency bounded. | Existing budget/reset/race tests pass unchanged in meaning, including failure paths through the new adapter. |
| PNRF-REQ-010 | Preserve candidate/discovery provenance and grounding limits. Search result is not verified evidence; snippet is not inspected source; relevance is not reliability. | Existing prompts remain identical and grounding tests pass; tool payload round-trip retains URLs, metadata, warnings and query. No reliability scores/classifier are added. |
| PNRF-REQ-011 | Enforce selected dependency rules in small deterministic tests. Automated verification requires no live model/search service or credential. | AST tests reject prohibited imports/hardcodes, tested with violating samples; an offline composed fake run proves injection and payload/budget behavior. |
| PNRF-REQ-012 | Allow configuration-based model comparison and later adapter additions without changing agent responsibilities/prompts or source-candidate contracts. | Tests construct two agents with independent model settings/fakes; README names the extension seams and limits; no future providers or evaluation engine are implemented. |
| PNRF-REQ-013 | Migrate in independently verifiable increments using existing dependencies; every packet leaves imports valid and the verification gate green. | Each packet records baseline/final gate, scoped diff and acceptance; DAG and integration prerequisites are explicit. No dependency changes or framework rewrite. |
| PNRF-REQ-014 | Document operation, configuration, error boundaries, compatibility and a free-first policy without implicit provider fallback or paid service selection. | README includes exact defaults, restart/injection semantics, keys, sample profile, unsupported-provider behavior and manual-only live evaluation; no billing, hidden fallback or retries are added. |

## Exclusions

No new providers, agents, RAG, embeddings, document reader, chunking, reranking,
vector store, YouTube/transcription, final dossier, frontend/API, containers,
deployment, multiagent autonomy, billing, plugin registry or global mutation
testing. Future additions require separate specs and packets. None receives a
Task Packet here. Software checks protect mechanics and prompt preservation;
they do not prove that every model produces grounded prose.
