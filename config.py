from pathlib import Path

# ======================================================
# Project Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent

PROJECT_DIR = PROJECT_ROOT / "project"

DATA_DIR = PROJECT_DIR / "data"

KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge_base"

RESOLVED_CASES_FILE = DATA_DIR / "resolved_cases.json"

VECTOR_STORE_DIR = PROJECT_DIR / "vector_store"

# ======================================================
# Models
# ======================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

LLM_MODEL = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

# ======================================================
# Retrieval
# ======================================================

TOP_K = 3


# print(KNOWLEDGE_BASE_DIR)
# print(RESOLVED_CASES_FILE)