import json
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

from config import KNOWLEDGE_BASE_DIR, RESOLVED_CASES_FILE


def _load_knowledge_base() -> list[Document]:
    """
    Load all markdown knowledge base documents.
    """

    loader = DirectoryLoader(
        path=str(KNOWLEDGE_BASE_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    documents = loader.load()

    for doc in documents:
        file_path = Path(doc.metadata["source"])
        filename = file_path.stem

        kb_number = int(filename.split("_")[0])

        doc.metadata.update(
            {
                "source_id": f"KB-{kb_number:03d}",
                "title": filename.replace("_", " ").title(),
                "type": "knowledge_base",
            }
        )

    return documents


def _load_resolved_cases() -> list[Document]:
    """
    Load resolved support cases and convert them into LangChain Documents.
    """

    with open(RESOLVED_CASES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cases = data["cases"]

    documents: list[Document] = []

    for case in cases:

        if case.get("status") == "superseded":
            continue

        page_content_parts = []

        if case.get("title"):
            page_content_parts.append(f"Title:\n{case['title']}")

        if case.get("symptoms"):
            symptoms = "\n".join(f"- {s}" for s in case["symptoms"])
            page_content_parts.append(f"Symptoms:\n{symptoms}")

        if case.get("resolution"):
            resolution = "\n".join(f"- {r}" for r in case["resolution"])
            page_content_parts.append(f"Resolution:\n{resolution}")

        if case.get("important_limit"):
            page_content_parts.append(
                f"Important Limitation:\n{case['important_limit']}"
            )

        documents.append(
            Document(
                page_content="\n\n".join(page_content_parts),
                metadata={
                    "source_id": case.get("case_id"),
                    "type": "resolved_case",
                    "status": case.get("status"),
                    "product_version": case.get("product_version"),
                    "source_documents": case.get("source_documents", []),
                },
            )
        )

    return documents

def load_documents() -> list[Document]:
    """
    Load the complete searchable corpus.

    Returns:
        List[Document]: Knowledge Base + Valid Resolved Cases
    """

    kb_documents = _load_knowledge_base()
    resolved_case_documents = _load_resolved_cases()

    return kb_documents + resolved_case_documents