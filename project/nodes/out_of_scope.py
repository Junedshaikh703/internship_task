from project.graph.state import GraphState


def out_of_scope_node(state: GraphState) -> GraphState:
    """
    Handle questions outside the OrbitDesk knowledge base.
    """

    return {
        **state,
        "answer": (
            "I'm only able to answer questions related to OrbitDesk. "
            "Please ask a question about the OrbitDesk product or its documentation."
        ),
        "sources": [],
        "verification_passed": True,
        "confidence": 1.0,
        "requires_human": False,
        "reason": "The query is outside the supported knowledge base.",
    }