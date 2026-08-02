from langchain_core.messages import HumanMessage, SystemMessage

from project.graph.state import GraphState
from project.models.llm import chat_model
from project.prompts.triage import SYSTEM_PROMPT


def triage_node(state: GraphState) -> GraphState:
    """
    Classify the incoming user query.
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=state["query"]),
    ]

    response = chat_model.invoke(messages)

    classification = response.content.strip().lower()

    valid_labels = {
        "answerable",
        "requires_clarification",
        "requires_escalation",
        "out_of_scope",
    }

    if classification not in valid_labels:
        classification = "requires_clarification"

    return {
        **state,
        "classification": classification,
    }