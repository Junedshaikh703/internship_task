from project.graph.state import GraphState


def safe_failure_node(state: GraphState) -> GraphState:
    """
    Return a safe response when the system cannot produce
    a verified answer after one retry.
    """

    return {
        **state,
        "answer": (
            "I'm sorry, but I couldn't generate a verified answer based on the available documentation. "
            "Please contact OrbitDesk Support or provide additional details so I can assist further."
        ),
        "verification_passed": False,
        "confidence": 0.0,
        "requires_human": True,
        "reason": "The answer could not be verified after one revision attempt.",
    }