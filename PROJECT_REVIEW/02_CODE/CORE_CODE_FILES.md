# ResearchNexusAI — Top Core Code Files (23 A+ Architectural Spine)

> **Authoritative Inventory Reference:** PROJECT_REVIEW_CODE_INVENTORY.md  
> **Status:** Authoritative Core Preparation Guide  

These 23 files form the complete execution backbone of ResearchNexusAI. Technical reviewers, examiners, and faculty auditors will focus questions primarily on this architectural sequence.

---

## The 23 A+ Core Files in Study Order

| # | File Path | Category | Importance | Actual Role / Purpose |
|---|---|---|---|---|
| 1 | src/App.tsx | FRONTEND_ENTRY | **A+** | Root React routing configuration, theme layout providers, and navigation shell. |
| 2 | ackend/app/main.py | BACKEND_ENTRY | **A+** | FastAPI application initialization, CORS middleware, router registrations, and lifecycle events. |
| 3 | ackend/app/api/ai.py | API | **A+** | Endpoints for RAG query processing, live paper synthesis, and XAI explanation generation. |
| 4 | ackend/app/api/papers.py | API | **A+** | Endpoints for searching, filtering, and retrieving paper details and metadata. |
| 5 | ackend/app/api/research.py | API | **A+** | Endpoints orchestrating deep literature research, comparative matrices, and gap analysis. |
| 6 | ackend/app/models/paper.py | DATABASE | **A+** | SQLAlchemy ORM model defining paper metadata, chunks, citations, and embeddings schema. |
| 7 | ackend/app/services/assistant/enhanced_rag.py | RAG_ORCHESTRATION | **A+** | Multi-stage RAG orchestrator coordinating retrieval, prompt assembly, claim checking, and citations. |
| 8 | ackend/app/services/assistant/iterative_rag.py | RAG_ORCHESTRATION | **A+** | Iterative multi-turn retrieval and refinement loop managing feedback-driven re-querying. |
| 9 | ackend/app/services/retrieval.py | RETRIEVAL | **A+** | Dual BM25 + ChromaDB dense retrieval, Reciprocal Rank Fusion (RRF), and BGE reranker scoring. |
| 10 | ackend/app/services/local_evidence.py | RETRIEVAL | **A+** | Local corpus retrieval engine with cached indexes, token cleaning, and dense embedding matching. |
| 11 | chunk_corpus.py | DATA_INGESTION | **A+** | Offline pipeline script to chunk corpus. |
| 12 | embed_corpus.py | DATA_INGESTION | **A+** | Offline pipeline script to embed corpus. |
| 13 | uild_indexes.py | DATA_INGESTION | **A+** | Offline pipeline script to build indexes. |
| 14 | ackend/app/services/llm_provider.py | GENERATION_LLM | **A+** | Multi-provider LLM interface (Groq, Gemini, OpenAI, Claude) with fallback and prompt caching. |
| 15 | ackend/app/services/assistant/synthesis_engine.py | GENERATION_LLM | **A+** | Scientific synthesis generator constructing multi-paper summaries and structured analyses. |
| 16 | ackend/app/services/assistant/claim_verifier.py | CLAIM_VERIFICATION | **A+** | Automated NLI/LLM claim verification checking factual statements against retrieved context. |
| 17 | ackend/app/services/assistant/citation_repair.py | CITATION_PROVENANCE_XAI | **A+** | Rule-based citation repair attempting to ground unverified claims to retrieved chunk IDs. |
| 18 | src/utils/api.ts | FRONTEND_API_SERVICES | **A+** | Core frontend HTTP client providing typed calls to backend FastAPI endpoints. |
| 19 | src/pages/HybridSearchPage.tsx | FRONTEND_PAGES | **A+** | Primary user-facing view for HybridSearchPage. |
| 20 | src/pages/AssistantPage.tsx | FRONTEND_PAGES | **A+** | Primary user-facing view for AssistantPage. |
| 21 | src/pages/LiteratureReviewPage.tsx | FRONTEND_PAGES | **A+** | Primary user-facing view for LiteratureReviewPage. |
| 22 | src/pages/XaiPage.tsx | FRONTEND_PAGES | **A+** | Primary user-facing view for XaiPage. |
| 23 | evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py | EVALUATION | **A+** | Authoritative V4 canonical reconciliation reproduction script. |

---

## Detailed File Specifications

### 1. src/App.tsx
- **Category:** FRONTEND_ENTRY | **Importance:** A+
- **Actual Purpose:** Top-level React routing declaration, authentication wrapper, and navigation shell.
- **Why Reviewer Asks:** Primary frontend routing architecture determining page transitions and access control.
- **Main Concepts to Study:** React Router v6 nested layout routing, ProtectedRoute HOC, Zustand auth integration.
- **Dependencies / Related Files:** src/layouts/AppLayout.tsx, src/store/authStore.ts, src/utils/api.ts.

### 2. ackend/app/main.py
- **Category:** BACKEND_ENTRY | **Importance:** A+
- **Actual Purpose:** FastAPI bootstrap application, middleware configuration, CORS origins, and API route registrations.
- **Why Reviewer Asks:** Central server bootstrap point and API route aggregator.
- **Main Concepts to Study:** FastAPI lifecycle events, middleware stack, prefix routers (/api/ai, /api/papers, /api/research).
- **Dependencies / Related Files:** ackend/app/api/*.py, ackend/app/core/config.py.

### 3. ackend/app/api/ai.py
- **Category:** API | **Importance:** A+
- **Actual Purpose:** Endpoints for RAG query processing, live paper synthesis, and XAI explanation generation.
- **Why Reviewer Asks:** Direct API surface invoked by frontend for AI synthesis and XAI traces.
- **Main Concepts to Study:** Request validation via Pydantic (AskRequest), asynchronous request handling, synthesis orchestrator invocation.
- **Dependencies / Related Files:** ackend/app/services/assistant/enhanced_rag.py, ackend/app/services/assistant/synthesis_engine.py.

### 4. ackend/app/api/papers.py
- **Category:** API | **Importance:** A+
- **Actual Purpose:** Endpoints for searching, filtering, and retrieving paper details and metadata.
- **Why Reviewer Asks:** Core paper catalog search and retrieval API gateway.
- **Main Concepts to Study:** Query normalization, metadata filtering, hybrid search execution dispatch.
- **Dependencies / Related Files:** ackend/app/services/retrieval.py, ackend/app/models/paper.py.

### 5. ackend/app/api/research.py
- **Category:** API | **Importance:** A+
- **Actual Purpose:** Endpoints orchestrating deep literature research, comparative matrices, and gap analysis.
- **Why Reviewer Asks:** Powers advanced comparative literature review workflows.
- **Main Concepts to Study:** Multi-paper comparison contracts, matrix generation, persistent research sessions.
- **Dependencies / Related Files:** ackend/app/services/assistant/comparison_engine.py, ackend/app/services/research_session_service.py.

### 6. ackend/app/models/paper.py
- **Category:** DATABASE | **Importance:** A+
- **Actual Purpose:** SQLAlchemy ORM model defining paper metadata, chunks, citations, and embeddings schema.
- **Why Reviewer Asks:** Core database entity storing scientific corpus records.
- **Main Concepts to Study:** Relational schema design, vector embedding foreign keys, chunk indexing.
- **Dependencies / Related Files:** ackend/app/db/session.py, ResearchMind_LocalKB/metadata/.

### 7. ackend/app/services/assistant/enhanced_rag.py
- **Category:** RAG_ORCHESTRATION | **Importance:** A+
- **Actual Purpose:** Multi-stage RAG orchestrator coordinating retrieval, prompt assembly, claim checking, and citations.
- **Why Reviewer Asks:** Master pipeline orchestrating end-to-end evidence synthesis.
- **Main Concepts to Study:** End-to-end RAG state machine, passage injection, verifier dispatch, grounding metrics calculation.
- **Dependencies / Related Files:** ackend/app/services/retrieval.py, ackend/app/services/assistant/claim_verifier.py, ackend/app/services/llm_provider.py.

### 8. ackend/app/services/assistant/iterative_rag.py
- **Category:** RAG_ORCHESTRATION | **Importance:** A+
- **Actual Purpose:** Iterative multi-turn retrieval and refinement loop managing feedback-driven re-querying.
- **Why Reviewer Asks:** Executes iterative refinement tested in benchmark e07.
- **Main Concepts to Study:** Feedback loop conditions, refinement query formulation, termination bounds.
- **Dependencies / Related Files:** ackend/app/services/assistant/enhanced_rag.py, ackend/app/services/assistant/self_feedback.py.

### 9. ackend/app/services/retrieval.py
- **Category:** RETRIEVAL | **Importance:** A+
- **Actual Purpose:** Dual BM25 + ChromaDB dense retrieval, Reciprocal Rank Fusion (RRF), and BGE reranker scoring.
- **Why Reviewer Asks:** Core algorithmic module for hybrid multi-stage scientific document retrieval.
- **Main Concepts to Study:** BM25 scoring, dense cosine similarity, RRF formula ((d) = \sum \frac{1}{k + r(d)}$, =60$), cross-encoder reranking.
- **Dependencies / Related Files:** 
ank_bm25, chromadb, sentence_transformers.

### 10. ackend/app/services/local_evidence.py
- **Category:** RETRIEVAL | **Importance:** A+
- **Actual Purpose:** Local corpus retrieval engine with cached indexes, token cleaning, and dense embedding matching.
- **Why Reviewer Asks:** Execution engine for local KB corpus searches.
- **Main Concepts to Study:** Precomputed index loading, token filtering, memory-efficient passage retrieval.
- **Dependencies / Related Files:** ResearchMind_LocalKB/indexes/, ackend/app/models/paper.py.

### 11. chunk_corpus.py
- **Category:** DATA_INGESTION | **Importance:** A+
- **Actual Purpose:** Offline pipeline script to chunk scientific paper full texts into passages.
- **Why Reviewer Asks:** Determines granularity and context boundary for all retrieval and grounding operations.
- **Main Concepts to Study:** Sliding window chunking, token length constraints, metadata preservation.
- **Dependencies / Related Files:** ResearchMind_LocalKB/extracted_text/, ResearchMind_LocalKB/chunks/.

### 12. embed_corpus.py
- **Category:** DATA_INGESTION | **Importance:** A+
- **Actual Purpose:** Offline pipeline script to embed corpus passages using dense neural embeddings.
- **Why Reviewer Asks:** Directly creates the vector index powering dense retrieval evaluation.
- **Main Concepts to Study:** Dense sentence embeddings (BAAI/bge-base-en-v1.5), ChromaDB batch insertion, cosine space indexing.
- **Dependencies / Related Files:** chunk_corpus.py, ResearchMind_LocalKB/embeddings/.

### 13. uild_indexes.py
- **Category:** DATA_INGESTION | **Importance:** A+
- **Actual Purpose:** Offline pipeline script to build inverted BM25 indices and manifest maps.
- **Why Reviewer Asks:** Creates the lexical search baseline and ID mapping table.
- **Main Concepts to Study:** Inverted index serialization, token frequency calculation, synchronization with Chroma IDs.
- **Dependencies / Related Files:** ResearchMind_LocalKB/indexes/bm25_index.pkl, ResearchMind_LocalKB/indexes/bm25_mapping.json.

### 14. ackend/app/services/llm_provider.py
- **Category:** GENERATION_LLM | **Importance:** A+
- **Actual Purpose:** Multi-provider LLM interface (Groq, Gemini, OpenAI, Claude) with fallback and prompt caching.
- **Why Reviewer Asks:** Central generation driver communicating with foundation models.
- **Main Concepts to Study:** Provider abstraction, deterministic temperature settings, retry and fallback architecture.
- **Dependencies / Related Files:** ackend/app/core/config.py, external LLM APIs.

### 15. ackend/app/services/assistant/synthesis_engine.py
- **Category:** GENERATION_LLM | **Importance:** A+
- **Actual Purpose:** Scientific synthesis generator constructing multi-paper summaries and structured analyses.
- **Why Reviewer Asks:** Drives structured scientific synthesis outputs.
- **Main Concepts to Study:** Multi-document prompt engineering, synthesis extraction, inline citation insertion.
- **Dependencies / Related Files:** ackend/app/services/llm_provider.py, ackend/app/services/assistant/synthesis_extractor.py.

### 16. ackend/app/services/assistant/claim_verifier.py
- **Category:** CLAIM_VERIFICATION | **Importance:** A+
- **Actual Purpose:** Automated NLI/LLM claim verification checking factual statements against retrieved context.
- **Why Reviewer Asks:** Core novelty module verifying generated claims for grounding.
- **Main Concepts to Study:** Factual claim extraction, natural language inference entailment scoring, grounding precision/recall metrics.
- **Dependencies / Related Files:** ackend/app/services/assistant/claim_extractor.py, ackend/app/services/assistant/enhanced_rag.py.

### 17. ackend/app/services/assistant/citation_repair.py
- **Category:** CITATION_PROVENANCE_XAI | **Importance:** A+
- **Actual Purpose:** Rule-based citation repair attempting to ground unverified claims to retrieved chunk IDs.
- **Why Reviewer Asks:** Key audited module evaluated in benchmark e06 / Module 3.
- **Main Concepts to Study:** Rule-based chunk alignment, frozen test findings (.0\%$ coverage across C0, C1, C2; 1/5 claims), repair safety limitations.
- **Dependencies / Related Files:** ackend/app/services/assistant/claim_verifier.py, evaluation/module_03/.

### 18. src/utils/api.ts
- **Category:** FRONTEND_API_SERVICES | **Importance:** A+
- **Actual Purpose:** Core frontend HTTP client providing typed calls to backend FastAPI endpoints.
- **Why Reviewer Asks:** Central interface between React components and backend API services.
- **Main Concepts to Study:** Axios request/response interceptors, JWT authorization header injection, unified error dispatch.
- **Dependencies / Related Files:** src/store/authStore.ts, backend API routes.

### 19. src/pages/HybridSearchPage.tsx
- **Category:** FRONTEND_PAGES | **Importance:** A+
- **Actual Purpose:** Primary user-facing view for hybrid lexical and dense document search.
- **Why Reviewer Asks:** Visual realization of the hybrid retrieval model presented in the research paper.
- **Main Concepts to Study:** Search parameter tuning, rank score visualization, paper inspection modals.
- **Dependencies / Related Files:** src/utils/api.ts, src/components/search/.

### 20. src/pages/AssistantPage.tsx
- **Category:** FRONTEND_PAGES | **Importance:** A+
- **Actual Purpose:** Primary conversational RAG interface displaying synthesized answers and inline citations.
- **Why Reviewer Asks:** Primary user experience demonstrating end-to-end evidence synthesis.
- **Main Concepts to Study:** Real-time synthesis rendering, verified claim badges, evidence drawer toggles.
- **Dependencies / Related Files:** src/utils/api.ts, src/components/assistant/.

### 21. src/pages/LiteratureReviewPage.tsx
- **Category:** FRONTEND_PAGES | **Importance:** A+
- **Actual Purpose:** Primary user-facing view for multi-paper comparative literature reviews and gap analysis.
- **Why Reviewer Asks:** Demonstrates complex multi-document scientific literature synthesis.
- **Main Concepts to Study:** Comparative matrix tables, research gap highlights, exportable review summaries.
- **Dependencies / Related Files:** src/utils/api.ts, ackend/app/api/research.py.

### 22. src/pages/XaiPage.tsx
- **Category:** FRONTEND_PAGES | **Importance:** A+
- **Actual Purpose:** Primary Explainable AI view rendering evidence provenance graphs and claim verification traces.
- **Why Reviewer Asks:** The Explainable AI core demonstrating transparent provenance from PDF chunks to claims.
- **Main Concepts to Study:** Provenance path visualization, attention / relevance distributions, claim audit inspector.
- **Dependencies / Related Files:** src/components/xai/, src/utils/api.ts.

### 23. evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py
- **Category:** EVALUATION | **Importance:** A+
- **Actual Purpose:** Authoritative V4 canonical reconciliation reproduction script recalculating all paper metrics.
- **Why Reviewer Asks:** The single reproduction gate verifying IEEE paper metrics against frozen experimental outputs.
- **Main Concepts to Study:** Canonical benchmark manifest (=90$), retrieval evaluation (@20=0.867$), claim accounting (=5$), grounding metrics.
- **Dependencies / Related Files:** evaluation/Re-evaluation of mistakes/, 
esearch_artifacts/results_freeze/.
