import json

from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser

from project.graph.state import GraphState
from project.models.llm import chat_model
from project.prompts.verification import SYSTEM_PROMPT


class VerificationResult(BaseModel):
    verification_passed: bool = Field(
        description="Whether the generated answer is fully supported by the retrieved context."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0."
    )

    requires_human: bool = Field(
        description="Whether the query should be escalated to a human."
    )

    reason: str = Field(
        description="Reason for the verification decision."
    )


parser = PydanticOutputParser(
    pydantic_object=VerificationResult
)


def verification_node(state: GraphState) -> GraphState:
    """
    Verify the generated answer using the retrieved documents.
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

Generated Answer:
{state["answer"]}
"""
        ),
    ]

    response = chat_model.invoke(messages)

    try:
        result = parser.parse(response.content)

    except Exception:
        result = VerificationResult(
            verification_passed=False,
            confidence=0.0,
            requires_human=True,
            reason="The verifier failed to return a valid structured response.",
        )

    return {
        **state,
        "verification_passed": result.verification_passed,
        "confidence": result.confidence,
        "requires_human": result.requires_human,
        "reason": result.reason,
    }