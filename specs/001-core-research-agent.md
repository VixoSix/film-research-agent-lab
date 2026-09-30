# Core Research Agent Specification

## 1. Problem Statement

Film research often requires information that is scattered across interviews, books, trade publications, archival material, specialist journalism, festival records, and other sources. Basic film metadata is comparatively easy to find, but deeper questions require discovering relevant sources, comparing accounts, tracing claims back to evidence, and communicating uncertainty.

Without a disciplined research process, a researcher may receive an apparently confident summary that contains invented details, unsupported quotations, conflated people or events, or a single version of a disputed story presented as fact. The system must therefore support evidence-based research rather than produce plausible-sounding film trivia or unverified opinion.

## 2. Goal

The goal is to define a research assistant that helps users discover, retrieve, verify, organize, and synthesize deeper film research into a clearly sourced dossier.

The system should support research into topics including:

- interviews with directors, actors, writers, cinematographers, composers, editors, designers, producers, and other crew members;
- first-hand accounts and production anecdotes;
- creative decisions and changes made during development or production;
- production problems, disputes, and controversies;
- filming locations and location-specific production information;
- deleted, altered, censored, or otherwise changed material;
- critical reception and changes in critical interpretation;
- conflicting accounts of people, events, decisions, or timelines; and
- specialized film sources that are unlikely to appear in basic metadata databases.

The system supports the user's research and organization. It does not replace the user's personal interpretation of a film or write opinions on the user's behalf.

## 3. Scope

This specification covers the behavior and quality of a core research agent that:

1. accepts a focused or exploratory film-research request;
2. identifies research subquestions and useful search directions;
3. retrieves relevant sources and records source metadata;
4. extracts claims, quotations, people, dates, events, and relationships from retrieved material;
5. classifies source strength and reliability;
6. links claims to the evidence that supports them;
7. identifies agreement, disagreement, ambiguity, and gaps;
8. produces a structured research dossier; and
9. communicates when evidence is insufficient or unavailable.

The system may organize retrieved information into a research trail so that a user can inspect how a conclusion was formed. The specification does not prescribe a particular interface, retrieval technology, agent architecture, storage system, or model.

## 4. Non-Goals

The system is not intended to:

- replace film databases that provide routine metadata such as cast lists, release years, runtimes, or genres;
- generate unsourced film trivia or fill gaps with likely-sounding details;
- invent, reconstruct, or paraphrase an interview that was not retrieved;
- present generated prose as evidence;
- decide which disputed account is true without explaining the evidentiary basis;
- write a user's personal review, interpretation, ranking, or aesthetic judgment;
- provide legal, historical, journalistic, or academic certification of a claim;
- guarantee that a source is truthful merely because it is categorized as strong; or
- implement a specific provider, model, programming language, dependency, or deployment method.

## 5. Research Request Input

A research request should allow the user to provide, at minimum:

- the film or films under investigation;
- the central research question or topic;
- the desired scope, such as a production period, person, controversy, location, or reception period;
- optional people, events, sources, keywords, or languages to prioritize; and
- optional output preferences, such as concise findings, a chronological dossier, a source comparison, or an evidence table.

The system should clarify ambiguity when the film title, person, event, or requested period could refer to more than one subject. If clarification is not possible, the dossier must state the interpretation used and any resulting limitation.

Requests may be broad, but the system should decompose them into explicit research questions or investigative threads. It should preserve the user's original question and distinguish user-provided assumptions from retrieved evidence.

## 6. Expected Research Dossier Output

Each completed research dossier should contain, where applicable:

1. **Research question and scope** — the request as understood, including assumptions and boundaries.
2. **Executive summary** — a concise synthesis that distinguishes established findings, reported claims, disputed points, and unknowns.
3. **Research threads** — the subquestions investigated and their status.
4. **Key findings** — claims written in appropriately qualified language.
5. **Evidence for each claim** — citations or source references tied to the specific claim, quotation, date, person, or event.
6. **Direct quotations** — only when present in a retrieved source, clearly attributed and kept faithful to that source.
7. **Timeline or event sequence** — when dates or chronology are relevant, with uncertainty marked.
8. **People and roles** — identities and roles as supported by sources, without conflating similarly named people.
9. **Conflicting accounts** — competing versions, the sources supporting each, and the reason the disagreement remains unresolved or is weighted one way.
10. **Source register** — title, author or speaker, publication or host, date when available, URL or other locator, source category, and relevant access limitations.
11. **Evidence gaps and limitations** — missing sources, inaccessible material, ambiguous attribution, unresolved claims, and topics not adequately researched.
12. **User interpretation boundary** — a clear indication that conclusions about meaning, artistic value, or personal response remain the user's responsibility.

The dossier must not imply that an item is verified merely because it appears in a summary. Verification status and source support must remain visible at the claim level.

## 7. Source Hierarchy

When sources are available, the system should prefer the following hierarchy, while recognizing that relevance and directness still matter:

1. **Primary sources** — direct interviews, first-hand accounts, production documents, official transcripts, recordings, contemporaneous statements, archival material, and direct testimony from a participant.
2. **Strong secondary sources** — careful reporting, specialist books, scholarly work, established trade journalism, or well-documented criticism that identifies and contextualizes its evidence.
3. **Secondary sources** — reputable summaries, reviews, databases, or articles that report information without fully exposing the underlying evidence.
4. **Weak sources** — unattributed summaries, low-context listicles, reposts, user-generated pages, snippets, or sources with unclear editorial standards.
5. **Unknown sources** — material whose authorship, provenance, date, editorial process, or relationship to the claim cannot be established.

The hierarchy is a guide to evidentiary weight, not a guarantee of accuracy. A primary source may be partial, self-interested, mistaken, retrospective, or contradicted by other evidence. The dossier should record those limitations.

## 8. Source Reliability Categories

Every source used to support a material claim must be assigned one of these categories:

- **Primary:** The source is direct evidence from a participant, contemporaneous record, original document, or direct recording relevant to the claim.
- **Strong secondary:** The source is independently produced, identifiable, relevant, and demonstrates substantial editorial, scholarly, or evidentiary rigor.
- **Secondary:** The source is identifiable and plausibly relevant but provides limited evidence, context, or traceability.
- **Weak:** The source has limited provenance, weak editorial controls, unclear attribution, or a high risk of repeating unsupported claims.
- **Unknown:** The source's provenance or reliability cannot be established sufficiently for a stronger category.

The system should record why a source received its category when that classification materially affects the synthesis. Source category must not be silently upgraded because multiple weak sources repeat the same claim; repetition is not independent corroboration unless the sources can be shown to rely on independent evidence.

## 9. Grounding Rules

The following rules are mandatory:

- Never invent interviews, quotes, people, dates, incidents, claims, or sources.
- Every interview-derived claim must reference the retrieved interview or a clearly identified source that faithfully reports it.
- Every material factual claim in the dossier must be traceable to one or more retrieved sources.
- Direct quotations must be reproduced only from retrieved material, with the speaker, source, and location identified when available.
- The system must distinguish a source's wording from the system's summary or inference.
- Inferences must be labeled as inferences and must identify the evidence from which they follow.
- The system must not present search snippets, generated text, or inaccessible references as if they were inspected evidence.
- A source that is mentioned but not retrieved must be marked as unverified and must not be used as sole support for a factual conclusion.
- The system must preserve meaningful qualifiers such as “according to,” “reportedly,” “in a later recollection,” or “the available source states.”
- The system must not convert the user's premise into a confirmed fact without evidence.
- Personal interpretation of the film remains the user's responsibility; the system should support research, verification, and organization rather than write opinions on behalf of the user.

## 10. Handling Conflicting Sources

When credible sources disagree, the system must present the disagreement rather than silently selecting one version.

For each material conflict, the dossier should:

1. state the disputed claim or question;
2. summarize each materially different account;
3. identify the source, speaker, date, and reliability category for each account;
4. note whether the accounts are independent, retrospective, direct, or second-hand;
5. explain any reason to give one account more weight, such as direct knowledge, contemporaneity, corroboration, specificity, or documented correction; and
6. state whether the conflict can be resolved, remains open, or reflects different interpretations of the event.

If one account is weighted more strongly, the dossier must state the justification and must not describe the lower-weight account as disproven unless the evidence supports that conclusion. If the evidence does not justify a preference, the output must say that the matter remains disputed.

## 11. Handling Insufficient Evidence

The system must clearly report insufficient evidence when it cannot support a reliable answer. This includes cases where:

- no relevant source was retrieved;
- available sources are too weak, indirect, inaccessible, or ambiguous;
- a quotation, date, person, or incident cannot be verified;
- sources refer to the subject inconsistently;
- the evidence supports only part of the user's question; or
- the available sources conflict without a defensible basis for resolution.

An insufficient-evidence result should identify what was checked, what remains unverified, why the evidence is inadequate, and what kind of source or follow-up research could help. It must not fill the gap with a guess, a generalized statement presented as a specific fact, or an invented citation.

## 12. Functional Requirements

### Request and Research Planning

- The system shall accept a film-research request and preserve its original wording.
- The system shall identify ambiguity in the film, person, event, time period, or terminology.
- The system shall decompose broad requests into explicit research threads.
- The system shall prioritize the user's requested topic over routine metadata.

### Retrieval and Source Records

- The system shall retrieve or otherwise inspect sources before making source-dependent claims.
- The system shall record enough metadata to identify each source and locate the relevant passage or section when available.
- The system shall distinguish retrieved sources from merely discovered or referenced sources.
- The system shall support specialized film sources and first-hand material when available.

### Evidence and Claim Management

- The system shall represent material claims with links to their supporting evidence.
- The system shall distinguish direct quotations, source summaries, system inferences, and user-provided assertions.
- The system shall assign a source reliability category to each used source.
- The system shall identify unsupported, partially supported, disputed, and unresolved claims.
- The system shall not treat repeated wording across dependent sources as independent corroboration.

### Synthesis and Reporting

- The system shall produce a structured dossier containing findings, evidence, source register, conflicts, and limitations.
- The system shall use qualified language appropriate to the strength and directness of the evidence.
- The system shall present conflicting credible accounts rather than conceal them.
- The system shall state clearly when the available evidence is insufficient.
- The system shall keep factual research separate from the user's personal interpretation.

### Traceability and Review

- A user shall be able to trace each material claim to the source or sources supporting it.
- A user shall be able to distinguish primary, strong secondary, secondary, weak, and unknown sources.
- A user shall be able to inspect why an account was preferred, qualified, or left unresolved.
- The system shall preserve enough research context for a user to repeat or extend the investigation.

## 13. Quality Requirements

- **Accuracy:** The dossier must not contain fabricated sources, quotations, people, dates, incidents, or claims.
- **Groundedness:** Material factual statements must be supported by retrieved evidence or explicitly marked as unverified.
- **Traceability:** Claims, quotations, conflicts, and conclusions must link back to identifiable sources.
- **Source transparency:** Reliability categories and important source limitations must be visible.
- **Conflict transparency:** Disagreement must be represented fairly and not hidden through unqualified synthesis.
- **Uncertainty transparency:** Missing, ambiguous, inaccessible, and insufficient evidence must be stated plainly.
- **Relevance:** Research effort and output should focus on the user's deeper question rather than unnecessary metadata.
- **Attribution fidelity:** The system must preserve who said or reported what and must not merge separate accounts.
- **Reproducibility:** Another researcher should be able to understand the research path and locate the cited material when access permits.
- **Interpretive neutrality:** The system should organize evidence without asserting the user's personal artistic or critical judgment.
- **Clarity:** The dossier should be readable by a film researcher and should separate evidence, synthesis, uncertainty, and interpretation.

## 14. Acceptance Criteria

The core research agent is acceptable when all of the following are true:

1. A focused request about a film's production history produces a dossier organized around the requested research question rather than only routine metadata.
2. Every material interview-derived claim in the dossier points to a retrieved interview or an explicitly identified, faithful report of that interview.
3. The dossier identifies sources as primary, strong secondary, secondary, weak, or unknown and does not collapse these categories into a single undifferentiated citation list.
4. A direct quotation is included only when its wording can be traced to retrieved source material, with attribution and location when available.
5. When two credible sources disagree, the dossier presents both accounts, identifies their evidentiary differences, and states whether the disagreement is resolved or remains open.
6. When evidence is insufficient, the dossier says so explicitly, identifies the gap, and does not supply a guessed answer or fabricated source.
7. The dossier distinguishes sourced findings from system inference and from the user's own premise.
8. The output includes a source register and enough traceability for a user to inspect the evidence behind material claims.
9. The output separates evidence-based research from personal interpretation and does not write a review or opinion on behalf of the user.
10. The specification can be implemented without assuming a particular AI model, provider, retrieval system, API, programming language, or dependency.

## 15. Example Successful Research Case

### Request

“Research how the production of *Example Film* changed its central visual approach, including the cinematographer's account, any director interviews, production constraints, and later critical discussion. Identify where sources disagree.”

### Expected Result

The dossier should:

- define the visual-approach question and identify the relevant production period;
- locate and cite a retrieved interview with the cinematographer, if available;
- locate and cite relevant director or other crew interviews, if available;
- distinguish first-hand accounts from later reporting and criticism;
- connect each claim about a creative decision or production constraint to a source passage;
- identify whether an account is contemporaneous or retrospective;
- compare any disagreement about why the visual approach changed;
- explain why one account may carry more or less weight, without treating authority alone as proof;
- summarize later critical discussion as critical reception rather than as evidence of the creators' intent; and
- list unresolved questions and make clear that the user's interpretation of the film remains separate from the dossier.

The successful result is not defined by finding a dramatic production story. It is defined by producing a useful, traceable, and appropriately qualified account of what the available evidence supports.

## 16. Example Failure / Insufficient Evidence Case

### Request

“Find the interview where the director said the final scene was changed after a specific incident on set, and explain exactly what happened.”

### Expected Result

If the interview cannot be retrieved, the available sources do not identify the director's statement, or the sources provide only an unattributed repetition, the system must not invent the interview, quote, incident, date, or explanation.

The dossier should instead state that the claim could not be verified, identify the sources that were found and their reliability categories, distinguish any related but different evidence, and explain what would be needed to verify the story. If one source reports the incident but no primary or strong secondary evidence is available, the dossier may describe it as an attributed report, clearly mark it as unverified or weakly supported, and avoid presenting it as established fact.

The system has failed if it fabricates a plausible interview, assigns a quotation to the director without retrieved evidence, merges separate production anecdotes, or presents the requested story as true merely because it appears in search results or is repeated by weak sources.
