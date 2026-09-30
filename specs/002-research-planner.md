# Research Planner Specification

## 1. Purpose

The Research Planner is the first AI agent in the film research workflow. It transforms a user's film research request into a structured investigation plan that later research agents can use to discover, retrieve, compare, and verify evidence.

The planner is intended for deeper film research, especially questions involving creative decisions, production history, first-hand accounts, controversies, changes over time, and conflicting interpretations. It should focus the investigation on useful questions rather than routine film metadata.

The planner preserves the user's original request, separates user-provided statements from questions that require investigation, identifies ambiguity, and makes the intended research scope explicit.

## 2. Responsibilities

The Research Planner shall:

- preserve the user's original wording and stated scope;
- identify the film, people, events, periods, locations, and concepts mentioned in the request;
- distinguish user-provided facts, assumptions, hypotheses, and desired outcomes from matters that still need research;
- identify ambiguity in film titles, people, events, terminology, dates, and requested periods;
- decompose broad requests into focused research questions and useful research threads;
- prioritize threads according to the user's question, likely evidentiary value, and relevance to deeper film research;
- prioritize interviews, direct testimony, production documents, and other first-hand accounts when they are relevant to a question;
- identify likely source types and search directions without claiming that any source has been found;
- identify where competing accounts, chronology, attribution, or source independence will need comparison;
- state clarification questions or assumptions required to make the investigation meaningful; and
- produce a plan that later research, retrieval, evidence, and synthesis agents can execute and evaluate.

## 3. Non-Responsibilities

The Research Planner shall not:

- perform web searches or retrieve source material;
- call TMDB or any other film metadata provider;
- inspect, quote, summarize, or verify a source;
- confirm that a person, event, interview, incident, date, or claim exists;
- invent interviews, quotations, sources, incidents, people, dates, or facts;
- use search snippets, model memory, or general plausibility as evidence;
- perform retrieval-augmented generation or access a research corpus;
- resolve a dispute between accounts;
- produce a final research dossier, factual synthesis, review, or personal interpretation of a film; or
- convert a user's premise into an established fact.

The planner may state that a later agent should investigate a claim or seek a particular kind of source. That statement is a planning instruction, not evidence that the claim or source is real.

## 4. Input

The planner accepts a film research request containing, where available:

- the user's original request in natural language;
- one or more film titles or identifiers;
- a central question, topic, or hypothesis;
- a requested scope, such as a production period, person, controversy, location, or reception period;
- named people, events, sources, keywords, or languages to prioritize;
- desired output preferences, such as a chronology, source comparison, or evidence table; and
- any context the user explicitly supplies, including assumptions or claims they want investigated.

The planner should not require routine metadata unless it is necessary to disambiguate the investigation. If a title, person, event, or period is ambiguous, the input should be represented as ambiguous rather than silently resolved.

## 5. Expected Output

The planner produces a structured investigation plan with these fields:

1. **Original request** — the user's request preserved verbatim or faithfully preserved.
2. **Working scope** — the film or films, central topic, time boundaries, people, events, and output preferences identified from the request.
3. **User-provided statements** — premises, assumptions, hypotheses, or facts supplied by the user, each marked as user-provided and not independently established.
4. **Clarifications and assumptions** — ambiguities requiring user clarification and, only when necessary, explicit provisional assumptions for later agents.
5. **Research threads** — an ordered set of focused threads. Each thread includes:
   - a short title and category;
   - a focused research question;
   - why the question matters to the user's request;
   - entities, periods, or terms to investigate;
   - preferred source types, with first-hand sources prioritized when relevant;
   - likely comparison or verification needs; and
   - dependencies on other threads, if any.
6. **Priority and rationale** — high, medium, or low priority for each thread, with a concise reason.
7. **Search directions** — concepts, names, phrases, archives, publications, languages, or source classes for later agents to investigate. These are directions, not search results.
8. **Expected evidence needs** — the claims, quotations, dates, relationships, chronology, or disagreements that later agents should trace to retrieved sources.
9. **Grounding limits** — an explicit statement that no source has been found, inspected, or verified by the planner.
10. **Open questions and stopping conditions** — unresolved ambiguity, evidence gaps to watch for, and conditions under which later agents should report insufficient evidence rather than guess.

The plan should be concise enough to guide execution while detailed enough that later agents can distinguish the user's premise, the question to investigate, and the evidence they must obtain.

## 6. Research Thread Categories

The planner may use one or more of the following categories. It should create only threads relevant to the request.

- **Creative decisions** — changes in story, visual approach, performance, editing, sound, design, or other artistic choices.
- **Development and production history** — development stages, rewrites, financing, casting, scheduling, production constraints, or changes during filming.
- **First-hand accounts and interviews** — statements by directors, actors, writers, cinematographers, editors, producers, designers, composers, or other participants.
- **Production anecdotes and incidents** — reported events on set or during development, including claims that require careful attribution and verification.
- **People, roles, and relationships** — identity, role, participation, collaboration, or possible conflation of similarly named people.
- **Locations and material conditions** — filming locations, location-specific decisions, logistical conditions, or environmental constraints.
- **Deleted, altered, or censored material** — scenes, endings, cuts, changes, censorship, or alternate versions.
- **Disputes and controversies** — competing accounts, conflicts, allegations, responses, and unresolved issues.
- **Chronology and change over time** — sequences of decisions or events, including retrospective versus contemporaneous accounts.
- **Critical reception and interpretation** — contemporary and later criticism, changing critical views, and distinctions between reception and creator intent.
- **Institutional, industrial, or historical context** — studios, distributors, festivals, labor, regulation, technology, or period conditions relevant to the question.
- **Source and evidence mapping** — what kinds of sources are needed to support particular claims, quotations, dates, or comparisons.

Routine metadata such as cast lists, release years, runtimes, or genres should not become a research thread unless it is directly relevant to the user's deeper question or needed to resolve ambiguity.

## 7. Planning Rules

1. Start from the user's central question and requested scope. Do not substitute a generic film profile.
2. Prefer a small number of focused, actionable threads over a long list of loosely related topics.
3. Decompose broad requests into questions that can be researched independently and later synthesized.
4. For claims about intent, decisions, experiences, or events, prioritize direct interviews, first-hand accounts, production documents, contemporaneous records, and other primary material when relevant.
5. Treat interviews as targets for investigation, not as evidence already in hand. Specify whose account would be useful and what question it should address.
6. Distinguish what the user stated from what a later agent must establish. Preserve the user's premise without endorsing it.
7. Mark whether a thread seeks a fact, a quotation, a chronology, a comparison of accounts, a source trail, or an interpretation of reception.
8. Identify dependencies when one thread must establish identity, chronology, or terminology before another can be evaluated.
9. Include a comparison or corroboration need whenever the request involves controversy, disputed memory, attribution, retrospective claims, or a dramatic production story.
10. Include a reception thread only when the user asks about criticism, interpretation, influence, or changing views. Do not use criticism as automatic evidence of creator intent.
11. Use conditional language for unestablished premises: “investigate whether,” “look for evidence of,” or “compare accounts of.”
12. Do not add unsupported specificity merely to make a plan appear complete.
13. Make later failure visible. If a thread may end with insufficient evidence, state what would count as an adequate source and what must remain unresolved otherwise.
14. Keep the plan provider-, model-, retrieval-, and implementation-independent, consistent with the core research agent specification and the project's implementation-agnostic foundation.

## 8. Grounding Boundaries

The plan is a map for investigation, not a research result.

The planner may rely on the user's request to identify subjects, questions, and stated premises. It may use general planning knowledge to suggest relevant source categories and search directions. It must not present remembered or inferred film information as a discovered fact.

Every item that depends on external evidence must be phrased as a research target. For example, the plan may say “look for a retrieved interview in which the cinematographer discusses the visual change,” but it must not say that such an interview exists or that the cinematographer made the change.

The output must explicitly state that the planner did not search, retrieve, inspect, or verify sources. Later agents must establish material claims from retrieved evidence, preserve attribution and qualifiers, and report insufficient evidence when the plan cannot be completed reliably.

## 9. Example Input

> Research how the production of *Example Film* changed its central visual approach. I want the cinematographer's account, relevant director interviews, production constraints, and later critical discussion. Identify where sources disagree. I have heard that a specific incident on set caused the final visual change, but I am not sure whether that is documented.

## 10. Example Expected Plan

### Original request

Investigate the change in *Example Film*'s central visual approach, including the cinematographer's account, director interviews, production constraints, later critical discussion, and disagreements between sources.

### User-provided statements

- The user wants to investigate a change in the film's visual approach.
- The user has heard that a specific on-set incident caused the final change.
- The alleged incident is a user-provided premise and is not established by the plan.

### Clarifications and assumptions

- Clarify which film titled *Example Film* is intended if the title is not unique.
- Clarify the relevant production or release period if multiple versions or adaptations exist.
- Until clarified, treat the alleged on-set incident as an unverified hypothesis, not as an event.

### Prioritized research threads

1. **Creative decision: identify the visual change — High**
   - Question: What visual approach was initially intended, what approach appeared in the completed film, and when did the change occur?
   - Source needs: production documents, contemporaneous records, and first-hand accounts from relevant crew.
   - Evidence needs: dates, decision points, named participants, and direct support for each version.

2. **First-hand account: cinematographer — High**
   - Question: What does the cinematographer say about the visual approach, its development, and any changes during production?
   - Source needs: retrieved interviews, talks, commentaries, production notes, or other direct testimony.
   - Comparison need: distinguish contemporaneous statements from later recollections and compare them with other accounts.

3. **First-hand account: director and crew — High**
   - Question: What do the director and other relevant participants say about the visual decision and its causes?
   - Source needs: retrieved interviews and direct statements, prioritized by relevance and proximity to the decision.
   - Comparison need: preserve who said what and identify agreement, contradiction, or independent corroboration.

4. **Production constraints — Medium**
   - Question: Did schedule, budget, location, equipment, personnel, studio, or other production conditions affect the visual approach?
   - Source needs: first-hand accounts, production records, trade reporting, and specialist books or criticism where relevant.
   - Evidence needs: separate documented constraints from later explanations or speculation.

5. **Alleged on-set incident — High**
   - Question: Is there retrieved evidence for the alleged incident, its date, participants, and causal relationship to the visual change?
   - Source needs: a direct account or an identifiable, well-supported report; repeated unattributed versions are not independent corroboration.
   - Stopping condition: if the incident or causal link cannot be supported, report it as unverified rather than narrating it as fact.

6. **Reception and later interpretation — Medium**
   - Question: How did contemporary and later critics describe the film's visual approach and its change, and how did those views evolve?
   - Source needs: identifiable criticism and specialist writing.
   - Boundary: treat this as evidence of reception and interpretation, not automatic evidence of creator intent or production causation.

7. **Conflict and chronology mapping — High**
   - Question: Where do retrieved accounts differ about the timing, cause, or significance of the visual change?
   - Source needs: all relevant retrieved accounts with speaker, date, provenance, and source category.
   - Expected output: a comparison showing whether disagreement is resolved, weighted with justification, or left open.

### Grounding statement

No interview, source, incident, quotation, or claim has been found or verified by this plan. The listed source types and search directions are targets for later agents. Any final claim must be tied to retrieved evidence, with uncertainty and disagreement preserved.

## 11. Failure and Ambiguity Handling

The planner shall produce a usable partial plan rather than invent missing details.

- **Ambiguous film:** identify the ambiguity, list the identifying information needed, and avoid assigning a year, director, country, or version without user support.
- **Ambiguous person:** identify possible role or identity ambiguity and require later agents to confirm the person's identity before attributing a statement.
- **Ambiguous period or version:** state the competing interpretations and create a clarification requirement or explicitly labeled provisional scope.
- **Unclear terminology:** preserve the user's wording, identify the term that needs definition, and suggest the distinction later research should test.
- **Broad request:** split it into focused threads, rank them, and state which threads are essential versus optional.
- **Premise presented as fact:** record it as user-provided and create a conditional investigation thread.
- **Requested interview or quote:** turn it into a source-retrieval target and verification requirement; never imply that it was found.
- **Potentially disputed story:** create threads for the claim, first-hand accounts, corroboration, chronology, and competing explanations as appropriate.
- **Insufficient planning context:** state what cannot be scoped and ask for the minimum clarification needed. Do not compensate with guessed metadata.

If clarification is unavailable, the plan must state the interpretation used, the limitation it creates, and which later conclusions must remain conditional.

## 12. Acceptance Criteria

The Research Planner specification is satisfied when an implementation can:

1. Preserve the user's original film research request and identify its central question.
2. Focus a plan on deeper research rather than routine metadata unless metadata is relevant to the investigation.
3. Decompose a broad request into focused, prioritized research threads.
4. Include useful thread categories and identify appropriate source types for each thread.
5. Prioritize interviews and first-hand accounts when the question concerns participant experience, intent, decisions, or production events.
6. Distinguish user-provided statements and assumptions from claims that later agents must research.
7. Identify ambiguous films, people, events, terminology, and periods, and state the required clarification or explicit provisional assumption.
8. Describe search directions and evidence needs without implying that a source was found, inspected, or verified.
9. Never invent or assert interviews, quotations, sources, incidents, people, dates, or facts.
10. Mark disputed or causally loaded premises as questions to investigate and include comparison or corroboration needs where appropriate.
11. Define stopping conditions that cause later agents to report insufficient evidence rather than guess.
12. Produce a plan that later retrieval, evidence, verification, and synthesis agents can execute without needing to infer the planner's hidden assumptions.
13. Keep the planner separate from web search, source retrieval, TMDB, claim verification, RAG, and final dossier production.
14. Remain consistent with the core research agent's requirements for traceability, source transparency, uncertainty, conflict handling, and separation of user interpretation from evidence-based research.
15. Avoid assumptions about a particular AI model, provider, retrieval technology, API, programming language, dependency, or deployment method.
