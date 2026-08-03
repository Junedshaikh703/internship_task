# OrbitDesk AI Support Assistant

> AI-powered customer support workflow built with LangGraph, Retrieval-Augmented Generation (RAG), and local Hugging Face models.

---

## Overview

Traditional RAG pipelines retrieve context and generate an answer in a single pass. While effective for straightforward questions, they lack mechanisms for handling ambiguous queries, validating generated responses, or recovering from unsupported answers.

This project extends a standard RAG pipeline into a workflow-oriented AI support system using LangGraph. Instead of treating question answering as a single LLM call, the solution decomposes the problem into multiple specialized nodes responsible for classification, retrieval, response generation, verification, revision, and safe failure handling.

The workflow is designed around three engineering goals:

- Produce grounded responses using only the supplied OrbitDesk documentation.
- Prevent unsupported or hallucinated answers through an explicit verification stage.
- Gracefully recover from failures using revision and safe fallback strategies.

---

# System Architecture

```text
                                    User Query
                                         │
                                         ▼
                             ┌────────────────────┐
                             │   Triage Node      │
                             └────────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
        ▼                                ▼                                ▼
  Answerable                    Clarification                  Out of Scope
        │                                │                                │
        ▼                                ▼                                ▼
 Semantic Retrieval             Return Clarification        Safe Response
      (FAISS)
        │
        ▼
 Context Construction
        │
        ▼
 Response Generation
        │
        ▼
 Verification
        │
   ┌────┴─────┐
   │          │
   ▼          ▼
Pass       Fail
 │           │
 │      Retry < Limit
 │           │
 ▼           ▼
END      Revision
             │
             └──────────────► Generation
```

---

# Workflow

## 1. Query Triage

Every incoming query first passes through a dedicated triage node.

The node classifies the request into one of four categories:

- Answerable
- Requires Clarification
- Requires Escalation
- Out of Scope

Rather than forcing every request through retrieval, this early routing reduces unnecessary computation and allows different handling strategies depending on user intent.

---

## 2. Semantic Retrieval

Answerable and escalation queries continue to the retrieval stage.

Sentence Transformers generate dense embeddings for every knowledge base document and resolved support case. These embeddings are indexed using FAISS for efficient semantic search.

The retriever returns the most relevant context together with document identifiers, which are later surfaced as supporting sources.

---

## 3. Response Generation

The generation node constructs the final prompt using:

- User query
- Retrieved documents
- System instructions

The language model is instructed to answer **only from the supplied context** and avoid introducing external knowledge.

---

## 4. Answer Verification

Unlike conventional RAG systems, generated responses are not immediately returned.

Instead, every answer passes through a dedicated verification node.

The verifier evaluates whether the generated response is completely supported by the retrieved documents.

Structured verification outputs include:

- verification_passed
- confidence
- requires_human
- reason

Pydantic validates these fields before they are written into the graph state.

---

## 5. Revision

If verification fails, the workflow performs a controlled revision.

The verifier feedback is supplied back to the generator, allowing the model to correct unsupported statements.

A retry counter prevents infinite correction loops.

---

## 6. Safe Failure

When the retry limit is exhausted, the workflow terminates with a safe fallback response rather than repeatedly generating unsupported answers.

This guarantees deterministic behaviour even when verification repeatedly fails.

---

# Graph State

Every workflow node communicates through a shared graph state.

```text
GraphState

├── query
├── classification
├── retrieved_documents
├── answer
├── verification_passed
├── confidence
├── requires_human
├── reason
└── sources
```

This shared state enables loosely coupled nodes while keeping the workflow deterministic.

---

# Project Structure

```text
project/

├── data/
│   ├── knowledge_base/
│   └── resolved_cases/
│
├── graph/
│   ├── builder.py
│   └── state.py
│
├── models/
│   Local Hugging Face model configuration
│
├── nodes/
│   ├── triage.py
│   ├── retrieval.py
│   ├── generation.py
│   ├── verification.py
│   ├── revision.py
│   ├── clarification.py
│   ├── out_of_scope.py
│   └── safe_failure.py
│
├── prompts/
│   Prompt templates for every workflow node
│
├── vectorstore/
│   FAISS index creation
│
└── tests/
    Automated workflow tests
```

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| LangGraph | Workflow orchestration |
| LangChain | Prompt management and model abstraction |
| Hugging Face | Local language model inference |
| Sentence Transformers | Dense embedding generation |
| FAISS | Semantic vector retrieval |
| Pydantic | Structured output validation |
| LangSmith | Workflow tracing and observability |
| Pytest | Automated testing |

---

# Design Decisions

## Why LangGraph?

The workflow contains multiple conditional execution paths including clarification, verification, retries, and safe failure. LangGraph provides explicit state management and routing, making it a natural fit for this architecture.

---

## Why Retrieval-Augmented Generation?

Keeping the knowledge base external ensures generated responses remain grounded in the supplied OrbitDesk documentation instead of relying solely on model parameters.

---

## Why Verification?

Retrieval alone cannot guarantee factual correctness. A dedicated verification stage prevents unsupported information from being returned to the user.

---

## Why Revision?

Rather than immediately failing verification, the system attempts one corrective generation pass, improving robustness while maintaining deterministic execution.

---

## Why Structured Outputs?

Verification results are validated with Pydantic before updating the graph state, ensuring every downstream node receives well-formed data.

---

# Installation

```bash
git clone <repository-url>
cd internship_task

python -m venv myenv

# Windows
myenv\Scripts\activate

# Linux/macOS
source myenv/bin/activate

pip install -r requirements.txt
```

---

# Environment Variables

```env
LANGSMITH_API_KEY=your_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=OrbitDesk-RAG
```

---

# Running the Project

```bash
python main.py
```

---

# Running Tests

```bash
python -m pytest
```

---

# Observability

The complete workflow is instrumented using LangSmith.

Each execution records:

- Node execution order
- Prompt inputs
- LLM responses
- State transitions
- Execution traces

This enables debugging and inspection of every workflow invocation.

---

# Current Limitations

- Dense retrieval only
- Single-turn interactions
- Fixed retry limit
- No reranking stage
- Local model quality depends on the selected checkpoint

---

# Future Improvements

- Hybrid retrieval (Dense + BM25)
- Cross-encoder reranking
- Multi-turn conversation memory
- Streaming responses
- Confidence calibration
- Human approval workflow

---

# Acknowledgement

This project was developed as part of an AI Engineering internship take-home assignment. The supplied OrbitDesk knowledge base and resolved support cases are treated as the authoritative source of information for all generated responses.
