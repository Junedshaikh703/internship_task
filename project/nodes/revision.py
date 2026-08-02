from langchain_core.messages import HumanMessage, SystemMessage

from project.graph.state import GraphState
from project.models.llm import chat_model
from project.prompts.revision import SYSTEM_PROMPT


def revision_node(state: GraphState) -> GraphState:
    """
    Revise the previous answer using the verification feedback.
    """

    context = "\n\n".join(
        f"Document {i + 1}:\n{doc.page_content}"
        for i, doc in enumerate(state["retrieved_documents"])
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
Retrieved Context:
{context}

User Question:
{state["query"]}

Previous Answer:
{state["answer"]}

Verification Feedback:
{state["reason"]}

Rewrite the answer.
"""
        ),
    ]

    response = chat_model.invoke(messages)

    return {
        **state,
        "answer": response.content.strip(),
        "retry_count": state["retry_count"] + 1,
    }