from langchain_core.documents import Document

from config import TOP_K
from project.rag.vector_store import load_vector_store


def retrieve_documents(query: str) -> list[Document]:
    """
    Retrieve the most relevant documents for a user query.
    """

    vector_store = load_vector_store()

    documents = vector_store.similarity_search(
        query=query,
        k=TOP_K,
    )

    return documents