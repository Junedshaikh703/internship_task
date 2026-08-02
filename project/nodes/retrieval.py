from project.graph.state import GraphState
from project.rag.retriever import retrieve_documents


def retrieval_node(state: GraphState) -> GraphState:
    """
    Retrieve relevant documents for the user query.
    """

    documents = retrieve_documents(state["query"])

    return {
        **state,
        "retrieved_documents": documents,
    }