# OrbitDesk AI Support Assistant

An AI-powered customer support assistant built using **LangGraph**, **Retrieval-Augmented Generation (RAG)**, and **local Hugging Face models**. The system answers OrbitDesk support questions using only the provided knowledge base and resolved support cases while following a graph-based workflow for query routing, answer generation, verification, and recovery.

---

# Project Overview

Traditional RAG systems retrieve documents and generate an answer in a single pass. This project extends that approach by introducing a workflow-driven architecture using LangGraph.

Instead of relying on a single LLM call, the system decomposes the problem into specialized nodes responsible for:

- Query classification
- Context retrieval
- Response generation
- Answer verification
- Revision after failed verification
- Safe failure handling

The workflow ensures responses remain grounded in the supplied OrbitDesk documentation while preventing unsupported or hallucinated answers.

---

## Architecture

<p align="center">
  <img src="docs/architecture.png" width="900">
</p>

The workflow uses conditional routing to determine the appropriate execution path for every user query. Depending on the query type and verification outcome, the graph dynamically selects clarification, retrieval, revision, or safe failure nodes.

---

# Workflow

## 1. Triage

Every incoming query is classified into one of four categories:

- Answerable
- Requires Clarification
- Requires Escalation
- Out of Scope

This determines the execution path through the workflow.

---

## 2. Retrieval

For answerable and escalation queries, the retrieval node performs semantic search over the supplied knowledge base and resolved support cases using FAISS and Sentence Transformers.

---

## 3. Generation

The retrieved context is supplied to the local language model to generate an answer grounded only in the provided documentation.

---

## 4. Verification

Every generated response is validated against the retrieved evidence.

The verifier determines:

- Whether the answer is supported by the retrieved context
- Confidence score
- Human escalation requirement
- Verification reasoning

Structured outputs are validated using Pydantic before being stored in the workflow state.

---

## 5. Revision

If verification fails, the workflow performs one revision cycle. The revised answer is generated using verifier feedback and is verified again.

A retry counter prevents infinite revision loops.

---

## 6. Safe Failure

If verification still fails after the retry limit is reached, the workflow returns a safe fallback response instead of repeatedly regenerating unsupported answers.

---

# Graph State

The workflow uses a shared typed state that is passed between all nodes.

```text
query
classification
retrieved_documents
answer
sources
confidence
requires_human
reason
verification_passed
retry_count
```

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming language |
| LangGraph | Workflow orchestration |
| LangChain | Prompt management and model abstraction |
| Hugging Face Transformers | Local language model inference |
| Sentence Transformers | Embedding generation |
| FAISS | Vector similarity search |
| Pydantic | Structured output validation |
| LangSmith | Workflow tracing |
| Pytest | Automated testing |

---

## Models Used

### Generation Model

- **Model:** SmolLM2-360M-Instruct
- **Revision:** main
- **Loaded Locally:** Yes

### Embedding Model

- **Model:** sentence-transformers/all-MiniLM-L6-v2
- **Revision:** main
- **Loaded Locally:** Yes
---

# Hardware & Performance

Example (replace with your actual values):

| Item | Value |
|------|-------|
| CPU | Intel Core i5-12450H |
| RAM | 16 GB |
| GPU | None / NVIDIA RTX XXXX |
| Operating System | Windows 11 |
| Approximate Model Load Time | XX seconds |
| Average Response Time | XX seconds |

---

# Project Structure

```text
project/
├── data/
│   ├── knowledge_base/
│   └── resolved_cases/
├── graph/
├── models/
├── nodes/
├── prompts/
├── vectorstore/
tests/
main.py
requirements.txt
README.md
```

---

# Installation

```bash
git clone <repository-url>

cd internship_task

python -m venv myenv

# Windows
myenv\Scripts\activate

pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
LANGSMITH_API_KEY=your_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=OrbitDesk-RAG
```

---

# Running the Application

```bash
python main.py
```

---

# Running Tests

```bash
python -m pytest
```

The project includes an automated workflow test that validates graph routing for representative queries.

---

# Observability

Workflow execution is traced using LangSmith.

Each execution records:

- Graph execution path
- Node transitions
- Prompt inputs
- LLM responses
- State transitions
- Execution traces

---

# Design Decisions

### Why LangGraph?

The workflow contains multiple conditional execution paths, making LangGraph a natural choice for stateful orchestration.

### Why RAG?

Retrieval-Augmented Generation ensures responses remain grounded in the supplied OrbitDesk documentation rather than relying solely on model parameters.

### Why Verification?

A dedicated verification stage helps detect unsupported or hallucinated content before returning an answer.

### Why Revision?

Instead of immediately failing verification, the workflow performs one corrective generation pass using verifier feedback.

### Why Safe Failure?

A retry limit prevents infinite loops and guarantees deterministic behaviour when verification repeatedly fails.

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
- Human approval workflow

---

# AI Assistance Disclosure

AI coding assistants were used for brainstorming, code review, debugging assistance, and documentation drafting. The final implementation, workflow design, integration, testing, and engineering decisions were completed, validated, and reviewed by the author in accordance with the assignment guidelines.

---

# Acknowledgement

This project was developed as part of an AI Engineering internship take-home assignment. The supplied OrbitDesk knowledge base and resolved support cases were treated as the authoritative source of information for all generated responses.
