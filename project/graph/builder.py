from langgraph.graph import START, END, StateGraph

from project.graph.state import GraphState


from project.nodes.triage import triage_node
from project.nodes.clarification import clarification_node
from project.nodes.out_of_scope import out_of_scope_node
from project.nodes.retrieval import retrieval_node
from project.nodes.generation import generation_node
from project.nodes.verification import verification_node
from project.nodes.revision import revision_node
from project.nodes.safe_failure import safe_failure_node


def route_query(state: GraphState):
    return state["classification"]

def route_after_verification(state: GraphState):

    if state["verification_passed"]:
        return "end"

    if state["retry_count"] == 0:
        return "revision"

    return "safe_failure"



graph_builder = StateGraph(GraphState)

# Nodes
graph_builder.add_node("triage", triage_node)
graph_builder.add_node("clarification", clarification_node)
graph_builder.add_node("out_of_scope", out_of_scope_node)
graph_builder.add_node("retrieval", retrieval_node)
graph_builder.add_node("generation", generation_node)
graph_builder.add_node("verification", verification_node)
graph_builder.add_node("revision", revision_node)
graph_builder.add_node("safe_failure", safe_failure_node)


# Flow
graph_builder.add_edge(START, "triage")
graph_builder.add_conditional_edges(
    "triage",
    route_query,
    {
        "answerable": "retrieval",
        "requires_clarification": "clarification",
        "out_of_scope": "out_of_scope",

        # Temporary
        "requires_escalation": "retrieval",
    },
)

graph_builder.add_edge("clarification", END)
graph_builder.add_edge("out_of_scope", END)
graph_builder.add_edge("retrieval", "generation")
graph_builder.add_edge("generation", "verification")
graph_builder.add_conditional_edges(
    "verification",
    route_after_verification,
    {
        "revision": "revision",
        "safe_failure": "safe_failure",
        "end": END,
    },
)
graph_builder.add_edge("safe_failure", END)

graph = graph_builder.compile()