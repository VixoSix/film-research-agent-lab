from app.research_planner.agent import root_agent


def test_root_agent_configuration() -> None:
    assert root_agent.name == "research_planner"
    assert root_agent.model == "gemini-3.8-flash"
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
