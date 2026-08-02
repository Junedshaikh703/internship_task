from project.graph.state import GraphState


def clarification_node(state: GraphState) -> GraphState:
    """
    Ask the user for more information before continuing.
    """

    return {
        **state,
        "answer": (
            "I need a little more information to answer your question. "
            "Could you provide additional details or describe the issue more specifically?"
        ),
        "sources": [],
        "verification_passed": True,
        "confidence": 1.0,
        "requires_human": False,
        "reason": "The query requires additional clarification.",
    }