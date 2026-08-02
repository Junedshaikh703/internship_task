from langgraph.graph import START, END, StateGraph

from project.graph.state import GraphState

from project.nodes.retrieval import retrieval_node
from project.nodes.generation import generation_node
from project.nodes.verification import verification_node


graph_builder = StateGraph(GraphState)

# Nodes
graph_builder.add_node("retrieval", retrieval_node)
graph_builder.add_node("generation", generation_node)
graph_builder.add_node("verification", verification_node)

# Flow
graph_builder.add_edge(START, "retrieval")
graph_builder.add_edge("retrieval", "generation")
graph_builder.add_edge("generation", "verification")
graph_builder.add_edge("verification", END)

graph = graph_builder.compile()