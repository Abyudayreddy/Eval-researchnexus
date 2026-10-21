# ResearchNexusAI — System Architecture

> **Architecture Style:** Decoupled Client-Server Micro-Architecture  
> **Backend:** FastAPI (Python 3.11+) | **Frontend:** React 18 + TypeScript + Vite  

---

## Architectural Diagram

```text
+------------------------------------------------------------------------+
|                        FRONTEND PRESENTATION LAYER                     |
|  React 18 + TypeScript + TailwindCSS + Zustand + Lucide Icons          |
|  |-- HybridSearchPage.tsx   (Querying & Parameter Tuning)              |
|  |-- AssistantPage.tsx      (Conversational RAG & Verified Badges)     |
|  |-- LiteratureReviewPage.tsx (Multi-Paper Comparative Synthesis)      |
|  +-- XaiPage.tsx            (Provenance DAG & Entailment Inspection)   |
+-----------------------------------T------------------------------------+
                                    | (Typed Axios HTTP / REST API)
                                    v
+------------------------------------------------------------------------+
|                        BACKEND API & ORCHESTRATION                     |
|  FastAPI + Pydantic v2 + Uvicorn                                       |
|  |-- /api/papers    --> Catalog Search, Filtering, Metadata Lookup     |
|  |-- /api/ai        --> RAG Query, Synthesis, XAI Traces              |
|  +-- /api/research  --> Literature Matrices & Gap Analyses             |
+------------------T--------------------------------T--------------------+
                   |                                |
                   v                                v
+--------------------------------------+  +------------------------------+
|       RAG ORCHESTRATION & NLI        |  |       RETRIEVAL & INDEX      |
|  |-- EnhancedRAGService              |  |  |-- BM25 (rank_bm25)        |
|  |-- IterativeRAGService             |  |  |-- ChromaDB (Vector Store) |
|  |-- ClaimVerifier (NLI Entailment)  |  |  |-- RRF Merger (k=60)       |
|  |-- SynthesisEngine                 |  |  +-- BGE Cross-Encoder       |
|  +-- CitationRepair Engine           |  |      Reranker                |
+------------------T-------------------+  +--------------T---------------+
                   |                                     |
                   v                                     v
+--------------------------------------+  +------------------------------+
|       EXTERNAL FOUNDATION LLMS       |  |       PERSISTENCE LAYER      |
|  |-- Groq API (Llama 3.3 70B)        |  |  |-- SQLite / PostgreSQL     |
|  |-- Google Gemini 1.5 Flash         |  |  |   (SQLAlchemy ORM)        |
|  +-- Fallback Multi-Provider Client  |  |  |-- Chroma Vector Store     |
|                                      |  |  +-- Pickled BM25 Indices    |
+--------------------------------------+  +------------------------------+
```
