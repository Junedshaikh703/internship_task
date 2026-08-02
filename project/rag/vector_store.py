from langchain_community.vectorstores import FAISS

from config import VECTOR_STORE_DIR
from project.models.embeddings import embeddings
from project.rag.loader import load_documents


def build_vector_store() -> FAISS:
    """
    Build a FAISS vector store from all documents
    and save it locally.
    """

    documents = load_documents()

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings,
    )

    vector_store.save_local(str(VECTOR_STORE_DIR))

    return vector_store


def load_vector_store() -> FAISS:
    """
    Load the saved FAISS vector store.
    """

    return FAISS.load_local(
        folder_path=str(VECTOR_STORE_DIR),
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )