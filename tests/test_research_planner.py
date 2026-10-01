from google.adk.models.lite_llm import LiteLlm

from app.research_planner.agent import root_agent


def test_root_agent_configuration() -> None:
    assert root_agent.name == "research_planner"
    assert isinstance(root_agent.model, LiteLlm)
    assert root_agent.model.model == "groq/openai/gpt-oss-120b"
    assert root_agent.model._additional_args["include_reasoning"] is False
    assert not root_agent.tools
    assert "structured investigation plan" in root_agent.description.lower()


def test_root_agent_instruction_has_grounding_boundaries() -> None:
    instruction = root_agent.instruction.lower()

    for phrase in (
        "do not search",
        "do not retrieve",
        "do not verify",
        "never invent",
        "user-provided",
        "not established fact",
        "source has been found",
    ):
        assert phrase in instruction


def test_root_agent_instruction_has_output_contract() -> None:
    instruction = " ".join(root_agent.instruction.lower().split())

    for concept in (
        "original request",
        "working scope",
        "user-provided statements",
        "clarifications and assumptions",
        "prioritized research threads",
        "search directions",
        "expected evidence needs",
        "grounding limits",
        "open questions and stopping conditions",
        "title/category",
        "focused research question",
        "why it matters",
        "preferred source types",
        "comparison or verification needs",
        "priority and rationale",
        "dependencies",
    ):
        assert concept in instruction


def test_root_agent_instruction_limits_unsupported_specificity() -> None:
    instruction = " ".join(root_agent.instruction.lower().split())

    for concept in (
        "conditional investigative language",
        "do not invent specific incidents, interviews, quotations, documents, budgets, dates, or allegations",
        "distinguish user-provided information from possible research directions",
        "do not name specific sources or archives",
        "accessible interviews, public documents, and published first-hand accounts",
        "do not suggest obtaining private medical records",
        "avoid excessive or arbitrary research threads",
        "insufficient evidence",
        "do not introduce specific people, film dates, production events, interview titles, publications, or archives",
        "refer to unidentified people by role",
        "suggest source categories rather than supposedly existing sources",
        "never state that interviews or evidence exist or are likely to be available without retrieval",
        "preserve the original research request separately from later planning instructions",
        "do not estimate the probability that a claim will remain unverified",
        "evidence needed and the limitations that could prevent verification",
        "before producing the final plan",
        "replace any unsupported specificity with a generic role, category, or conditional research question",
    ):
        assert concept in instruction
