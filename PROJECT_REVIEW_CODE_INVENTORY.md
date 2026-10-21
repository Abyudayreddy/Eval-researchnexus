# ResearchNexusAI — Comprehensive Source Code Inventory & Review Preparation Guide

> **Audited Repository:** `C:\Users\Abyureddy\Downloads\SDC2`  
> **Inventory Date:** October 2026  
> **Status:** Static Code Inventory & Review Handoff (No code modifications, deletions, or moves performed)

---

## Executive Summary & Study Counts

This comprehensive code inventory catalogues all source code, API services, RAG orchestration components, verification algorithms, frontend views, dataset manifests, and evaluation modules present in the **ResearchNexusAI** repository.

### Study Counts Summary

| Metric | Count | Description |
|---|---|---|
| **Total Relevant Source Files** | **665** | Filtered active source, config, data & test files |
| **A+ (Must Know Deeply)** | **23** | Top Core architecture files essential for defense |
| **A (Must Understand)** | **40** | High-importance architectural & supporting modules |
| **B (Supporting Code & Tests)** | **282** | Functional components, connectors, stores, and tests |
| **C (Reference / Historical / Low Priority)** | **320** | Reference datasets, historical scripts, one-time patches |
| **Total Reference / Historical / Do-Not-Study** | **406** | Files not requiring active review memorization |
| **Top Core Review Files Selected** | **23** | Critical path files covering user journey to evaluation |

### Category-Wise Distribution

| Category | File Count | Primary Focus |
|---|---|---|
| `DATASET_KB` | 168 | Detailed in full inventory below |
| `UTILITY` | 126 | Detailed in full inventory below |
| `EVALUATION` | 123 | Detailed in full inventory below |
| `TESTS` | 70 | Detailed in full inventory below |
| `FRONTEND_COMPONENTS` | 61 | Detailed in full inventory below |
| `FRONTEND_PAGES` | 22 | Detailed in full inventory below |
| `API` | 17 | Detailed in full inventory below |
| `RAG_ORCHESTRATION` | 17 | Detailed in full inventory below |
| `DATABASE` | 14 | Detailed in full inventory below |
| `RETRIEVAL` | 12 | Detailed in full inventory below |
| `FRONTEND_STATE` | 6 | Detailed in full inventory below |
| `CONFIGURATION` | 5 | Detailed in full inventory below |
| `DATA_INGESTION` | 5 | Detailed in full inventory below |
| `CITATION_PROVENANCE_XAI` | 5 | Detailed in full inventory below |
| `CLAIM_VERIFICATION` | 4 | Detailed in full inventory below |
| `AUTHENTICATION_SECURITY` | 2 | Detailed in full inventory below |
| `BACKEND_ENTRY` | 2 | Detailed in full inventory below |
| `GENERATION_LLM` | 2 | Detailed in full inventory below |
| `FRONTEND_ENTRY` | 2 | Detailed in full inventory below |
| `FRONTEND_API_SERVICES` | 2 | Detailed in full inventory below |

---

## Top Core Files (A+ Must Know Deeply)

These 23 core files implement the complete end-to-end functionality of ResearchNexusAI. A reviewer will focus almost exclusively on this architectural spine.

| # | File Path | Category | Importance | Actual Role / Purpose |
|---|---|---|---|---|
| 1 | [`src/App.tsx`](src/App.tsx) | `FRONTEND_ENTRY` | **A+** | Root React routing configuration, theme layout providers, and navigation shell. |
| 2 | [`backend/app/main.py`](backend/app/main.py) | `BACKEND_ENTRY` | **A+** | FastAPI application initialization, CORS middleware, router registrations, and lifecycle events. |
| 3 | [`backend/app/api/ai.py`](backend/app/api/ai.py) | `API` | **A+** | Endpoints for RAG query processing, live paper synthesis, and XAI explanation generation. |
| 4 | [`backend/app/api/papers.py`](backend/app/api/papers.py) | `API` | **A+** | Endpoints for searching, filtering, and retrieving paper details and metadata. |
| 5 | [`backend/app/api/research.py`](backend/app/api/research.py) | `API` | **A+** | Endpoints orchestrating deep literature research, comparative matrices, and gap analysis. |
| 6 | [`backend/app/models/paper.py`](backend/app/models/paper.py) | `DATABASE` | **A+** | SQLAlchemy ORM model defining paper metadata, chunks, citations, and embeddings schema. |
| 7 | [`backend/app/services/assistant/enhanced_rag.py`](backend/app/services/assistant/enhanced_rag.py) | `RAG_ORCHESTRATION` | **A+** | Multi-stage RAG orchestrator coordinating retrieval, prompt assembly, claim checking, and citations. |
| 8 | [`backend/app/services/assistant/iterative_rag.py`](backend/app/services/assistant/iterative_rag.py) | `RAG_ORCHESTRATION` | **A+** | Iterative multi-turn retrieval and refinement loop managing feedback-driven re-querying. |
| 9 | [`backend/app/services/retrieval.py`](backend/app/services/retrieval.py) | `RETRIEVAL` | **A+** | Dual BM25 + ChromaDB dense retrieval, Reciprocal Rank Fusion (RRF), and BGE reranker scoring. |
| 10 | [`backend/app/services/local_evidence.py`](backend/app/services/local_evidence.py) | `RETRIEVAL` | **A+** | Local corpus retrieval engine with cached indexes, token cleaning, and dense embedding matching. |
| 11 | [`chunk_corpus.py`](chunk_corpus.py) | `DATA_INGESTION` | **A+** | Offline pipeline script to chunk corpus. |
| 12 | [`embed_corpus.py`](embed_corpus.py) | `DATA_INGESTION` | **A+** | Offline pipeline script to embed corpus. |
| 13 | [`build_indexes.py`](build_indexes.py) | `DATA_INGESTION` | **A+** | Offline pipeline script to build indexes. |
| 14 | [`backend/app/services/llm_provider.py`](backend/app/services/llm_provider.py) | `GENERATION_LLM` | **A+** | Multi-provider LLM interface (Groq, Gemini, OpenAI, Claude) with fallback and prompt caching. |
| 15 | [`backend/app/services/assistant/synthesis_engine.py`](backend/app/services/assistant/synthesis_engine.py) | `GENERATION_LLM` | **A+** | Scientific synthesis generator constructing multi-paper summaries and structured analyses. |
| 16 | [`backend/app/services/assistant/claim_verifier.py`](backend/app/services/assistant/claim_verifier.py) | `CLAIM_VERIFICATION` | **A+** | Automated NLI/LLM claim verification checking factual statements against retrieved context. |
| 17 | [`backend/app/services/assistant/citation_repair.py`](backend/app/services/assistant/citation_repair.py) | `CITATION_PROVENANCE_XAI` | **A+** | Rule-based citation repair attempting to ground unverified claims to retrieved chunk IDs. |
| 18 | [`src/utils/api.ts`](src/utils/api.ts) | `FRONTEND_API_SERVICES` | **A+** | Core frontend HTTP client providing typed calls to backend FastAPI endpoints. |
| 19 | [`src/pages/HybridSearchPage.tsx`](src/pages/HybridSearchPage.tsx) | `FRONTEND_PAGES` | **A+** | Primary user-facing view for HybridSearchPage. |
| 20 | [`src/pages/AssistantPage.tsx`](src/pages/AssistantPage.tsx) | `FRONTEND_PAGES` | **A+** | Primary user-facing view for AssistantPage. |
| 21 | [`src/pages/LiteratureReviewPage.tsx`](src/pages/LiteratureReviewPage.tsx) | `FRONTEND_PAGES` | **A+** | Primary user-facing view for LiteratureReviewPage. |
| 22 | [`src/pages/XaiPage.tsx`](src/pages/XaiPage.tsx) | `FRONTEND_PAGES` | **A+** | Primary user-facing view for XaiPage. |
| 23 | [`evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py`](evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py) | `EVALUATION` | **A+** | Authoritative V4 canonical reconciliation reproduction script. |

---

## Core Code Study Order (A+ Sequenced)

Follow this exact numbered sequence to prepare for technical questioning, architecture walkthroughs, and viva defense:

### 1. `src/App.tsx`
- **Stage:** Frontend Root & Application Shell
- **Category:** `FRONTEND_ENTRY` | **Importance:** **A+**
- **Actual Purpose:** Root React routing configuration, theme layout providers, and navigation shell.
- **Main Classes / Models:** `None`
- **Key Functions:** `ProtectedRoute`
- **Key Imports / Dependencies:** `AnalyticsPage, AppLayout, AssistantPage, ComparisonPage, DashboardPage, DiscussionsPage`
- **Why Reviewers Will Ask:** Primary frontend routing architecture determining page transitions.

### 2. `backend/app/main.py`
- **Stage:** Backend Bootstrap & Lifecycle
- **Category:** `BACKEND_ENTRY` | **Importance:** **A+**
- **Actual Purpose:** FastAPI application initialization, CORS middleware, router registrations, and lifecycle events.
- **Main Classes / Models:** `None`
- **Key Functions:** `root, health_check`
- **Key Imports / Dependencies:** `app, fastapi, os, sqlalchemy`
- **Why Reviewers Will Ask:** Central server bootstrap point and API route aggregator.

### 3. `backend/app/api/ai.py`
- **Stage:** RAG & AI Synthesis Endpoints
- **Category:** `API` | **Importance:** **A+**
- **Actual Purpose:** Endpoints for RAG query processing, live paper synthesis, and XAI explanation generation.
- **Main Classes / Models:** `ContextPaper, AskRequest`
- **Key Functions:** `compare_papers_endpoint, get_comparison_result, ask_ai, explain_ai`
- **Key Imports / Dependencies:** `app, fastapi, pydantic, typing, uuid`
- **Why Reviewers Will Ask:** Direct API surface invoked by frontend for AI synthesis and XAI traces.

### 4. `backend/app/api/papers.py`
- **Stage:** Corpus Paper Catalog Search Gateway
- **Category:** `API` | **Importance:** **A+**
- **Actual Purpose:** Endpoints for searching, filtering, and retrieving paper details and metadata.
- **Main Classes / Models:** `SearchRequest`
- **Key Functions:** `_init_experiment, _update_experiment, _deterministic_query_analysis, _retrieve_postgres_metadata, normalize_title, run_local_search`
- **Key Imports / Dependencies:** `app, asyncio, fastapi, os, pydantic, re`
- **Why Reviewers Will Ask:** Core paper catalog search and retrieval API gateway.

### 5. `backend/app/api/research.py`
- **Stage:** Comparative Synthesis & Literature Review API
- **Category:** `API` | **Importance:** **A+**
- **Actual Purpose:** Endpoints orchestrating deep literature research, comparative matrices, and gap analysis.
- **Main Classes / Models:** `CreateSessionRequest, UpdateSessionRequest, CreateMemoryRequest, UpdateMemoryRequest`
- **Key Functions:** `get_db, create_session, list_sessions, get_session, update_session, soft_delete_session`
- **Key Imports / Dependencies:** `app, fastapi, pydantic, sqlalchemy, typing`
- **Why Reviewers Will Ask:** Powers advanced comparative literature review workflows.

### 6. `backend/app/models/paper.py`
- **Stage:** Core Database Entity & Embeddings Schema
- **Category:** `DATABASE` | **Importance:** **A+**
- **Actual Purpose:** SQLAlchemy ORM model defining paper metadata, chunks, citations, and embeddings schema.
- **Main Classes / Models:** `Domain, Paper, PaperChunk`
- **Key Functions:** `generate_uuid`
- **Key Imports / Dependencies:** `app, sqlalchemy, uuid`
- **Why Reviewers Will Ask:** Core database entity storing scientific corpus records.

### 7. `backend/app/services/assistant/enhanced_rag.py`
- **Stage:** Multi-Stage RAG Pipeline Orchestrator
- **Category:** `RAG_ORCHESTRATION` | **Importance:** **A+**
- **Actual Purpose:** Multi-stage RAG orchestrator coordinating retrieval, prompt assembly, claim checking, and citations.
- **Main Classes / Models:** `EnhancedRAGService`
- **Key Functions:** `None`
- **Key Imports / Dependencies:** `app, re, time, typing, uuid`
- **Why Reviewers Will Ask:** Master pipeline orchestrating end-to-end evidence synthesis.

### 8. `backend/app/services/assistant/iterative_rag.py`
- **Stage:** Iterative Refinement Loop & Feedback Engine
- **Category:** `RAG_ORCHESTRATION` | **Importance:** **A+**
- **Actual Purpose:** Iterative multi-turn retrieval and refinement loop managing feedback-driven re-querying.
- **Main Classes / Models:** `AnswerVersion, IterativeRAGService`
- **Key Functions:** `None`
- **Key Imports / Dependencies:** `app, pydantic, time, typing`
- **Why Reviewers Will Ask:** Executes iterative refinement tested in benchmark e07.

### 9. `backend/app/services/retrieval.py`
- **Stage:** Hybrid Retrieval Engine (BM25 + ChromaDB + RRF + BGE)
- **Category:** `RETRIEVAL` | **Importance:** **A+**
- **Actual Purpose:** Dual BM25 + ChromaDB dense retrieval, Reciprocal Rank Fusion (RRF), and BGE reranker scoring.
- **Main Classes / Models:** `MockCrossEncoder`
- **Key Functions:** `get_reranker, query_chromadb, query_bm25_all, reciprocal_rank_fusion, rerank_with_bge, generate_rag_response`
- **Key Imports / Dependencies:** `app, google, os, rank_bm25, sentence_transformers, typing`
- **Why Reviewers Will Ask:** Core algorithmic module for hybrid multi-stage scientific document retrieval.

### 10. `backend/app/services/local_evidence.py`
- **Stage:** Local Knowledge Base Fast Evidence Retriever
- **Category:** `RETRIEVAL` | **Importance:** **A+**
- **Actual Purpose:** Local corpus retrieval engine with cached indexes, token cleaning, and dense embedding matching.
- **Main Classes / Models:** `LocalEvidenceRetriever`
- **Key Functions:** `clean_token, get_shared_embed_model, get_shared_rerank_model, get_local_retriever`
- **Key Imports / Dependencies:** `app, chromadb, functools, json, os, pickle`
- **Why Reviewers Will Ask:** Execution engine for local KB corpus searches.

### 11. `chunk_corpus.py`
- **Stage:** Scientific Document Text Chunking Pipeline
- **Category:** `DATA_INGESTION` | **Importance:** **A+**
- **Actual Purpose:** Offline pipeline script to chunk corpus.
- **Main Classes / Models:** `None`
- **Key Functions:** `chunk_text, process`
- **Key Imports / Dependencies:** `json, os, re`
- **Why Reviewers Will Ask:** Creates the BM25 indexes and ChromaDB embeddings used in evaluation.

### 12. `embed_corpus.py`
- **Stage:** Corpus Vector Embedding & ChromaDB Batch Storage
- **Category:** `DATA_INGESTION` | **Importance:** **A+**
- **Actual Purpose:** Offline pipeline script to embed corpus.
- **Main Classes / Models:** `None`
- **Key Functions:** `process`
- **Key Imports / Dependencies:** `datetime, json, math, os, sentence_transformers, time`
- **Why Reviewers Will Ask:** Creates the BM25 indexes and ChromaDB embeddings used in evaluation.

### 13. `build_indexes.py`
- **Stage:** Inverted BM25 & Dense Index Builder
- **Category:** `DATA_INGESTION` | **Importance:** **A+**
- **Actual Purpose:** Offline pipeline script to build indexes.
- **Main Classes / Models:** `None`
- **Key Functions:** `clean_token, main`
- **Key Imports / Dependencies:** `chromadb, datetime, json, os, pickle, rank_bm25`
- **Why Reviewers Will Ask:** Creates the BM25 indexes and ChromaDB embeddings used in evaluation.

### 14. `backend/app/services/llm_provider.py`
- **Stage:** Multi-Model LLM Interface & Fallback Manager
- **Category:** `GENERATION_LLM` | **Importance:** **A+**
- **Actual Purpose:** Multi-provider LLM interface (Groq, Gemini, OpenAI, Claude) with fallback and prompt caching.
- **Main Classes / Models:** `LLMProvider, GeminiProvider, LocalOllamaProvider, LLMProviderManager`
- **Key Functions:** `None`
- **Key Imports / Dependencies:** `abc, app, google, httpx, re, typing`
- **Why Reviewers Will Ask:** Central generation driver communicating with foundation models.

### 15. `backend/app/services/assistant/synthesis_engine.py`
- **Stage:** Structured Multi-Paper Synthesis Generator
- **Category:** `GENERATION_LLM` | **Importance:** **A+**
- **Actual Purpose:** Scientific synthesis generator constructing multi-paper summaries and structured analyses.
- **Main Classes / Models:** `LiteratureSynthesisEngine`
- **Key Functions:** `None`
- **Key Imports / Dependencies:** `app, json, sqlalchemy, time, typing, uuid`
- **Why Reviewers Will Ask:** Drives structured scientific synthesis outputs.

### 16. `backend/app/services/assistant/claim_verifier.py`
- **Stage:** Natural Language Inference Claim Verifier
- **Category:** `CLAIM_VERIFICATION` | **Importance:** **A+**
- **Actual Purpose:** Automated NLI/LLM claim verification checking factual statements against retrieved context.
- **Main Classes / Models:** `VerifierAuditRecord, ClaimVerifier`
- **Key Functions:** `None`
- **Key Imports / Dependencies:** `app, pydantic, re, time, typing`
- **Why Reviewers Will Ask:** Core novelty module verifying generated claims for grounding.

### 17. `backend/app/services/assistant/citation_repair.py`
- **Stage:** Rule-Based Citation Repair Engine (Audited Module 3)
- **Category:** `CITATION_PROVENANCE_XAI` | **Importance:** **A+**
- **Actual Purpose:** Rule-based citation repair attempting to ground unverified claims to retrieved chunk IDs.
- **Main Classes / Models:** `CitationRepair`
- **Key Functions:** `None`
- **Key Imports / Dependencies:** `app, re, typing`
- **Why Reviewers Will Ask:** Key audited module evaluated in benchmark e06 / Module 3.

### 18. `src/utils/api.ts`
- **Stage:** Frontend Typed Axios API Bridge
- **Category:** `FRONTEND_API_SERVICES` | **Importance:** **A+**
- **Actual Purpose:** Core frontend HTTP client providing typed calls to backend FastAPI endpoints.
- **Main Classes / Models:** `None`
- **Key Functions:** `API_BASE_URL`
- **Key Imports / Dependencies:** `None`
- **Why Reviewers Will Ask:** Central interface between React components and backend API services.

### 19. `src/pages/HybridSearchPage.tsx`
- **Stage:** Interactive Hybrid Search User Interface
- **Category:** `FRONTEND_PAGES` | **Importance:** **A+**
- **Actual Purpose:** Primary user-facing view for HybridSearchPage.
- **Main Classes / Models:** `None`
- **Key Functions:** `loadBookmarks, loadHistory, startPolling, poll, handleSearchSubmit, handleExplain`
- **Key Imports / Dependencies:** `LocalRetrievalPanel, OnlineRetrievalPanel, Overlays, PaperCard, ResearchAtmosphere, ResearchExecutionPipeline`
- **Why Reviewers Will Ask:** Key feature page demonstrated to reviewers and users.

### 20. `src/pages/AssistantPage.tsx`
- **Stage:** RAG Research Assistant Conversational UI
- **Category:** `FRONTEND_PAGES` | **Importance:** **A+**
- **Actual Purpose:** Primary user-facing view for AssistantPage.
- **Main Classes / Models:** `None`
- **Key Functions:** `handleSendQuestionWithSearchId, handleRunMultiPaperComparison, handleSendQuestion, handleOpenXai, handleSaveSession`
- **Key Imports / Dependencies:** `AskWorkspace, AssistantLanding, ComparisonModalOverlay, ExplorePapersWorkspace, Overlays, ProveWorkspace`
- **Why Reviewers Will Ask:** Key feature page demonstrated to reviewers and users.

### 21. `src/pages/LiteratureReviewPage.tsx`
- **Stage:** Multi-Paper Comparative Synthesis Review UI
- **Category:** `FRONTEND_PAGES` | **Importance:** **A+**
- **Actual Purpose:** Primary user-facing view for LiteratureReviewPage.
- **Main Classes / Models:** `None`
- **Key Functions:** `initReviewState, togglePaperSelection, toggleRequirement, handleGenerateTopicsWithRequirements, generateSynthesis, nextStep`
- **Key Imports / Dependencies:** `api, cn, lucide-react, react, react-router-dom, toastStore`
- **Why Reviewers Will Ask:** Key feature page demonstrated to reviewers and users.

### 22. `src/pages/XaiPage.tsx`
- **Stage:** Explainable AI (XAI) Provenance Visualizer
- **Category:** `FRONTEND_PAGES` | **Importance:** **A+**
- **Actual Purpose:** Primary user-facing view for XaiPage.
- **Main Classes / Models:** `None`
- **Key Functions:** `fetchHistory, getValidationModeText, getSortLogic, openPaper, Section, Item`
- **Key Imports / Dependencies:** `Overlays, api, apiAdapter, cn, lucide-react, overlayStore`
- **Why Reviewers Will Ask:** Key feature page demonstrated to reviewers and users.

### 23. `evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py`
- **Stage:** Authoritative V4 Paper Evaluation Reproduction Gate
- **Category:** `EVALUATION` | **Importance:** **A+**
- **Actual Purpose:** Authoritative V4 canonical reconciliation reproduction script.
- **Main Classes / Models:** `None`
- **Key Functions:** `main`
- **Key Imports / Dependencies:** `csv, json, os, sys`
- **Why Reviewers Will Ask:** The single reproduction entry point recalculating all paper metrics.

---

## Reviewer Question Potential (A+ Files)

Below are the 3–8 specific, highly likely technical questions a reviewer or examiner will ask about each A+ file:

### `src/App.tsx` (FRONTEND_ENTRY)
- [ ] How is client-side routing structured across Search, Synthesis, Assistant, and XAI views?
- [ ] What global context providers (Auth, Theme, Notification) wrap the application tree?
- [ ] How does navigation transition between hybrid search, research review, and deep evidence inspection?
- [ ] How are protected routes or authentication barriers enforced?

### `backend/app/main.py` (BACKEND_ENTRY)
- [ ] Why is this file needed and what is its role in backend lifecycle management?
- [ ] How are CORS middleware, routers, and global exception handlers configured here?
- [ ] What endpoints or routers are exposed to the frontend, and how are prefixes managed?
- [ ] What occurs during the application startup and shutdown lifecycle events?

### `backend/app/api/ai.py` (API)
- [ ] What is the input schema for the /api/ai/query and /api/ai/synthesize endpoints?
- [ ] How does this router bridge frontend requests into the underlying RAG orchestration pipeline?
- [ ] What is the exact JSON structure of the generated response and its attached XAI trace?
- [ ] How are timeouts, rate limits, and LLM API failures handled before returning to the client?

### `backend/app/api/papers.py` (API)
- [ ] What query parameters are supported for searching, filtering, and sorting corpus papers?
- [ ] How does this endpoint retrieve chunk text, citation counts, and vector embeddings from the DB?
- [ ] What caching or pagination mechanisms are implemented to handle 687+ indexed papers?
- [ ] What happens when a requested paper ID does not exist in the local SQLite/PostgreSQL store?

### `backend/app/api/research.py` (API)
- [ ] What analytical capabilities does this endpoint provide beyond simple keyword or vector search?
- [ ] How are multi-paper comparison matrices and research gap analyses assembled and returned?
- [ ] What data models represent the research synthesis sessions and persistent state?
- [ ] How are concurrent synthesis requests scheduled and executed?

### `backend/app/models/paper.py` (DATABASE)
- [ ] What relational columns and indexes are defined on the Paper and PaperChunk SQLAlchemy models?
- [ ] How are document embeddings and metadata (DOI, year, domain, authors) represented?
- [ ] How does this schema relate to ChromaDB vector store collections?
- [ ] What foreign keys or relationships link papers to user workspaces and citations?

### `backend/app/services/assistant/enhanced_rag.py` (RAG_ORCHESTRATION)
- [ ] What are the sequential stages of the Enhanced RAG pipeline from query to verified answer?
- [ ] How does this service integrate retrieval, prompt assembly, claim verification, and repair?
- [ ] What data contracts represent the generated synthesis and its associated provenance trace?
- [ ] What happens if retrieval returns zero relevant passages for an unanswerable query?

### `backend/app/services/assistant/iterative_rag.py` (RAG_ORCHESTRATION)
- [ ] What triggers an iterative refinement loop instead of returning a single-turn answer?
- [ ] How are gap analysis and contradiction detection converted into targeted refinement queries?
- [ ] How does the orchestrator prevent infinite refinement loops and enforce max iteration bounds?
- [ ] What is the observed latency vs. accuracy trade-off across 1, 2, and 3 refinement iterations?

### `backend/app/services/retrieval.py` (RETRIEVAL)
- [ ] How does dual BM25 and ChromaDB dense retrieval operate across candidate documents?
- [ ] What is the exact mathematical formulation of Reciprocal Rank Fusion (RRF) used to merge ranks?
- [ ] Why was the parameter k=60 chosen for RRF scoring?
- [ ] How does BGE reranker (BAAI/bge-reranker-large) rescore top candidate passages, and what fallback occurs if GPU memory is constrained?

### `backend/app/services/local_evidence.py` (RETRIEVAL)
- [ ] How does LocalEvidenceRetriever index and load precomputed BM25 pickles and Chroma vectors?
- [ ] What tokenization and text normalization rules are applied during local token cleaning?
- [ ] What is the input query format and how are candidate passages scored and aggregated?
- [ ] How does this service maintain low latency across the 687-document corpus?

### `chunk_corpus.py` (DATA_INGESTION)
- [ ] What chunking strategy (sliding window, paragraph boundary, token overlap) is implemented here?
- [ ] What are the exact chunk size and overlap parameters applied to the scientific PDF text?
- [ ] How are section headings, formulas, and references preserved or filtered during chunking?
- [ ] What output format and manifest does this script produce for downstream embedding?

### `embed_corpus.py` (DATA_INGESTION)
- [ ] Which embedding model (e.g., BAAI/bge-base-en-v1.5) generates passage vectors?
- [ ] How are chunks batched to prevent memory exhaustion and maximize GPU/CPU throughput?
- [ ] What distance metric (cosine, L2, dot product) is configured for ChromaDB vector storage?
- [ ] How is the embedding manifest validated to ensure zero dropped chunks?

### `build_indexes.py` (DATA_INGESTION)
- [ ] How are the BM25 inverted index and ChromaDB collection initialized and persisted?
- [ ] What data structures are pickled to disk for fast in-memory query evaluation?
- [ ] How does the script verify synchronization between BM25 document IDs and ChromaDB chunk IDs?
- [ ] What integrity checks run after indexing to confirm corpus completeness?

### `backend/app/services/llm_provider.py` (GENERATION_LLM)
- [ ] Which foundation models and LLM APIs (Groq, Gemini, OpenAI, Claude) are integrated?
- [ ] How is provider fallback and error recovery orchestrated if an API endpoint times out or errors?
- [ ] What prompt templates and temperature settings are enforced for deterministic factual generation?
- [ ] How are token usage and latency metrics measured and recorded per invocation?

### `backend/app/services/assistant/synthesis_engine.py` (GENERATION_LLM)
- [ ] How are multi-document evidence snippets organized into structured comparative paragraphs?
- [ ] What mechanisms prevent hallucinated comparisons between conflicting research findings?
- [ ] What structured output format (JSON/Markdown) does the synthesis engine produce?
- [ ] How does the engine format inline numeric citation markers linking claims to sources?

### `backend/app/services/assistant/claim_verifier.py` (CLAIM_VERIFICATION)
- [ ] How are generated synthesis responses decomposed into atomic factual claims?
- [ ] What NLI / entailment model or prompt logic verifies whether retrieved evidence entails each claim?
- [ ] What are the classification labels (Entailed, Contradicted, Unverifiable) and confidence thresholds?
- [ ] How does claim verification output affect the final grounding precision and recall metrics?

### `backend/app/services/assistant/citation_repair.py` (CITATION_PROVENANCE_XAI)
- [ ] What algorithmic rules does CitationRepair use to match unverified claims to retrieved chunks?
- [ ] Why did audited benchmarks show 20.0% coverage across C0, C1, and C2 conditions (1/5 eligible claims)?
- [ ] What limitations prevented CitationRepair from demonstrating safety and effectiveness on test items?
- [ ] What alternative repair architectures (e.g., iterative LLM self-correction) should be considered?

### `src/utils/api.ts` (FRONTEND_API_SERVICES)
- [ ] How is Axios configured with base URLs, request interceptors, and error handlers?
- [ ] What typed API client methods exist for searching, RAG synthesis, and XAI explanations?
- [ ] How are authentication tokens injected into HTTP Authorization headers?
- [ ] How are backend connection errors and network timeouts communicated to the user interface?

### `src/pages/HybridSearchPage.tsx` (FRONTEND_PAGES)
- [ ] How does this page present hybrid search controls (lexical vs. dense weights, domain filters)?
- [ ] How are search results and their respective BM25 and vector scores rendered to the user?
- [ ] How can a user select papers from search results to launch a focused synthesis session?
- [ ] What visual indicators distinguish local corpus documents from external live query results?

### `src/pages/AssistantPage.tsx` (FRONTEND_PAGES)
- [ ] How does the research assistant chat interface display multi-stage RAG answers?
- [ ] How are inline citations rendered and linked to evidence modal previews?
- [ ] How does the user inspect claim verification statuses (Supported, Warning, Unverified)?
- [ ] How is the conversational context scope preserved across multiple user prompts?

### `src/pages/LiteratureReviewPage.tsx` (FRONTEND_PAGES)
- [ ] How does this page guide users through multi-paper comparative literature reviews?
- [ ] How are comparison matrices, thematic clusters, and research gap tables rendered?
- [ ] How does the export functionality compile generated literature reviews into formatted reports?
- [ ] How are user customizations to the review scope persisted to backend workspaces?

### `src/pages/XaiPage.tsx` (FRONTEND_PAGES)
- [ ] What Explainable AI visualizations (attention weights, passage ranks, token saliency) are rendered here?
- [ ] How does the UI illustrate the provenance path from raw PDF chunk to final generated claim?
- [ ] How are confidence intervals and claim entailment scores displayed visually?
- [ ] How can an auditor or reviewer interact with the XAI trace to verify answer grounding?

### `evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py` (EVALUATION)
- [ ] What inputs and benchmark splits does reproduce_v4.py load to recalculate paper metrics?
- [ ] How does it resolve historical discrepancies in Hybrid Hit@20 and claim accounting?
- [ ] What verification assertions ensure all tables match the canonical evidence gate exactly?
- [ ] Why is this script the single authoritative reproduction gate for IEEE paper publication?

---

## Project Code Flow

Based strictly on existing imports, API routers, and service calls in the codebase, the runtime execution flow is:

```text
USER QUERY / INTERACTION
  │
  ▼
1. FRONTEND USER INTERFACE
   ├── src/pages/HybridSearchPage.tsx       (Query input & hybrid controls)
   ├── src/pages/AssistantPage.tsx          (Conversational RAG assistant)
   └── src/pages/LiteratureReviewPage.tsx   (Multi-paper comparative synthesis)
  │
  ▼
2. FRONTEND API BRIDGE
   └── src/utils/api.ts                     (Typed Axios HTTP client)
  │
  ▼
3. BACKEND API ROUTER
   ├── backend/app/main.py                  (FastAPI route registry & CORS)
   ├── backend/app/api/ai.py                (/api/ai/query, /api/ai/synthesize)
   ├── backend/app/api/papers.py            (/api/papers/search, /api/papers/{id})
   └── backend/app/api/research.py          (/api/research/synthesize, /api/research/matrix)
  │
  ▼
4. RAG PIPELINE ORCHESTRATION
   ├── backend/app/services/assistant/enhanced_rag.py   (Master synthesis orchestrator)
   └── backend/app/services/assistant/iterative_rag.py  (Multi-turn refinement loop)
  │
  ▼
5. HYBRID RETRIEVAL
   ├── backend/app/services/retrieval.py               (BM25 + ChromaDB dense retrieval)
   ├── backend/app/services/local_evidence.py          (Local corpus index query engine)
   └── Reciprocal Rank Fusion (RRF, k=60)
  │
  ▼
6. RERANKING
   └── backend/app/services/retrieval.py::rerank_with_bge (BAAI/bge-reranker-large scoring)
  │
  ▼
7. GENERATION (LLM)
   ├── backend/app/services/llm_provider.py            (Multi-provider driver: Groq/Gemini)
   └── backend/app/services/assistant/synthesis_engine.py (Evidence synthesis & paragraph assembly)
  │
  ▼
8. CLAIM VERIFICATION
   ├── backend/app/services/assistant/claim_extractor.py (Atomic factual claim decomposition)
   └── backend/app/services/assistant/claim_verifier.py  (NLI entailment verification against chunks)
  │
  ▼
9. CITATION / PROVENANCE / XAI
   ├── backend/app/services/assistant/citation_repair.py (Rule-based citation repair)
   └── backend/app/services/research_artifact_service.py (Provenance graph & XAI trace assembly)
  │
  ▼
10. RESPONSE TRANSMISSION
   └── FastAPI returns structured JSON: { response, citations, claims, xai_trace, latency }
  │
  ▼
11. FRONTEND VISUALIZATION
   ├── src/pages/AssistantPage.tsx          (Inline verified claims & citations)
   ├── src/pages/XaiPage.tsx                (Attention weights, chunk ranking, audit trace)
   └── src/components/xai/ProvenanceGraph.tsx (Visual evidence provenance graph)
```

---

## Files You Do NOT Need to Study (Do-Not-Study Register)

There are **406** files classified as **REFERENCE**, **HISTORICAL**, or **DO-NOT-STUDY**. Do not spend revision time memorizing these:

### 1. Historical & Temporary Utility Scripts (151 files)
- `scratch/*` (30 scratchpad inspection & temporary scripts, e.g., `capture_page.py`, `inspect_malla.py`)
- `fix_*.py` / `edit_*.py` / `patch_*.py` in root (82 historical one-time patches applied during development)
- `Viva/Presentation_Prep/*` (8 study guide builder scripts)
- `ieee_paper/generate_*.py` (3 one-time docx/figure generator scripts)

### 2. Static Reference Artifacts & Benchmark Logs (255 files)
- `ResearchMind_LocalKB/metadata/*.json` (688 raw paper metadata files excluded from source scanning)
- `ResearchMind_LocalKB/embeddings/*`, `indexes/*`, `manifests/*` (Precomputed vector & BM25 binary indices)
- `research_artifacts/*` (Frozen benchmark logs, e.g., e01 through e11 raw JSON outputs)
- `publication_audit/*` (Early historical audit JSONs superseded by V4 canonical evaluation)
- `evaluation/module_01/`, `module_02/`, `module_03/` raw JSON execution logs

---

## Complete Classified Source Code Inventory (All 665 Files)

| Relative Path | Ext | Category | Status | Importance | Reviewer Likely | Actual Purpose |
|---|---|---|---|---|---|---|
| [`backend/app/api/ai.py`](backend/app/api/ai.py) | `.py` | `API` | `source` | **A+** | **YES** | Endpoints for RAG query processing, live paper synthesis, and XAI explanation generation. |
| [`backend/app/api/papers.py`](backend/app/api/papers.py) | `.py` | `API` | `source` | **A+** | **YES** | Endpoints for searching, filtering, and retrieving paper details and metadata. |
| [`backend/app/api/research.py`](backend/app/api/research.py) | `.py` | `API` | `source` | **A+** | **YES** | Endpoints orchestrating deep literature research, comparative matrices, and gap analysis. |
| [`backend/app/main.py`](backend/app/main.py) | `.py` | `BACKEND_ENTRY` | `source` | **A+** | **YES** | FastAPI application initialization, CORS middleware, router registrations, and lifecycle events. |
| [`backend/app/models/paper.py`](backend/app/models/paper.py) | `.py` | `DATABASE` | `source` | **A+** | **YES** | SQLAlchemy ORM model defining paper metadata, chunks, citations, and embeddings schema. |
| [`backend/app/services/assistant/citation_repair.py`](backend/app/services/assistant/citation_repair.py) | `.py` | `CITATION_PROVENANCE_XAI` | `source` | **A+** | **YES** | Rule-based citation repair attempting to ground unverified claims to retrieved chunk IDs. |
| [`backend/app/services/assistant/claim_verifier.py`](backend/app/services/assistant/claim_verifier.py) | `.py` | `CLAIM_VERIFICATION` | `source` | **A+** | **YES** | Automated NLI/LLM claim verification checking factual statements against retrieved context. |
| [`backend/app/services/assistant/enhanced_rag.py`](backend/app/services/assistant/enhanced_rag.py) | `.py` | `RAG_ORCHESTRATION` | `source` | **A+** | **YES** | Multi-stage RAG orchestrator coordinating retrieval, prompt assembly, claim checking, and citations. |
| [`backend/app/services/assistant/iterative_rag.py`](backend/app/services/assistant/iterative_rag.py) | `.py` | `RAG_ORCHESTRATION` | `source` | **A+** | **YES** | Iterative multi-turn retrieval and refinement loop managing feedback-driven re-querying. |
| [`backend/app/services/assistant/synthesis_engine.py`](backend/app/services/assistant/synthesis_engine.py) | `.py` | `GENERATION_LLM` | `source` | **A+** | **YES** | Scientific synthesis generator constructing multi-paper summaries and structured analyses. |
| [`backend/app/services/llm_provider.py`](backend/app/services/llm_provider.py) | `.py` | `GENERATION_LLM` | `source` | **A+** | **YES** | Multi-provider LLM interface (Groq, Gemini, OpenAI, Claude) with fallback and prompt caching. |
| [`backend/app/services/local_evidence.py`](backend/app/services/local_evidence.py) | `.py` | `RETRIEVAL` | `source` | **A+** | **YES** | Local corpus retrieval engine with cached indexes, token cleaning, and dense embedding matching. |
| [`backend/app/services/retrieval.py`](backend/app/services/retrieval.py) | `.py` | `RETRIEVAL` | `source` | **A+** | **YES** | Dual BM25 + ChromaDB dense retrieval, Reciprocal Rank Fusion (RRF), and BGE reranker scoring. |
| [`build_indexes.py`](build_indexes.py) | `.py` | `DATA_INGESTION` | `source` | **A+** | **YES** | Offline pipeline script to build indexes. |
| [`chunk_corpus.py`](chunk_corpus.py) | `.py` | `DATA_INGESTION` | `source` | **A+** | **YES** | Offline pipeline script to chunk corpus. |
| [`embed_corpus.py`](embed_corpus.py) | `.py` | `DATA_INGESTION` | `source` | **A+** | **YES** | Offline pipeline script to embed corpus. |
| [`evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py`](evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py) | `.py` | `EVALUATION` | `source` | **A+** | **YES** | Authoritative V4 canonical reconciliation reproduction script. |
| [`src/App.tsx`](src/App.tsx) | `.tsx` | `FRONTEND_ENTRY` | `source` | **A+** | **YES** | Root React routing configuration, theme layout providers, and navigation shell. |
| [`src/pages/AssistantPage.tsx`](src/pages/AssistantPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A+** | **YES** | Primary user-facing view for AssistantPage. |
| [`src/pages/HybridSearchPage.tsx`](src/pages/HybridSearchPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A+** | **YES** | Primary user-facing view for HybridSearchPage. |
| [`src/pages/LiteratureReviewPage.tsx`](src/pages/LiteratureReviewPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A+** | **YES** | Primary user-facing view for LiteratureReviewPage. |
| [`src/pages/XaiPage.tsx`](src/pages/XaiPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A+** | **YES** | Primary user-facing view for XaiPage. |
| [`src/utils/api.ts`](src/utils/api.ts) | `.ts` | `FRONTEND_API_SERVICES` | `source` | **A+** | **YES** | Core frontend HTTP client providing typed calls to backend FastAPI endpoints. |
| [`backend/app/api/evaluation.py`](backend/app/api/evaluation.py) | `.py` | `API` | `source` | **A** | **YES** | API endpoint handler for evaluation. |
| [`backend/app/api/knowledge_base.py`](backend/app/api/knowledge_base.py) | `.py` | `API` | `source` | **A** | **YES** | API endpoint handler for knowledge base. |
| [`backend/app/api/literature_review.py`](backend/app/api/literature_review.py) | `.py` | `API` | `source` | **A** | **YES** | API endpoint handler for literature review. |
| [`backend/app/api/search_history.py`](backend/app/api/search_history.py) | `.py` | `API` | `source` | **A** | **YES** | API endpoint handler for search history. |
| [`backend/app/core/config.py`](backend/app/core/config.py) | `.py` | `CONFIGURATION` | `source` | **A** | **YES** | Backend application core configuration config.py. |
| [`backend/app/db/session.py`](backend/app/db/session.py) | `.py` | `DATABASE` | `source` | **A** | **YES** | SQLAlchemy model / session manager for session. |
| [`backend/app/models/document.py`](backend/app/models/document.py) | `.py` | `DATABASE` | `source` | **A** | **YES** | SQLAlchemy model / session manager for document. |
| [`backend/app/models/search_history.py`](backend/app/models/search_history.py) | `.py` | `DATABASE` | `source` | **A** | **YES** | SQLAlchemy model / session manager for search_history. |
| [`backend/app/models/session.py`](backend/app/models/session.py) | `.py` | `DATABASE` | `source` | **A** | **YES** | SQLAlchemy model / session manager for session. |
| [`backend/app/models/workspace.py`](backend/app/models/workspace.py) | `.py` | `DATABASE` | `source` | **A** | **YES** | SQLAlchemy model / session manager for workspace. |
| [`backend/app/services/assistant/claim_extractor.py`](backend/app/services/assistant/claim_extractor.py) | `.py` | `CLAIM_VERIFICATION` | `source` | **A** | **YES** | Supporting verification component for claim extractor. |
| [`backend/app/services/assistant/contradiction_detector.py`](backend/app/services/assistant/contradiction_detector.py) | `.py` | `CLAIM_VERIFICATION` | `source` | **A** | **YES** | Supporting verification component for contradiction detector. |
| [`backend/app/services/assistant/eligibility.py`](backend/app/services/assistant/eligibility.py) | `.py` | `CLAIM_VERIFICATION` | `source` | **A** | **YES** | Supporting verification component for eligibility. |
| [`backend/app/services/assistant/gap_analyzer.py`](backend/app/services/assistant/gap_analyzer.py) | `.py` | `CITATION_PROVENANCE_XAI` | `source` | **A** | **YES** | Provenance and explanation service for gap analyzer. |
| [`backend/app/services/assistant/synthesis_extractor.py`](backend/app/services/assistant/synthesis_extractor.py) | `.py` | `CITATION_PROVENANCE_XAI` | `source` | **A** | **YES** | Provenance and explanation service for synthesis extractor. |
| [`backend/app/services/research_artifact_service.py`](backend/app/services/research_artifact_service.py) | `.py` | `CITATION_PROVENANCE_XAI` | `source` | **A** | **YES** | Provenance and explanation service for research artifact service. |
| [`backend/app/services/research_memory_service.py`](backend/app/services/research_memory_service.py) | `.py` | `CITATION_PROVENANCE_XAI` | `source` | **A** | **YES** | Provenance and explanation service for research memory service. |
| [`evidence_layer.py`](evidence_layer.py) | `.py` | `RETRIEVAL` | `source` | **A** | **YES** | Standalone retrieval and evidence scoring script evidence_layer.py. |
| [`hybrid_retriever.py`](hybrid_retriever.py) | `.py` | `RETRIEVAL` | `source` | **A** | **YES** | Standalone retrieval and evidence scoring script hybrid_retriever.py. |
| [`run_e04_eval.py`](run_e04_eval.py) | `.py` | `EVALUATION` | `source` | **A** | **YES** | Benchmark runner script executing run_e04_eval. |
| [`run_e05_eval.py`](run_e05_eval.py) | `.py` | `EVALUATION` | `source` | **A** | **YES** | Benchmark runner script executing run_e05_eval. |
| [`run_e07_authoritative.py`](run_e07_authoritative.py) | `.py` | `EVALUATION` | `source` | **A** | **YES** | Benchmark runner script executing run_e07_authoritative. |
| [`run_e08_xai_evaluation.py`](run_e08_xai_evaluation.py) | `.py` | `EVALUATION` | `source` | **A** | **YES** | Benchmark runner script executing run_e08_xai_evaluation. |
| [`run_e10_ablation_study.py`](run_e10_ablation_study.py) | `.py` | `EVALUATION` | `source` | **A** | **YES** | Benchmark runner script executing run_e10_ablation_study. |
| [`run_e11_reconciled.py`](run_e11_reconciled.py) | `.py` | `EVALUATION` | `source` | **A** | **YES** | Benchmark runner script executing run_e11_reconciled. |
| [`src/components/assistant/ClaimProofDrawer.tsx`](src/components/assistant/ClaimProofDrawer.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | **A** | **YES** | Reusable UI component for ClaimProofDrawer. |
| [`src/components/research/PaperCard.tsx`](src/components/research/PaperCard.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | **A** | **YES** | Reusable UI component for PaperCard. |
| [`src/main.tsx`](src/main.tsx) | `.tsx` | `FRONTEND_ENTRY` | `source` | **A** | Maybe | ReactDOM root mount and top-level provider wrapping. |
| [`src/pages/AnalyticsPage.tsx`](src/pages/AnalyticsPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A** | **YES** | Secondary management view for AnalyticsPage. |
| [`src/pages/ComparisonPage.tsx`](src/pages/ComparisonPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A** | **YES** | Secondary management view for ComparisonPage. |
| [`src/pages/DashboardPage.tsx`](src/pages/DashboardPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A** | **YES** | Secondary management view for DashboardPage. |
| [`src/pages/PaperReaderPage.tsx`](src/pages/PaperReaderPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A** | **YES** | Secondary management view for PaperReaderPage. |
| [`src/pages/ResearchPage.tsx`](src/pages/ResearchPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | **A** | **YES** | Secondary management view for ResearchPage. |
| [`src/store/authStore.ts`](src/store/authStore.ts) | `.ts` | `FRONTEND_STATE` | `source` | **A** | **YES** | State store slice for authStore. |
| [`src/store/overlayStore.ts`](src/store/overlayStore.ts) | `.ts` | `FRONTEND_STATE` | `source` | **A** | **YES** | State store slice for overlayStore. |
| [`src/store/researchSessionStore.ts`](src/store/researchSessionStore.ts) | `.ts` | `FRONTEND_STATE` | `source` | **A** | **YES** | State store slice for researchSessionStore. |
| [`src/store/themeStore.ts`](src/store/themeStore.ts) | `.ts` | `FRONTEND_STATE` | `source` | **A** | **YES** | State store slice for themeStore. |
| [`src/store/tipStore.ts`](src/store/tipStore.ts) | `.ts` | `FRONTEND_STATE` | `source` | **A** | **YES** | State store slice for tipStore. |
| [`src/store/toastStore.ts`](src/store/toastStore.ts) | `.ts` | `FRONTEND_STATE` | `source` | **A** | **YES** | State store slice for toastStore. |
| [`src/utils/apiAdapter.ts`](src/utils/apiAdapter.ts) | `.ts` | `FRONTEND_API_SERVICES` | `source` | **A** | **YES** | Core frontend HTTP client providing typed calls to backend FastAPI endpoints. |
| [`backend/alembic/env.py`](backend/alembic/env.py) | `.py` | `DATABASE` | `source` | B | No | Database migration scripts and secondary ORM models. |
| [`backend/alembic/versions/77773a740595_add_project_papers_table.py`](backend/alembic/versions/77773a740595_add_project_papers_table.py) | `.py` | `DATABASE` | `source` | B | No | Database migration scripts and secondary ORM models. |
| [`backend/app/api/__init__.py`](backend/app/api/__init__.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for __init__. |
| [`backend/app/api/analytics.py`](backend/app/api/analytics.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for analytics. |
| [`backend/app/api/auth.py`](backend/app/api/auth.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for auth. |
| [`backend/app/api/bookmarks.py`](backend/app/api/bookmarks.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for bookmarks. |
| [`backend/app/api/dashboard.py`](backend/app/api/dashboard.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for dashboard. |
| [`backend/app/api/documents.py`](backend/app/api/documents.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for documents. |
| [`backend/app/api/goals.py`](backend/app/api/goals.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for goals. |
| [`backend/app/api/notes.py`](backend/app/api/notes.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for notes. |
| [`backend/app/api/projects.py`](backend/app/api/projects.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for projects. |
| [`backend/app/api/toolkit.py`](backend/app/api/toolkit.py) | `.py` | `API` | `source` | B | Maybe | Supporting API endpoint module for toolkit. |
| [`backend/app/core/domains.py`](backend/app/core/domains.py) | `.py` | `CONFIGURATION` | `source` | B | Maybe | Backend application core configuration domains.py. |
| [`backend/app/core/security.py`](backend/app/core/security.py) | `.py` | `AUTHENTICATION_SECURITY` | `source` | B | Maybe | JWT token creation, password hashing, and user authentication handlers. |
| [`backend/app/models/__init__.py`](backend/app/models/__init__.py) | `.py` | `DATABASE` | `source` | B | No | Database migration scripts and secondary ORM models. |
| [`backend/app/models/evaluation.py`](backend/app/models/evaluation.py) | `.py` | `DATABASE` | `source` | B | No | Database migration scripts and secondary ORM models. |
| [`backend/app/models/search_experiment.py`](backend/app/models/search_experiment.py) | `.py` | `DATABASE` | `source` | B | No | Database migration scripts and secondary ORM models. |
| [`backend/app/models/user.py`](backend/app/models/user.py) | `.py` | `DATABASE` | `source` | B | No | Database migration scripts and secondary ORM models. |
| [`backend/app/scripts/alter_papers.py`](backend/app/scripts/alter_papers.py) | `.py` | `UTILITY` | `source` | B | No | Backend maintenance script alter_papers.py. |
| [`backend/app/scripts/create_search_experiment_table.py`](backend/app/scripts/create_search_experiment_table.py) | `.py` | `UTILITY` | `source` | B | No | Backend maintenance script create_search_experiment_table.py. |
| [`backend/app/scripts/ingest_local_kb.py`](backend/app/scripts/ingest_local_kb.py) | `.py` | `DATA_INGESTION` | `source` | B | No | Backend maintenance script ingest_local_kb.py. |
| [`backend/app/scripts/seed_benchmark_v10.py`](backend/app/scripts/seed_benchmark_v10.py) | `.py` | `DATA_INGESTION` | `source` | B | No | Backend maintenance script seed_benchmark_v10.py. |
| [`backend/app/services/assistant/__init__.py`](backend/app/services/assistant/__init__.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for __init__. |
| [`backend/app/services/assistant/comparison_engine.py`](backend/app/services/assistant/comparison_engine.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for comparison_engine. |
| [`backend/app/services/assistant/comparison_extractor.py`](backend/app/services/assistant/comparison_extractor.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for comparison_extractor. |
| [`backend/app/services/assistant/context_manager.py`](backend/app/services/assistant/context_manager.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for context_manager. |
| [`backend/app/services/assistant/metrics.py`](backend/app/services/assistant/metrics.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for metrics. |
| [`backend/app/services/assistant/models.py`](backend/app/services/assistant/models.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for models. |
| [`backend/app/services/assistant/refinement_query.py`](backend/app/services/assistant/refinement_query.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for refinement_query. |
| [`backend/app/services/assistant/self_feedback.py`](backend/app/services/assistant/self_feedback.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for self_feedback. |
| [`backend/app/services/assistant/session_manager.py`](backend/app/services/assistant/session_manager.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for session_manager. |
| [`backend/app/services/connectors/__init__.py`](backend/app/services/connectors/__init__.py) | `.py` | `RETRIEVAL` | `source` | B | Maybe | External literature API connector for __init__. |
| [`backend/app/services/connectors/arxiv_connector.py`](backend/app/services/connectors/arxiv_connector.py) | `.py` | `RETRIEVAL` | `source` | B | Maybe | External literature API connector for arxiv_connector. |
| [`backend/app/services/connectors/base.py`](backend/app/services/connectors/base.py) | `.py` | `RETRIEVAL` | `source` | B | Maybe | External literature API connector for base. |
| [`backend/app/services/connectors/crossref_connector.py`](backend/app/services/connectors/crossref_connector.py) | `.py` | `RETRIEVAL` | `source` | B | Maybe | External literature API connector for crossref_connector. |
| [`backend/app/services/connectors/nasa_ads_connector.py`](backend/app/services/connectors/nasa_ads_connector.py) | `.py` | `RETRIEVAL` | `source` | B | Maybe | External literature API connector for nasa_ads_connector. |
| [`backend/app/services/connectors/openalex_connector.py`](backend/app/services/connectors/openalex_connector.py) | `.py` | `RETRIEVAL` | `source` | B | Maybe | External literature API connector for openalex_connector. |
| [`backend/app/services/connectors/pmc_connector.py`](backend/app/services/connectors/pmc_connector.py) | `.py` | `RETRIEVAL` | `source` | B | Maybe | External literature API connector for pmc_connector. |
| [`backend/app/services/connectors/router.py`](backend/app/services/connectors/router.py) | `.py` | `RETRIEVAL` | `source` | B | Maybe | External literature API connector for router. |
| [`backend/app/services/document_processing.py`](backend/app/services/document_processing.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for document_processing. |
| [`backend/app/services/document_service.py`](backend/app/services/document_service.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for document_service. |
| [`backend/app/services/evaluation_service.py`](backend/app/services/evaluation_service.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for evaluation_service. |
| [`backend/app/services/ingestion.py`](backend/app/services/ingestion.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for ingestion. |
| [`backend/app/services/research_session_service.py`](backend/app/services/research_session_service.py) | `.py` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for research_session_service. |
| [`backend/app/tests/test_claim_verification.py`](backend/app/tests/test_claim_verification.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_claim_verification.py. |
| [`backend/app/tests/test_comparison_engine.py`](backend/app/tests/test_comparison_engine.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_comparison_engine.py. |
| [`backend/app/tests/test_context_engine.py`](backend/app/tests/test_context_engine.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_context_engine.py. |
| [`backend/app/tests/test_e02_bge_reranking.py`](backend/app/tests/test_e02_bge_reranking.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_e02_bge_reranking.py. |
| [`backend/app/tests/test_e03_enhanced_rag.py`](backend/app/tests/test_e03_enhanced_rag.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_e03_enhanced_rag.py. |
| [`backend/app/tests/test_e04_claim_verification.py`](backend/app/tests/test_e04_claim_verification.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_e04_claim_verification.py. |
| [`backend/app/tests/test_e05_iterative_refinement.py`](backend/app/tests/test_e05_iterative_refinement.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_e05_iterative_refinement.py. |
| [`backend/app/tests/test_enhanced_rag.py`](backend/app/tests/test_enhanced_rag.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_enhanced_rag.py. |
| [`backend/app/tests/test_evaluation_console.py`](backend/app/tests/test_evaluation_console.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_evaluation_console.py. |
| [`backend/app/tests/test_iterative_refinement.py`](backend/app/tests/test_iterative_refinement.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_iterative_refinement.py. |
| [`backend/app/tests/test_personal_corpus.py`](backend/app/tests/test_personal_corpus.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_personal_corpus.py. |
| [`backend/app/tests/test_research_sessions.py`](backend/app/tests/test_research_sessions.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_research_sessions.py. |
| [`backend/app/tests/test_synthesis_engine.py`](backend/app/tests/test_synthesis_engine.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_synthesis_engine.py. |
| [`backend/migrate_profile.py`](backend/migrate_profile.py) | `.py` | `DATABASE` | `source` | B | No | Database migration scripts and secondary ORM models. |
| [`backend/run_server.py`](backend/run_server.py) | `.py` | `BACKEND_ENTRY` | `source` | B | No | Uvicorn runner script to launch the FastAPI backend server. |
| [`backend/scripts/generate_toolkit_data.py`](backend/scripts/generate_toolkit_data.py) | `.py` | `UTILITY` | `source` | B | No | Backend maintenance script generate_toolkit_data.py. |
| [`backend/test_ai.py`](backend/test_ai.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_ai.py. |
| [`backend/test_db.py`](backend/test_db.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_db.py. |
| [`backend/test_diagnostic.py`](backend/test_diagnostic.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_diagnostic.py. |
| [`backend/test_e2e_full_verification.py`](backend/test_e2e_full_verification.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_e2e_full_verification.py. |
| [`backend/test_e2e_real_runtime.py`](backend/test_e2e_real_runtime.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_e2e_real_runtime.py. |
| [`backend/test_live_api.py`](backend/test_live_api.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_live_api.py. |
| [`backend/test_openalex.py`](backend/test_openalex.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_openalex.py. |
| [`backend/test_pipeline.py`](backend/test_pipeline.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_pipeline.py. |
| [`backend/test_retrieve.py`](backend/test_retrieve.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_retrieve.py. |
| [`backend/verify_auth.py`](backend/verify_auth.py) | `.py` | `AUTHENTICATION_SECURITY` | `source` | B | Maybe | JWT token creation, password hashing, and user authentication handlers. |
| [`evaluation/Re-evaluation of mistakes/canonical_benchmark_manifest.json`](evaluation/Re-evaluation of mistakes/canonical_benchmark_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file canonical_benchmark_manifest.json. |
| [`evaluation/Re-evaluation of mistakes/canonical_grounding_metrics.json`](evaluation/Re-evaluation of mistakes/canonical_grounding_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file canonical_grounding_metrics.json. |
| [`evaluation/module_01/benchmark_manifest.json`](evaluation/module_01/benchmark_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file benchmark_manifest.json. |
| [`evaluation/module_01/consistency/consistency_audit.json`](evaluation/module_01/consistency/consistency_audit.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file consistency_audit.json. |
| [`evaluation/module_01/error_analysis/error_cases.json`](evaluation/module_01/error_analysis/error_cases.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file error_cases.json. |
| [`evaluation/module_01/latency/latency_summary.json`](evaluation/module_01/latency/latency_summary.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file latency_summary.json. |
| [`evaluation/module_01/metrics/evidence_level_metrics.json`](evaluation/module_01/metrics/evidence_level_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file evidence_level_metrics.json. |
| [`evaluation/module_01/metrics/paper_level_metrics.json`](evaluation/module_01/metrics/paper_level_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file paper_level_metrics.json. |
| [`evaluation/module_01/run_manifest.json`](evaluation/module_01/run_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file run_manifest.json. |
| [`evaluation/module_01/statistics/statistical_tests.json`](evaluation/module_01/statistics/statistical_tests.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file statistical_tests.json. |
| [`evaluation/module_01/unit_tests/test_rrf.py`](evaluation/module_01/unit_tests/test_rrf.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_rrf.py. |
| [`evaluation/module_02/consistency/consistency_audit.json`](evaluation/module_02/consistency/consistency_audit.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file consistency_audit.json. |
| [`evaluation/module_02/context_snapshots/all_test_snapshots.json`](evaluation/module_02/context_snapshots/all_test_snapshots.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file all_test_snapshots.json. |
| [`evaluation/module_02/context_snapshots/item_v11_086_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_086_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_086_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_087_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_087_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_087_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_088_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_088_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_088_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_089_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_089_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_089_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_090_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_090_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_090_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_091_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_091_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_091_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_092_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_092_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_092_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_093_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_093_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_093_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_094_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_094_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_094_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_095_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_095_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_095_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_096_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_096_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_096_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_097_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_097_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_097_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_098_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_098_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_098_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_099_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_099_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_099_snapshot.json. |
| [`evaluation/module_02/context_snapshots/item_v11_100_snapshot.json`](evaluation/module_02/context_snapshots/item_v11_100_snapshot.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_100_snapshot.json. |
| [`evaluation/module_02/error_analysis/error_analysis.json`](evaluation/module_02/error_analysis/error_analysis.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file error_analysis.json. |
| [`evaluation/module_02/fairness/fairness_audit.json`](evaluation/module_02/fairness/fairness_audit.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file fairness_audit.json. |
| [`evaluation/module_02/latency/latency_metrics.json`](evaluation/module_02/latency/latency_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file latency_metrics.json. |
| [`evaluation/module_02/metrics/aggregate_metrics.json`](evaluation/module_02/metrics/aggregate_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file aggregate_metrics.json. |
| [`evaluation/module_02/per_query/all_per_query_results.json`](evaluation/module_02/per_query/all_per_query_results.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file all_per_query_results.json. |
| [`evaluation/module_02/per_query/item_v11_086.json`](evaluation/module_02/per_query/item_v11_086.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_086.json. |
| [`evaluation/module_02/per_query/item_v11_087.json`](evaluation/module_02/per_query/item_v11_087.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_087.json. |
| [`evaluation/module_02/per_query/item_v11_088.json`](evaluation/module_02/per_query/item_v11_088.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_088.json. |
| [`evaluation/module_02/per_query/item_v11_089.json`](evaluation/module_02/per_query/item_v11_089.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_089.json. |
| [`evaluation/module_02/per_query/item_v11_090.json`](evaluation/module_02/per_query/item_v11_090.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_090.json. |
| [`evaluation/module_02/per_query/item_v11_091.json`](evaluation/module_02/per_query/item_v11_091.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_091.json. |
| [`evaluation/module_02/per_query/item_v11_092.json`](evaluation/module_02/per_query/item_v11_092.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_092.json. |
| [`evaluation/module_02/per_query/item_v11_093.json`](evaluation/module_02/per_query/item_v11_093.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_093.json. |
| [`evaluation/module_02/per_query/item_v11_094.json`](evaluation/module_02/per_query/item_v11_094.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_094.json. |
| [`evaluation/module_02/per_query/item_v11_095.json`](evaluation/module_02/per_query/item_v11_095.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_095.json. |
| [`evaluation/module_02/per_query/item_v11_096.json`](evaluation/module_02/per_query/item_v11_096.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_096.json. |
| [`evaluation/module_02/per_query/item_v11_097.json`](evaluation/module_02/per_query/item_v11_097.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_097.json. |
| [`evaluation/module_02/per_query/item_v11_098.json`](evaluation/module_02/per_query/item_v11_098.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_098.json. |
| [`evaluation/module_02/per_query/item_v11_099.json`](evaluation/module_02/per_query/item_v11_099.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_099.json. |
| [`evaluation/module_02/per_query/item_v11_100.json`](evaluation/module_02/per_query/item_v11_100.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file item_v11_100.json. |
| [`evaluation/module_02/raw/citations_raw.json`](evaluation/module_02/raw/citations_raw.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file citations_raw.json. |
| [`evaluation/module_02/raw/claims_raw.json`](evaluation/module_02/raw/claims_raw.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file claims_raw.json. |
| [`evaluation/module_02/raw/condition_a_naive_raw.json`](evaluation/module_02/raw/condition_a_naive_raw.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file condition_a_naive_raw.json. |
| [`evaluation/module_02/raw/condition_b_verified_raw.json`](evaluation/module_02/raw/condition_b_verified_raw.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file condition_b_verified_raw.json. |
| [`evaluation/module_02/revision_01/consistency_recheck.json`](evaluation/module_02/revision_01/consistency_recheck.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file consistency_recheck.json. |
| [`evaluation/module_02/revision_01/corrected_metrics.json`](evaluation/module_02/revision_01/corrected_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file corrected_metrics.json. |
| [`evaluation/module_02/revision_01/corrected_statistics.json`](evaluation/module_02/revision_01/corrected_statistics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file corrected_statistics.json. |
| [`evaluation/module_02/revision_01/fairness_recheck.json`](evaluation/module_02/revision_01/fairness_recheck.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file fairness_recheck.json. |
| [`evaluation/module_02/revision_01/human_annotation/annotation_template.json`](evaluation/module_02/revision_01/human_annotation/annotation_template.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file annotation_template.json. |
| [`evaluation/module_02/revision_01/human_annotation/sample_selection.json`](evaluation/module_02/revision_01/human_annotation/sample_selection.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file sample_selection.json. |
| [`evaluation/module_02/revision_01/latency_reanalysis.json`](evaluation/module_02/revision_01/latency_reanalysis.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file latency_reanalysis.json. |
| [`evaluation/module_02/revision_01/reclassified_claims.json`](evaluation/module_02/revision_01/reclassified_claims.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file reclassified_claims.json. |
| [`evaluation/module_02/revision_01/taxonomy_audit_56_claims.json`](evaluation/module_02/revision_01/taxonomy_audit_56_claims.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file taxonomy_audit_56_claims.json. |
| [`evaluation/module_02/run_manifest.json`](evaluation/module_02/run_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file run_manifest.json. |
| [`evaluation/module_02/statistics/statistical_tests.json`](evaluation/module_02/statistics/statistical_tests.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file statistical_tests.json. |
| [`evaluation/module_03/analysis/citation_metrics.json`](evaluation/module_03/analysis/citation_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file citation_metrics.json. |
| [`evaluation/module_03/analysis/latency_metrics.json`](evaluation/module_03/analysis/latency_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file latency_metrics.json. |
| [`evaluation/module_03/analysis/provenance_metrics.json`](evaluation/module_03/analysis/provenance_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file provenance_metrics.json. |
| [`evaluation/module_03/analysis/repair_metrics.json`](evaluation/module_03/analysis/repair_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file repair_metrics.json. |
| [`evaluation/module_03/analysis/statistical_results.json`](evaluation/module_03/analysis/statistical_results.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file statistical_results.json. |
| [`evaluation/module_03/benchmark_manifest.json`](evaluation/module_03/benchmark_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file benchmark_manifest.json. |
| [`evaluation/module_03/consistency/consistency_audit.json`](evaluation/module_03/consistency/consistency_audit.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file consistency_audit.json. |
| [`evaluation/module_03/fairness/fairness_audit.json`](evaluation/module_03/fairness/fairness_audit.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file fairness_audit.json. |
| [`evaluation/module_03/fairness/fairness_manifest.json`](evaluation/module_03/fairness/fairness_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file fairness_manifest.json. |
| [`evaluation/module_03/human_annotation/annotation_template.json`](evaluation/module_03/human_annotation/annotation_template.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file annotation_template.json. |
| [`evaluation/module_03/human_annotation/sample_selection.json`](evaluation/module_03/human_annotation/sample_selection.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file sample_selection.json. |
| [`evaluation/module_03/raw/citation_units.json`](evaluation/module_03/raw/citation_units.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file citation_units.json. |
| [`evaluation/module_03/raw/claim_units.json`](evaluation/module_03/raw/claim_units.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file claim_units.json. |
| [`evaluation/module_03/raw/latency_records.json`](evaluation/module_03/raw/latency_records.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file latency_records.json. |
| [`evaluation/module_03/raw/provenance_units.json`](evaluation/module_03/raw/provenance_units.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file provenance_units.json. |
| [`evaluation/module_03/raw/repair_units.json`](evaluation/module_03/raw/repair_units.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file repair_units.json. |
| [`evaluation/publication_audit_v2/experiment_manifest.json`](evaluation/publication_audit_v2/experiment_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file experiment_manifest.json. |
| [`evaluation/publication_audit_v2/forensic_validation_v3/validated_results_v3.json`](evaluation/publication_audit_v2/forensic_validation_v3/validated_results_v3.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file validated_results_v3.json. |
| [`evaluation/publication_audit_v2/p1_grounding_human/human_annotation_package/blinded_30_item_sample.json`](evaluation/publication_audit_v2/p1_grounding_human/human_annotation_package/blinded_30_item_sample.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file blinded_30_item_sample.json. |
| [`evaluation/publication_audit_v2/p4_freeze_reproducibility/corrected_results_master.json`](evaluation/publication_audit_v2/p4_freeze_reproducibility/corrected_results_master.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file corrected_results_master.json. |
| [`evaluation/publication_audit_v2/v4_reconciliation/ResearchNexusAI_V4_Paper_Update/canonical_benchmark_manifest.json`](evaluation/publication_audit_v2/v4_reconciliation/ResearchNexusAI_V4_Paper_Update/canonical_benchmark_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file canonical_benchmark_manifest.json. |
| [`evaluation/publication_audit_v2/v4_reconciliation/ResearchNexusAI_V4_Paper_Update/canonical_grounding_metrics.json`](evaluation/publication_audit_v2/v4_reconciliation/ResearchNexusAI_V4_Paper_Update/canonical_grounding_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file canonical_grounding_metrics.json. |
| [`evaluation/publication_audit_v2/v4_reconciliation/canonical_benchmark_manifest.json`](evaluation/publication_audit_v2/v4_reconciliation/canonical_benchmark_manifest.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file canonical_benchmark_manifest.json. |
| [`evaluation/publication_audit_v2/v4_reconciliation/canonical_grounding_metrics.json`](evaluation/publication_audit_v2/v4_reconciliation/canonical_grounding_metrics.json) | `.json` | `EVALUATION` | `reference` | B | No | Canonical benchmark or evaluation data file canonical_grounding_metrics.json. |
| [`package.json`](package.json) | `.json` | `CONFIGURATION` | `source` | B | No | Root build and dependency configuration package.json. |
| [`research_artifacts/benchmark_v11/test_manifest.json`](research_artifacts/benchmark_v11/test_manifest.json) | `.json` | `TESTS` | `source` | B | No | Automated test module test_manifest.json. |
| [`scratch/test_dense_bge_live.py`](scratch/test_dense_bge_live.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_dense_bge_live.py. |
| [`scratch/test_retrieval_flow.py`](scratch/test_retrieval_flow.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_retrieval_flow.py. |
| [`scratch/test_verifier_stage_a.py`](scratch/test_verifier_stage_a.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_verifier_stage_a.py. |
| [`scratch/test_verifier_stage_a_correct.py`](scratch/test_verifier_stage_a_correct.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_verifier_stage_a_correct.py. |
| [`scripts/run_module1_evaluations.py`](scripts/run_module1_evaluations.py) | `.py` | `UTILITY` | `source` | B | No | Backend maintenance script run_module1_evaluations.py. |
| [`src/__tests__/assistant_validation.test.ts`](src/__tests__/assistant_validation.test.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module assistant_validation.test.ts. |
| [`src/__tests__/assistant_workflow_validation.ts`](src/__tests__/assistant_workflow_validation.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module assistant_workflow_validation.ts. |
| [`src/__tests__/comparison_validation.test.ts`](src/__tests__/comparison_validation.test.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module comparison_validation.test.ts. |
| [`src/__tests__/evaluation_console_validation.test.ts`](src/__tests__/evaluation_console_validation.test.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module evaluation_console_validation.test.ts. |
| [`src/__tests__/research_session_validation.test.ts`](src/__tests__/research_session_validation.test.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module research_session_validation.test.ts. |
| [`src/__tests__/search_flow_validation.test.ts`](src/__tests__/search_flow_validation.test.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module search_flow_validation.test.ts. |
| [`src/__tests__/search_flow_validation.ts`](src/__tests__/search_flow_validation.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module search_flow_validation.ts. |
| [`src/__tests__/synthesis_validation.test.ts`](src/__tests__/synthesis_validation.test.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module synthesis_validation.test.ts. |
| [`src/__tests__/upload_validation.test.ts`](src/__tests__/upload_validation.test.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module upload_validation.test.ts. |
| [`src/__tests__/xai_validation.test.ts`](src/__tests__/xai_validation.test.ts) | `.ts` | `TESTS` | `source` | B | No | Automated test module xai_validation.test.ts. |
| [`src/components/CommandPalette.tsx`](src/components/CommandPalette.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for CommandPalette. |
| [`src/components/ContextualTip.tsx`](src/components/ContextualTip.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ContextualTip. |
| [`src/components/CurrentResearchBar.tsx`](src/components/CurrentResearchBar.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for CurrentResearchBar. |
| [`src/components/DomainHeroBackgrounds.tsx`](src/components/DomainHeroBackgrounds.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for DomainHeroBackgrounds. |
| [`src/components/ExperimentOverallStatus.tsx`](src/components/ExperimentOverallStatus.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ExperimentOverallStatus. |
| [`src/components/LocalProgressPanel.tsx`](src/components/LocalProgressPanel.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for LocalProgressPanel. |
| [`src/components/OnlineProgressPanel.tsx`](src/components/OnlineProgressPanel.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for OnlineProgressPanel. |
| [`src/components/ResearchAtmosphere.tsx`](src/components/ResearchAtmosphere.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchAtmosphere. |
| [`src/components/ThemeToggle.tsx`](src/components/ThemeToggle.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ThemeToggle. |
| [`src/components/ToastContainer.tsx`](src/components/ToastContainer.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ToastContainer. |
| [`src/components/assistant/AskWorkspace.tsx`](src/components/assistant/AskWorkspace.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for AskWorkspace. |
| [`src/components/assistant/AssistantEmptyState.tsx`](src/components/assistant/AssistantEmptyState.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for AssistantEmptyState. |
| [`src/components/assistant/AssistantLanding.tsx`](src/components/assistant/AssistantLanding.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for AssistantLanding. |
| [`src/components/assistant/AssistantModeTabs.tsx`](src/components/assistant/AssistantModeTabs.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for AssistantModeTabs. |
| [`src/components/assistant/Breadcrumb.tsx`](src/components/assistant/Breadcrumb.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for Breadcrumb. |
| [`src/components/assistant/CompareTable.tsx`](src/components/assistant/CompareTable.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for CompareTable. |
| [`src/components/assistant/CompareWorkspace.tsx`](src/components/assistant/CompareWorkspace.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for CompareWorkspace. |
| [`src/components/assistant/ComparisonModalOverlay.tsx`](src/components/assistant/ComparisonModalOverlay.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ComparisonModalOverlay. |
| [`src/components/assistant/ContextInspector.tsx`](src/components/assistant/ContextInspector.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ContextInspector. |
| [`src/components/assistant/EvidenceCard.tsx`](src/components/assistant/EvidenceCard.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for EvidenceCard. |
| [`src/components/assistant/EvidencePreview.tsx`](src/components/assistant/EvidencePreview.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for EvidencePreview. |
| [`src/components/assistant/ExplorePapersWorkspace.tsx`](src/components/assistant/ExplorePapersWorkspace.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ExplorePapersWorkspace. |
| [`src/components/assistant/KeyFindingCard.tsx`](src/components/assistant/KeyFindingCard.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for KeyFindingCard. |
| [`src/components/assistant/PaperInspector.tsx`](src/components/assistant/PaperInspector.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for PaperInspector. |
| [`src/components/assistant/PersonalResearchCorpus.tsx`](src/components/assistant/PersonalResearchCorpus.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for PersonalResearchCorpus. |
| [`src/components/assistant/ProveWorkspace.tsx`](src/components/assistant/ProveWorkspace.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ProveWorkspace. |
| [`src/components/assistant/RefineWorkspace.tsx`](src/components/assistant/RefineWorkspace.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for RefineWorkspace. |
| [`src/components/assistant/RefinementInspector.tsx`](src/components/assistant/RefinementInspector.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for RefinementInspector. |
| [`src/components/assistant/RefinementModeSelector.tsx`](src/components/assistant/RefinementModeSelector.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for RefinementModeSelector. |
| [`src/components/assistant/ResearchComposer.tsx`](src/components/assistant/ResearchComposer.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchComposer. |
| [`src/components/assistant/ResearchContextPanel.tsx`](src/components/assistant/ResearchContextPanel.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchContextPanel. |
| [`src/components/assistant/ResearchScopeSelector.tsx`](src/components/assistant/ResearchScopeSelector.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchScopeSelector. |
| [`src/components/assistant/SynthesisWorkspace.tsx`](src/components/assistant/SynthesisWorkspace.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for SynthesisWorkspace. |
| [`src/components/evaluation/AblationView.tsx`](src/components/evaluation/AblationView.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for AblationView. |
| [`src/components/evaluation/ErrorAnalysisWorkspace.tsx`](src/components/evaluation/ErrorAnalysisWorkspace.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ErrorAnalysisWorkspace. |
| [`src/components/evaluation/EvaluationConsole.tsx`](src/components/evaluation/EvaluationConsole.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for EvaluationConsole. |
| [`src/components/evaluation/ExperimentRunner.tsx`](src/components/evaluation/ExperimentRunner.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ExperimentRunner. |
| [`src/components/evaluation/HumanEvalPanel.tsx`](src/components/evaluation/HumanEvalPanel.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for HumanEvalPanel. |
| [`src/components/evaluation/PublicationTables.tsx`](src/components/evaluation/PublicationTables.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for PublicationTables. |
| [`src/components/layout/WorkspaceLayout.tsx`](src/components/layout/WorkspaceLayout.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for WorkspaceLayout. |
| [`src/components/research/LocalRetrievalPanel.tsx`](src/components/research/LocalRetrievalPanel.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for LocalRetrievalPanel. |
| [`src/components/research/OnlineRetrievalPanel.tsx`](src/components/research/OnlineRetrievalPanel.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for OnlineRetrievalPanel. |
| [`src/components/research/ResearchExecutionPipeline.tsx`](src/components/research/ResearchExecutionPipeline.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchExecutionPipeline. |
| [`src/components/research/ResearchMemoryPanel.tsx`](src/components/research/ResearchMemoryPanel.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchMemoryPanel. |
| [`src/components/research/ResearchSessionSummary.tsx`](src/components/research/ResearchSessionSummary.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchSessionSummary. |
| [`src/components/research/ResearchSessionWorkspace.tsx`](src/components/research/ResearchSessionWorkspace.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchSessionWorkspace. |
| [`src/components/research/ResearchSessionsPanel.tsx`](src/components/research/ResearchSessionsPanel.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchSessionsPanel. |
| [`src/components/research/ResearchTimeline.tsx`](src/components/research/ResearchTimeline.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for ResearchTimeline. |
| [`src/components/research/WhyThisPaperDrawer.tsx`](src/components/research/WhyThisPaperDrawer.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for WhyThisPaperDrawer. |
| [`src/components/ui/Overlays.tsx`](src/components/ui/Overlays.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | UI utility component for Overlays. |
| [`src/config/researchDomains.ts`](src/config/researchDomains.ts) | `.ts` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module researchDomains.ts. |
| [`src/data/known_good_review_questions.json`](src/data/known_good_review_questions.json) | `.json` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module known_good_review_questions.json. |
| [`src/data/research_review_toolkit.json`](src/data/research_review_toolkit.json) | `.json` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module research_review_toolkit.json. |
| [`src/data/review_execution_history.json`](src/data/review_execution_history.json) | `.json` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module review_execution_history.json. |
| [`src/layouts/AppLayout.tsx`](src/layouts/AppLayout.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module AppLayout.tsx. |
| [`src/layouts/Sidebar.tsx`](src/layouts/Sidebar.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module Sidebar.tsx. |
| [`src/layouts/TopNavigation.tsx`](src/layouts/TopNavigation.tsx) | `.tsx` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module TopNavigation.tsx. |
| [`src/mock/data.ts`](src/mock/data.ts) | `.ts` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module data.ts. |
| [`src/models/ResearchContext.ts`](src/models/ResearchContext.ts) | `.ts` | `DATABASE` | `source` | B | No | Database migration scripts and secondary ORM models. |
| [`src/pages/DiscussionsPage.tsx`](src/pages/DiscussionsPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for DiscussionsPage. |
| [`src/pages/DomainWorkspacePage.tsx`](src/pages/DomainWorkspacePage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for DomainWorkspacePage. |
| [`src/pages/LandingPage.tsx`](src/pages/LandingPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for LandingPage. |
| [`src/pages/LoginPage.tsx`](src/pages/LoginPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for LoginPage. |
| [`src/pages/NotebookPage.tsx`](src/pages/NotebookPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for NotebookPage. |
| [`src/pages/NotificationsPage.tsx`](src/pages/NotificationsPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for NotificationsPage. |
| [`src/pages/PaperLibraryPage.tsx`](src/pages/PaperLibraryPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for PaperLibraryPage. |
| [`src/pages/ProfilePage.tsx`](src/pages/ProfilePage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for ProfilePage. |
| [`src/pages/RegisterPage.tsx`](src/pages/RegisterPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for RegisterPage. |
| [`src/pages/ResearchDomainsPage.tsx`](src/pages/ResearchDomainsPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for ResearchDomainsPage. |
| [`src/pages/ResearchOverviewPage.tsx`](src/pages/ResearchOverviewPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for ResearchOverviewPage. |
| [`src/pages/ResearchReviewToolkitPage.tsx`](src/pages/ResearchReviewToolkitPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for ResearchReviewToolkitPage. |
| [`src/pages/SettingsPage.tsx`](src/pages/SettingsPage.tsx) | `.tsx` | `FRONTEND_PAGES` | `source` | B | Maybe | Supporting UI view for SettingsPage. |
| [`src/services/researchTopicService.ts`](src/services/researchTopicService.ts) | `.ts` | `RAG_ORCHESTRATION` | `source` | B | Maybe | Supporting service logic for researchTopicService.ts. |
| [`src/utils/cn.ts`](src/utils/cn.ts) | `.ts` | `FRONTEND_COMPONENTS` | `source` | B | No | Frontend module cn.ts. |
| [`test_5_queries.py`](test_5_queries.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_5_queries.py. |
| [`test_api.py`](test_api.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_api.py. |
| [`test_bm25.py`](test_bm25.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_bm25.py. |
| [`test_connectors.py`](test_connectors.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_connectors.py. |
| [`test_count.py`](test_count.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_count.py. |
| [`test_curl_api.py`](test_curl_api.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_curl_api.py. |
| [`test_curl_api2.py`](test_curl_api2.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_curl_api2.py. |
| [`test_curl_api3.py`](test_curl_api3.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_curl_api3.py. |
| [`test_curl_api4.py`](test_curl_api4.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_curl_api4.py. |
| [`test_deep.py`](test_deep.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_deep.py. |
| [`test_duplicates.py`](test_duplicates.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_duplicates.py. |
| [`test_exact_query.py`](test_exact_query.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_exact_query.py. |
| [`test_experiment.py`](test_experiment.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_experiment.py. |
| [`test_get_status.py`](test_get_status.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_get_status.py. |
| [`test_init.py`](test_init.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_init.py. |
| [`test_interactions.py`](test_interactions.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_interactions.py. |
| [`test_local.py`](test_local.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_local.py. |
| [`test_local_api.py`](test_local_api.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_local_api.py. |
| [`test_local_search.py`](test_local_search.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_local_search.py. |
| [`test_local_search2.py`](test_local_search2.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_local_search2.py. |
| [`test_local_search3.py`](test_local_search3.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_local_search3.py. |
| [`test_match.py`](test_match.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_match.py. |
| [`test_poll_status.py`](test_poll_status.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_poll_status.py. |
| [`test_postgres.py`](test_postgres.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_postgres.py. |
| [`test_query2.py`](test_query2.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_query2.py. |
| [`test_retriever.py`](test_retriever.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_retriever.py. |
| [`test_router.py`](test_router.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_router.py. |
| [`test_run_search.py`](test_run_search.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_run_search.py. |
| [`test_specific.py`](test_specific.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_specific.py. |
| [`test_status.py`](test_status.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_status.py. |
| [`test_trace.py`](test_trace.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_trace.py. |
| [`test_validation.py`](test_validation.py) | `.py` | `TESTS` | `source` | B | No | Automated test module test_validation.py. |
| [`tsconfig.json`](tsconfig.json) | `.json` | `CONFIGURATION` | `source` | B | No | Root build and dependency configuration tsconfig.json. |
| [`vite.config.ts`](vite.config.ts) | `.ts` | `CONFIGURATION` | `source` | B | No | Root build and dependency configuration vite.config.ts. |
| [`ResearchMind_LocalKB/embeddings/embedding_manifest.json`](ResearchMind_LocalKB/embeddings/embedding_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Knowledge base resource embedding_manifest.json. |
| [`ResearchMind_LocalKB/indexes/bm25_mapping.json`](ResearchMind_LocalKB/indexes/bm25_mapping.json) | `.json` | `DATASET_KB` | `reference` | C | No | Knowledge base resource bm25_mapping.json. |
| [`ResearchMind_LocalKB/indexes/index_manifest.json`](ResearchMind_LocalKB/indexes/index_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Knowledge base resource index_manifest.json. |
| [`ResearchMind_LocalKB/manifests/corpus_manifest.json`](ResearchMind_LocalKB/manifests/corpus_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Knowledge base resource corpus_manifest.json. |
| [`ResearchMind_LocalKB/manifests/offline_query_bank.json`](ResearchMind_LocalKB/manifests/offline_query_bank.json) | `.json` | `DATASET_KB` | `reference` | C | No | Knowledge base resource offline_query_bank.json. |
| [`ResearchMind_LocalKB/reports/extraction_failures.json`](ResearchMind_LocalKB/reports/extraction_failures.json) | `.json` | `DATASET_KB` | `reference` | C | No | Knowledge base resource extraction_failures.json. |
| [`ResearchMind_LocalKB/reports/failed_papers.json`](ResearchMind_LocalKB/reports/failed_papers.json) | `.json` | `DATASET_KB` | `reference` | C | No | Knowledge base resource failed_papers.json. |
| [`Viva/Presentation_Prep/build_study_guide.py`](Viva/Presentation_Prep/build_study_guide.py) | `.py` | `UTILITY` | `historical` | C | No | Viva preparation builder script build_study_guide.py. |
| [`Viva/Presentation_Prep/builder/doc_helpers.py`](Viva/Presentation_Prep/builder/doc_helpers.py) | `.py` | `UTILITY` | `historical` | C | No | Viva preparation builder script doc_helpers.py. |
| [`Viva/Presentation_Prep/builder/section_code_eval.py`](Viva/Presentation_Prep/builder/section_code_eval.py) | `.py` | `UTILITY` | `historical` | C | No | Viva preparation builder script section_code_eval.py. |
| [`Viva/Presentation_Prep/builder/section_compare_demo.py`](Viva/Presentation_Prep/builder/section_compare_demo.py) | `.py` | `UTILITY` | `historical` | C | No | Viva preparation builder script section_compare_demo.py. |
| [`Viva/Presentation_Prep/builder/section_modules_retrieval.py`](Viva/Presentation_Prep/builder/section_modules_retrieval.py) | `.py` | `UTILITY` | `historical` | C | No | Viva preparation builder script section_modules_retrieval.py. |
| [`Viva/Presentation_Prep/builder/section_story_stack.py`](Viva/Presentation_Prep/builder/section_story_stack.py) | `.py` | `UTILITY` | `historical` | C | No | Viva preparation builder script section_story_stack.py. |
| [`Viva/Presentation_Prep/builder/section_verification_xai.py`](Viva/Presentation_Prep/builder/section_verification_xai.py) | `.py` | `UTILITY` | `historical` | C | No | Viva preparation builder script section_verification_xai.py. |
| [`Viva/Presentation_Prep/builder/section_viva_defense.py`](Viva/Presentation_Prep/builder/section_viva_defense.py) | `.py` | `UTILITY` | `historical` | C | No | Viva preparation builder script section_viva_defense.py. |
| [`audit_e07_1.py`](audit_e07_1.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script audit_e07_1.py. |
| [`backend/app/data/gold_calibration_set.json`](backend/app/data/gold_calibration_set.json) | `.json` | `DATASET_KB` | `reference` | C | No | Toolkit / benchmark JSON dataset gold_calibration_set.json. |
| [`backend/data/known_good_review_questions.json`](backend/data/known_good_review_questions.json) | `.json` | `DATASET_KB` | `reference` | C | No | Toolkit / benchmark JSON dataset known_good_review_questions.json. |
| [`backend/data/research_review_toolkit.json`](backend/data/research_review_toolkit.json) | `.json` | `DATASET_KB` | `reference` | C | No | Toolkit / benchmark JSON dataset research_review_toolkit.json. |
| [`backend/data/review_execution_history.json`](backend/data/review_execution_history.json) | `.json` | `DATASET_KB` | `reference` | C | No | Toolkit / benchmark JSON dataset review_execution_history.json. |
| [`backend/offline_150_execution_report.json`](backend/offline_150_execution_report.json) | `.json` | `EVALUATION` | `reference` | C | No | Backend execution benchmark JSON offline_150_execution_report.json. |
| [`build_results_freeze.py`](build_results_freeze.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script build_results_freeze.py. |
| [`check_status.py`](check_status.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script check_status.py. |
| [`clean_corpus.py`](clean_corpus.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script clean_corpus.py. |
| [`compile_ieee_pdf.py`](compile_ieee_pdf.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script compile_ieee_pdf.py. |
| [`debug_status.json`](debug_status.json) | `.json` | `DATASET_KB` | `reference` | C | No | Reference state/data file debug_status.json. |
| [`edit.js`](edit.js) | `.js` | `UTILITY` | `historical` | C | No | Root utility/helper script edit.js. |
| [`edit.py`](edit.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script edit.py. |
| [`edit_api.py`](edit_api.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script edit_api.py. |
| [`edit_assistant.py`](edit_assistant.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script edit_assistant.py. |
| [`edit_assistant_ask.py`](edit_assistant_ask.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script edit_assistant_ask.py. |
| [`edit_date.py`](edit_date.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script edit_date.py. |
| [`edit_literature.py`](edit_literature.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script edit_literature.py. |
| [`edit_xaipage.py`](edit_xaipage.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script edit_xaipage.py. |
| [`evaluation/module_01/config.yaml`](evaluation/module_01/config.yaml) | `.yaml` | `EVALUATION` | `historical` | C | No | Evaluation module report/data config.yaml. |
| [`evaluation/module_01/error_analysis/gen_error_cases.py`](evaluation/module_01/error_analysis/gen_error_cases.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data gen_error_cases.py. |
| [`evaluation/module_01/run_module_1_experiment.py`](evaluation/module_01/run_module_1_experiment.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data run_module_1_experiment.py. |
| [`evaluation/module_02/config.yaml`](evaluation/module_02/config.yaml) | `.yaml` | `EVALUATION` | `historical` | C | No | Evaluation module report/data config.yaml. |
| [`evaluation/module_02/freeze_snapshots.py`](evaluation/module_02/freeze_snapshots.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data freeze_snapshots.py. |
| [`evaluation/module_02/revision_01/compute_corrected_metrics.py`](evaluation/module_02/revision_01/compute_corrected_metrics.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data compute_corrected_metrics.py. |
| [`evaluation/module_02/revision_01/generate_taxonomy_audit.py`](evaluation/module_02/revision_01/generate_taxonomy_audit.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data generate_taxonomy_audit.py. |
| [`evaluation/module_02/revision_01/inspect_candidates.py`](evaluation/module_02/revision_01/inspect_candidates.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data inspect_candidates.py. |
| [`evaluation/module_02/revision_01/inspect_claims.py`](evaluation/module_02/revision_01/inspect_claims.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data inspect_claims.py. |
| [`evaluation/module_02/revision_01/print_all_56.py`](evaluation/module_02/revision_01/print_all_56.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data print_all_56.py. |
| [`evaluation/module_02/revision_01/print_first_18.py`](evaluation/module_02/revision_01/print_first_18.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data print_first_18.py. |
| [`evaluation/module_02/revision_01/reanalyze_latency.py`](evaluation/module_02/revision_01/reanalyze_latency.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data reanalyze_latency.py. |
| [`evaluation/module_02/revision_01/reclassify_claims.py`](evaluation/module_02/revision_01/reclassify_claims.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data reclassify_claims.py. |
| [`evaluation/module_02/run_module_2_experiment.py`](evaluation/module_02/run_module_2_experiment.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data run_module_2_experiment.py. |
| [`evaluation/module_03/compute_module_03_analysis.py`](evaluation/module_03/compute_module_03_analysis.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data compute_module_03_analysis.py. |
| [`evaluation/module_03/config.yaml`](evaluation/module_03/config.yaml) | `.yaml` | `EVALUATION` | `historical` | C | No | Evaluation module report/data config.yaml. |
| [`evaluation/module_03/revision_01/verify_cleanliness.py`](evaluation/module_03/revision_01/verify_cleanliness.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data verify_cleanliness.py. |
| [`evaluation/module_03/run_fairness_consistency.py`](evaluation/module_03/run_fairness_consistency.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data run_fairness_consistency.py. |
| [`evaluation/module_03/run_module_03_experiment.py`](evaluation/module_03/run_module_03_experiment.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data run_module_03_experiment.py. |
| [`evaluation/publication_audit_v2/forensic_validation_v3/deterministic_recalculate.py`](evaluation/publication_audit_v2/forensic_validation_v3/deterministic_recalculate.py) | `.py` | `EVALUATION` | `historical` | C | No | Evaluation module report/data deterministic_recalculate.py. |
| [`extract_metadata.py`](extract_metadata.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script extract_metadata.py. |
| [`extract_pdfs.py`](extract_pdfs.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script extract_pdfs.py. |
| [`extract_text.py`](extract_text.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script extract_text.py. |
| [`find_api.py`](find_api.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script find_api.py. |
| [`find_exact_rects.py`](find_exact_rects.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script find_exact_rects.py. |
| [`fix_adapter.py`](fix_adapter.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_adapter.py. |
| [`fix_adapter_results.py`](fix_adapter_results.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_adapter_results.py. |
| [`fix_ai.py`](fix_ai.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_ai.py. |
| [`fix_api.py`](fix_api.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_api.py. |
| [`fix_authors.py`](fix_authors.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_authors.py. |
| [`fix_cleanup.py`](fix_cleanup.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_cleanup.py. |
| [`fix_div.py`](fix_div.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_div.py. |
| [`fix_frontend.py`](fix_frontend.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_frontend.py. |
| [`fix_gather.py`](fix_gather.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_gather.py. |
| [`fix_hybrid_search.py`](fix_hybrid_search.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_hybrid_search.py. |
| [`fix_local_xai.py`](fix_local_xai.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_local_xai.py. |
| [`fix_meta.py`](fix_meta.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_meta.py. |
| [`fix_other_pages.py`](fix_other_pages.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_other_pages.py. |
| [`fix_papers.py`](fix_papers.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_papers.py. |
| [`fix_prints.py`](fix_prints.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_prints.py. |
| [`fix_read_source.py`](fix_read_source.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_read_source.py. |
| [`fix_sources.py`](fix_sources.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_sources.py. |
| [`fix_trace.py`](fix_trace.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_trace.py. |
| [`fix_ts_errors.py`](fix_ts_errors.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_ts_errors.py. |
| [`fix_unused.py`](fix_unused.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_unused.py. |
| [`fix_warning.py`](fix_warning.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_warning.py. |
| [`fix_xai_detail.py`](fix_xai_detail.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_xai_detail.py. |
| [`fix_xai_page.py`](fix_xai_page.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script fix_xai_page.py. |
| [`generate_claim_evidence_map.py`](generate_claim_evidence_map.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_claim_evidence_map.py. |
| [`generate_colab.py`](generate_colab.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_colab.py. |
| [`generate_final_reconciled_pdfs.py`](generate_final_reconciled_pdfs.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_final_reconciled_pdfs.py. |
| [`generate_p0_artifacts.py`](generate_p0_artifacts.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_p0_artifacts.py. |
| [`generate_p0_governance.py`](generate_p0_governance.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_p0_governance.py. |
| [`generate_p1_artifacts.py`](generate_p1_artifacts.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_p1_artifacts.py. |
| [`generate_p2_p3_p4_artifacts.py`](generate_p2_p3_p4_artifacts.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_p2_p3_p4_artifacts.py. |
| [`generate_publication_figures.py`](generate_publication_figures.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_publication_figures.py. |
| [`generate_publication_tables.py`](generate_publication_tables.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_publication_tables.py. |
| [`generate_v3_forensics.py`](generate_v3_forensics.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_v3_forensics.py. |
| [`generate_v4_artifacts_part2.py`](generate_v4_artifacts_part2.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_v4_artifacts_part2.py. |
| [`generate_v4_registers.py`](generate_v4_registers.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script generate_v4_registers.py. |
| [`get_status.py`](get_status.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script get_status.py. |
| [`get_xai.py`](get_xai.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script get_xai.py. |
| [`hard_clean.py`](hard_clean.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script hard_clean.py. |
| [`ieee_paper/generate_expanded_ieee_paper.py`](ieee_paper/generate_expanded_ieee_paper.py) | `.py` | `UTILITY` | `historical` | C | No | Paper figure/text generator script generate_expanded_ieee_paper.py. |
| [`ieee_paper/generate_ieee_paper.py`](ieee_paper/generate_ieee_paper.py) | `.py` | `UTILITY` | `historical` | C | No | Paper figure/text generator script generate_ieee_paper.py. |
| [`ieee_paper/generate_web_ui_photos.py`](ieee_paper/generate_web_ui_photos.py) | `.py` | `UTILITY` | `historical` | C | No | Paper figure/text generator script generate_web_ui_photos.py. |
| [`integration_eval.py`](integration_eval.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script integration_eval.py. |
| [`local_evidence_new.py`](local_evidence_new.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script local_evidence_new.py. |
| [`package-lock.json`](package-lock.json) | `.json` | `DATASET_KB` | `reference` | C | No | Reference state/data file package-lock.json. |
| [`patch_evidence.py`](patch_evidence.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script patch_evidence.py. |
| [`patch_evidence2.py`](patch_evidence2.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script patch_evidence2.py. |
| [`patch_evidence3.py`](patch_evidence3.py) | `.py` | `UTILITY` | `historical` | C | No | One-time patch/repair script patch_evidence3.py. |
| [`prepare.py`](prepare.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script prepare.py. |
| [`process_corpus.py`](process_corpus.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script process_corpus.py. |
| [`public/data/known_good_review_questions.json`](public/data/known_good_review_questions.json) | `.json` | `DATASET_KB` | `reference` | C | No | Toolkit / benchmark JSON dataset known_good_review_questions.json. |
| [`public/data/research_review_toolkit.json`](public/data/research_review_toolkit.json) | `.json` | `DATASET_KB` | `reference` | C | No | Toolkit / benchmark JSON dataset research_review_toolkit.json. |
| [`public/data/review_execution_history.json`](public/data/review_execution_history.json) | `.json` | `DATASET_KB` | `reference` | C | No | Toolkit / benchmark JSON dataset review_execution_history.json. |
| [`publication_audit/01_system_inventory.json`](publication_audit/01_system_inventory.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 01_system_inventory.json. |
| [`publication_audit/02_retrieval_audit.json`](publication_audit/02_retrieval_audit.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 02_retrieval_audit.json. |
| [`publication_audit/03_rag_audit.json`](publication_audit/03_rag_audit.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 03_rag_audit.json. |
| [`publication_audit/04_verification_audit.json`](publication_audit/04_verification_audit.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 04_verification_audit.json. |
| [`publication_audit/05_refinement_audit.json`](publication_audit/05_refinement_audit.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 05_refinement_audit.json. |
| [`publication_audit/06_xai_audit.json`](publication_audit/06_xai_audit.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 06_xai_audit.json. |
| [`publication_audit/07_execution_state_audit.json`](publication_audit/07_execution_state_audit.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 07_execution_state_audit.json. |
| [`publication_audit/08_experiment_audit.json`](publication_audit/08_experiment_audit.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 08_experiment_audit.json. |
| [`publication_audit/09_benchmark_audit.json`](publication_audit/09_benchmark_audit.json) | `.json` | `EVALUATION` | `historical` | C | No | Historical publication audit snapshot 09_benchmark_audit.json. |
| [`rebuild_results_freeze_canonical.py`](rebuild_results_freeze_canonical.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script rebuild_results_freeze_canonical.py. |
| [`regenerate_e11_reconciled.py`](regenerate_e11_reconciled.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script regenerate_e11_reconciled.py. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_aggregate_metrics.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_aggregate_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_aggregate_metrics.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_citation_level_results.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_citation_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_citation_level_results.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_claim_level_results.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_claim_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_claim_level_results.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_component_deltas.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_component_deltas.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_component_deltas.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_config.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_config.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_error_analysis.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_error_analysis.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_error_analysis.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_hash_manifest.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_hash_manifest.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_integrity_report.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_integrity_report.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_latency_results.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_latency_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_latency_results.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_per_query_results.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_per_query_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_per_query_results.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_retrieval_results.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_retrieval_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_retrieval_results.json. |
| [`research_artifacts/ablation_evaluation/v11/e10_ablation/e10_statistics.json`](research_artifacts/ablation_evaluation/v11/e10_ablation/e10_statistics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e10_statistics.json. |
| [`research_artifacts/benchmark_v11/benchmark_items.json`](research_artifacts/benchmark_v11/benchmark_items.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact benchmark_items.json. |
| [`research_artifacts/benchmark_v11/benchmark_manifest.json`](research_artifacts/benchmark_v11/benchmark_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact benchmark_manifest.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_after_metrics.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_after_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_after_metrics.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_before_metrics.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_before_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_before_metrics.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_config.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_config.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_context_audit.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_context_audit.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_context_audit.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_error_analysis.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_error_analysis.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_error_analysis.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_hash_manifest.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_hash_manifest.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_integrity_report.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_integrity_report.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_latency_results.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_latency_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_latency_results.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_per_repair_results.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_per_repair_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_per_repair_results.json. |
| [`research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_statistics.json`](research_artifacts/citation_evaluation/v11/e06_1_corrected/e06_1_statistics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_1_statistics.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_after_metrics.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_after_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_after_metrics.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_before_metrics.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_before_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_before_metrics.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_config.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_config.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_error_analysis.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_error_analysis.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_error_analysis.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_hash_manifest.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_hash_manifest.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_integrity_report.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_integrity_report.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_latency_results.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_latency_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_latency_results.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_per_repair_results.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_per_repair_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_per_repair_results.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_query_level_results.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_query_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_query_level_results.json. |
| [`research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_statistics.json`](research_artifacts/citation_evaluation/v11/e06_citation_repair/e06_statistics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e06_statistics.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_category_counts.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_category_counts.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_category_counts.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_category_percentages.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_category_percentages.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_category_percentages.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_citation_level_classification.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_citation_level_classification.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_citation_level_classification.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_claim_level_classification.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_claim_level_classification.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_claim_level_classification.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_config.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_config.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_error_events.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_error_events.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_error_events.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_failure_trace.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_failure_trace.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_failure_trace.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_hash_manifest.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_hash_manifest.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_integrity_report.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_integrity_report.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_query_level_classification.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_query_level_classification.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_query_level_classification.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_statistics.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_statistics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_statistics.json. |
| [`research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_test_items.json`](research_artifacts/error_analysis/v11/e11_error_taxonomy/e11_test_items.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e11_test_items.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_aggregate_metrics.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_aggregate_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_aggregate_metrics.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_citation_level_results.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_citation_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_citation_level_results.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_claim_level_results.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_claim_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_claim_level_results.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_config.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_config.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_integrity_report.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_integrity_report.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_latency_results.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_latency_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_latency_results.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_naive_answers.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_naive_answers.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_naive_answers.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_per_query_results.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_per_query_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_per_query_results.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_provenance_audit.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_provenance_audit.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_provenance_audit.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_statistical_tests.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_statistical_tests.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_statistical_tests.json. |
| [`research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_verified_answers.json`](research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_verified_answers.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_1_verified_answers.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_aggregate_metrics.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_aggregate_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_aggregate_metrics.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_citation_level_results.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_citation_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_citation_level_results.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_claim_level_results.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_claim_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_claim_level_results.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_config.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_config.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_latency_results.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_latency_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_latency_results.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_naive_answers.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_naive_answers.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_naive_answers.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_per_query_results.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_per_query_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_per_query_results.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_statistical_tests.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_statistical_tests.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_statistical_tests.json. |
| [`research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_verified_answers.json`](research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_verified_answers.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e04_verified_answers.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_consistency_audit.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_consistency_audit.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_1_consistency_audit.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_hash_manifest.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_1_hash_manifest.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_integrity_report.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_1_integrity_report.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_latency_recheck.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_latency_recheck.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_1_latency_recheck.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_query_reclassification.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_query_reclassification.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_1_query_reclassification.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_statistics_recheck.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_statistics_recheck.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_1_statistics_recheck.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_aggregate_metrics.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_aggregate_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_aggregate_metrics.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_citation_level_results.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_citation_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_citation_level_results.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_claim_level_results.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_claim_level_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_claim_level_results.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_config.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_config.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_hash_manifest.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_hash_manifest.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_initial_answers.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_initial_answers.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_initial_answers.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_integrity_report.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_integrity_report.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_iteration_answers.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_iteration_answers.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_iteration_answers.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_iteration_changes.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_iteration_changes.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_iteration_changes.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_latency_results.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_latency_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_latency_results.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_no_iteration_answers.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_no_iteration_answers.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_no_iteration_answers.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_per_query_results.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_per_query_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_per_query_results.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_regression_analysis.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_regression_analysis.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_regression_analysis.json. |
| [`research_artifacts/generation_evaluation/v11/e07_iteration/e07_statistics.json`](research_artifacts/generation_evaluation/v11/e07_iteration/e07_statistics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e07_statistics.json. |
| [`research_artifacts/paper_experiment_protocol/PROTOCOL_FREEZE_MANIFEST.json`](research_artifacts/paper_experiment_protocol/PROTOCOL_FREEZE_MANIFEST.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact PROTOCOL_FREEZE_MANIFEST.json. |
| [`research_artifacts/paper_experiment_protocol/v1_1_amendment/PROTOCOL_V1_1_MANIFEST.json`](research_artifacts/paper_experiment_protocol/v1_1_amendment/PROTOCOL_V1_1_MANIFEST.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact PROTOCOL_V1_1_MANIFEST.json. |
| [`research_artifacts/results_freeze/publication_claim_register.json`](research_artifacts/results_freeze/publication_claim_register.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact publication_claim_register.json. |
| [`research_artifacts/results_freeze/results_freeze_manifest.json`](research_artifacts/results_freeze/results_freeze_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact results_freeze_manifest.json. |
| [`research_artifacts/results_freeze/results_freeze_master.json`](research_artifacts/results_freeze/results_freeze_master.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact results_freeze_master.json. |
| [`research_artifacts/retrieval_evaluation/e01_aggregate_results.json`](research_artifacts/retrieval_evaluation/e01_aggregate_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e01_aggregate_results.json. |
| [`research_artifacts/retrieval_evaluation/e01_raw_results/e01_bm25_raw.json`](research_artifacts/retrieval_evaluation/e01_raw_results/e01_bm25_raw.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e01_bm25_raw.json. |
| [`research_artifacts/retrieval_evaluation/e01_raw_results/e01_dense_raw.json`](research_artifacts/retrieval_evaluation/e01_raw_results/e01_dense_raw.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e01_dense_raw.json. |
| [`research_artifacts/retrieval_evaluation/e01_raw_results/e01_hybrid_raw.json`](research_artifacts/retrieval_evaluation/e01_raw_results/e01_hybrid_raw.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e01_hybrid_raw.json. |
| [`research_artifacts/retrieval_evaluation/e02_aggregate_results.json`](research_artifacts/retrieval_evaluation/e02_aggregate_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e02_aggregate_results.json. |
| [`research_artifacts/retrieval_evaluation/e02_raw_results/e02_b3_hybrid_raw.json`](research_artifacts/retrieval_evaluation/e02_raw_results/e02_b3_hybrid_raw.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e02_b3_hybrid_raw.json. |
| [`research_artifacts/retrieval_evaluation/e02_raw_results/e02_b4_bge_raw.json`](research_artifacts/retrieval_evaluation/e02_raw_results/e02_b4_bge_raw.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e02_b4_bge_raw.json. |
| [`research_artifacts/retrieval_evaluation/v11/e01/aggregate/e01_aggregate_results.json`](research_artifacts/retrieval_evaluation/v11/e01/aggregate/e01_aggregate_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e01_aggregate_results.json. |
| [`research_artifacts/retrieval_evaluation/v11/e01/raw/e01_raw_per_query.json`](research_artifacts/retrieval_evaluation/v11/e01/raw/e01_raw_per_query.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e01_raw_per_query.json. |
| [`research_artifacts/retrieval_evaluation/v11/e01_test_publication_results.json`](research_artifacts/retrieval_evaluation/v11/e01_test_publication_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e01_test_publication_results.json. |
| [`research_artifacts/retrieval_evaluation/v11/e02/aggregate/e02_aggregate_results.json`](research_artifacts/retrieval_evaluation/v11/e02/aggregate/e02_aggregate_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e02_aggregate_results.json. |
| [`research_artifacts/retrieval_evaluation/v11/e02/bge_sanity_5_items.json`](research_artifacts/retrieval_evaluation/v11/e02/bge_sanity_5_items.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact bge_sanity_5_items.json. |
| [`research_artifacts/retrieval_evaluation/v11/e02/candidate_schema.json`](research_artifacts/retrieval_evaluation/v11/e02/candidate_schema.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact candidate_schema.json. |
| [`research_artifacts/retrieval_evaluation/v11/e02/raw/e02_raw_per_query.json`](research_artifacts/retrieval_evaluation/v11/e02/raw/e02_raw_per_query.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e02_raw_per_query.json. |
| [`research_artifacts/retrieval_evaluation/v11/e02_statistical_analysis.json`](research_artifacts/retrieval_evaluation/v11/e02_statistical_analysis.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e02_statistical_analysis.json. |
| [`research_artifacts/retrieval_evaluation/v11/e02_test_publication_results.json`](research_artifacts/retrieval_evaluation/v11/e02_test_publication_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e02_test_publication_results.json. |
| [`research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_2_canonical_results.json`](research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_2_canonical_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e03_2_canonical_results.json. |
| [`research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_2_e01_canonical_recomputed.json`](research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_2_e01_canonical_recomputed.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e03_2_e01_canonical_recomputed.json. |
| [`research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_3_canonical_results_live.json`](research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_3_canonical_results_live.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e03_3_canonical_results_live.json. |
| [`research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_3_cutoff_prefix_summary.json`](research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_3_cutoff_prefix_summary.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e03_3_cutoff_prefix_summary.json. |
| [`research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_aggregate_results.json`](research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_aggregate_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e03_aggregate_results.json. |
| [`research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_raw_per_query.json`](research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_raw_per_query.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e03_raw_per_query.json. |
| [`research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/e03_1_independent_metric_check.json`](research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/e03_1_independent_metric_check.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e03_1_independent_metric_check.json. |
| [`research_artifacts/retrieval_evaluation/v11/experiment_manifest.json`](research_artifacts/retrieval_evaluation/v11/experiment_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact experiment_manifest.json. |
| [`research_artifacts/retrieval_evaluation/v11/final_latency_analysis.json`](research_artifacts/retrieval_evaluation/v11/final_latency_analysis.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact final_latency_analysis.json. |
| [`research_artifacts/retrieval_evaluation/v11/module_1_9/baseline_manifest.json`](research_artifacts/retrieval_evaluation/v11/module_1_9/baseline_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact baseline_manifest.json. |
| [`research_artifacts/retrieval_evaluation/v11/module_1_9/bge_execution_forensic_audit.json`](research_artifacts/retrieval_evaluation/v11/module_1_9/bge_execution_forensic_audit.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact bge_execution_forensic_audit.json. |
| [`research_artifacts/retrieval_evaluation/v11/module_1_9/candidate_set_equality_summary.json`](research_artifacts/retrieval_evaluation/v11/module_1_9/candidate_set_equality_summary.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact candidate_set_equality_summary.json. |
| [`research_artifacts/retrieval_evaluation/v11/module_1_9/genuine_rank_movement_summary.json`](research_artifacts/retrieval_evaluation/v11/module_1_9/genuine_rank_movement_summary.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact genuine_rank_movement_summary.json. |
| [`research_artifacts/retrieval_evaluation/v11/module_1_9/metric_definition_audit.json`](research_artifacts/retrieval_evaluation/v11/module_1_9/metric_definition_audit.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact metric_definition_audit.json. |
| [`research_artifacts/retrieval_evaluation/v11/module_1_9_1/independent_candidate_equality_summary.json`](research_artifacts/retrieval_evaluation/v11/module_1_9_1/independent_candidate_equality_summary.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact independent_candidate_equality_summary.json. |
| [`research_artifacts/retrieval_evaluation/v11/module_1_9_1/independently_verified_rank_movement.json`](research_artifacts/retrieval_evaluation/v11/module_1_9_1/independently_verified_rank_movement.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact independently_verified_rank_movement.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_adjudication_template.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_adjudication_template.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05a_adjudication_template.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_annotation_items.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_annotation_items.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05a_annotation_items.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_annotator_1_template.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_annotator_1_template.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05a_annotator_1_template.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_annotator_2_template.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_annotator_2_template.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05a_annotator_2_template.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_config.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05a_config.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_integrity_report.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05a_integrity_report.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_manifest.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/e05a_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05a_manifest.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/final/e05b_hash_manifest.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/final/e05b_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05b_hash_manifest.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/final/e05b_integrity_report.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/final/e05b_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05b_integrity_report.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/final/e05c_hash_manifest.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/final/e05c_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05c_hash_manifest.json. |
| [`research_artifacts/verification_evaluation/v11/e05_human_annotation/final/e05c_integrity_report.json`](research_artifacts/verification_evaluation/v11/e05_human_annotation/final/e05c_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05c_integrity_report.json. |
| [`research_artifacts/verification_evaluation/v11/e05_verifier_accuracy/e05_integrity_report.json`](research_artifacts/verification_evaluation/v11/e05_verifier_accuracy/e05_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e05_integrity_report.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_citation_evidence_results.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_citation_evidence_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_citation_evidence_results.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_claim_evidence_results.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_claim_evidence_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_claim_evidence_results.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_config.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_config.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_config.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_error_records.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_error_records.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_error_records.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_hash_manifest.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_hash_manifest.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_hash_manifest.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_integrity_report.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_integrity_report.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_integrity_report.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_local_provenance_results.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_local_provenance_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_local_provenance_results.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_metrics.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_metrics.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_metrics.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_offset_validation.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_offset_validation.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_offset_validation.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_online_provenance_results.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_online_provenance_results.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_online_provenance_results.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_per_claim_traces.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_per_claim_traces.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_per_claim_traces.json. |
| [`research_artifacts/xai_evaluation/v11/e08_provenance/e08_trace_completeness.json`](research_artifacts/xai_evaluation/v11/e08_provenance/e08_trace_completeness.json) | `.json` | `DATASET_KB` | `reference` | C | No | Frozen benchmark or evaluation artifact e08_trace_completeness.json. |
| [`run_e04_1_corrected.py`](run_e04_1_corrected.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script run_e04_1_corrected.py. |
| [`run_e11_error_taxonomy.py`](run_e11_error_taxonomy.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script run_e11_error_taxonomy.py. |
| [`run_e11_final_correction.py`](run_e11_final_correction.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script run_e11_final_correction.py. |
| [`scratch/capture_page.py`](scratch/capture_page.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script capture_page.py. |
| [`scratch/capture_qa.py`](scratch/capture_qa.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script capture_qa.py. |
| [`scratch/check_sqlite_dbs.py`](scratch/check_sqlite_dbs.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script check_sqlite_dbs.py. |
| [`scratch/clean_null_bytes.py`](scratch/clean_null_bytes.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script clean_null_bytes.py. |
| [`scratch/clean_runs.py`](scratch/clean_runs.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script clean_runs.py. |
| [`scratch/direct_backend_test_results.json`](scratch/direct_backend_test_results.json) | `.json` | `UTILITY` | `historical` | C | No | Development scratch/inspection script direct_backend_test_results.json. |
| [`scratch/gen_manifest.py`](scratch/gen_manifest.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script gen_manifest.py. |
| [`scratch/generate_ppt.py`](scratch/generate_ppt.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script generate_ppt.py. |
| [`scratch/inspect_chroma_dims.py`](scratch/inspect_chroma_dims.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script inspect_chroma_dims.py. |
| [`scratch/inspect_coords.py`](scratch/inspect_coords.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script inspect_coords.py. |
| [`scratch/inspect_malla.py`](scratch/inspect_malla.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script inspect_malla.py. |
| [`scratch/inspect_srs_doc.py`](scratch/inspect_srs_doc.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script inspect_srs_doc.py. |
| [`scratch/qa_screenshot.py`](scratch/qa_screenshot.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script qa_screenshot.py. |
| [`scratch/run_direct_backend_tests.py`](scratch/run_direct_backend_tests.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script run_direct_backend_tests.py. |
| [`scratch/run_visual_qa.py`](scratch/run_visual_qa.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script run_visual_qa.py. |
| [`scratch/strip_interleaved.py`](scratch/strip_interleaved.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script strip_interleaved.py. |
| [`scratch/update_malla_pptx.py`](scratch/update_malla_pptx.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script update_malla_pptx.py. |
| [`scratch/update_ppt_template.py`](scratch/update_ppt_template.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script update_ppt_template.py. |
| [`scratch/update_srs_doc.py`](scratch/update_srs_doc.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script update_srs_doc.py. |
| [`scratch/update_srs_rev_rel.py`](scratch/update_srs_rev_rel.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script update_srs_rev_rel.py. |
| [`scratch/update_srs_revision.py`](scratch/update_srs_revision.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script update_srs_revision.py. |
| [`scratch/write_chapters_11_to_14.py`](scratch/write_chapters_11_to_14.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script write_chapters_11_to_14.py. |
| [`scratch/write_chapters_1_to_3.py`](scratch/write_chapters_1_to_3.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script write_chapters_1_to_3.py. |
| [`scratch/write_chapters_4_to_5.py`](scratch/write_chapters_4_to_5.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script write_chapters_4_to_5.py. |
| [`scratch/write_chapters_6_to_7.py`](scratch/write_chapters_6_to_7.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script write_chapters_6_to_7.py. |
| [`scratch/write_chapters_8_to_10.py`](scratch/write_chapters_8_to_10.py) | `.py` | `UTILITY` | `historical` | C | No | Development scratch/inspection script write_chapters_8_to_10.py. |
| [`search_p1_p6.py`](search_p1_p6.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script search_p1_p6.py. |
| [`search_targets.py`](search_targets.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script search_targets.py. |
| [`search_terms.py`](search_terms.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script search_terms.py. |
| [`simplify_ux.py`](simplify_ux.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script simplify_ux.py. |
| [`status_dump.json`](status_dump.json) | `.json` | `DATASET_KB` | `reference` | C | No | Reference state/data file status_dump.json. |
| [`test2.py`](test2.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script test2.py. |
| [`trace_dump.json`](trace_dump.json) | `.json` | `DATASET_KB` | `reference` | C | No | Reference state/data file trace_dump.json. |
| [`tsconfig.app.json`](tsconfig.app.json) | `.json` | `DATASET_KB` | `reference` | C | No | Reference state/data file tsconfig.app.json. |
| [`tsconfig.node.json`](tsconfig.node.json) | `.json` | `DATASET_KB` | `reference` | C | No | Reference state/data file tsconfig.node.json. |
| [`update_ai.py`](update_ai.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script update_ai.py. |
| [`update_backend.py`](update_backend.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script update_backend.py. |
| [`update_deep_evidence.py`](update_deep_evidence.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script update_deep_evidence.py. |
| [`update_hybrid_search.py`](update_hybrid_search.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script update_hybrid_search.py. |
| [`update_hybrid_search2.py`](update_hybrid_search2.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script update_hybrid_search2.py. |
| [`update_metadata.py`](update_metadata.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script update_metadata.py. |
| [`update_relevance_gate.py`](update_relevance_gate.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script update_relevance_gate.py. |
| [`update_search.py`](update_search.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script update_search.py. |
| [`validate_corpus.py`](validate_corpus.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script validate_corpus.py. |
| [`validate_embeddings.py`](validate_embeddings.py) | `.py` | `UTILITY` | `historical` | C | No | Root utility/helper script validate_embeddings.py. |
| [`vercel.json`](vercel.json) | `.json` | `DATASET_KB` | `reference` | C | No | Reference state/data file vercel.json. |
| [`vite.config.d.ts`](vite.config.d.ts) | `.ts` | `UTILITY` | `historical` | C | No | Root utility/helper script vite.config.d.ts. |
| [`vite.config.js`](vite.config.js) | `.js` | `UTILITY` | `historical` | C | No | Root utility/helper script vite.config.js. |

---

**End of Inventory Report.**