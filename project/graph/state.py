from typing import List

from langchain_core.documents import Document
from typing_extensions import TypedDict


class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # User Input
    query: str

    # classification task
    classification: str

    # Retrieved Context
    retrieved_documents: List[Document]

    # Generated Response
    answer: str

    # Supporting Sources
    sources: List[str]

    # Confidence Score
    confidence: float

    # Human Escalation Flag
    requires_human: bool

    # Reason for Escalation / Verification
    reason: str

    # Verification Result
    verification_passed: bool

    retry_count: int