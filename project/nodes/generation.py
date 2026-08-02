from langchain_core.messages import HumanMessage, SystemMessage

from project.graph.state import GraphState
from project.models.llm import chat_model
from project.prompts.generation import SYSTEM_PROMPT


def generation_node(state: GraphState) -> GraphState:
    """
    Generate an answer using the retrieved context.
    """

    context = "\n\n".join(
        f"Document {i + 1}:\n{doc.page_content}"
        for i, doc in enumerate(state["retrieved_documents"])
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
Context:
{context}

Question:
{state["query"]}
"""
        ),
    ]

    response = chat_model.invoke(messages)

    answer = response.content

    sources = [
        doc.metadata["source_id"]
        for doc in state["retrieved_documents"]
    ]

    return {
        **state,
        "answer": answer,
        "sources": sources,
    }