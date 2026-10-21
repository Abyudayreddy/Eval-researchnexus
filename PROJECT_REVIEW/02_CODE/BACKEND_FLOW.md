# ResearchNexusAI — Backend Execution Flow

> **Scope:** FastAPI Python Application (ackend/app/)  
> **Entry:** ackend/app/main.py  

---

## 1. High-Level Flow Architecture

`	ext
HTTP Request from Frontend (Axios)
    │
    ▼
[ backend/app/main.py ] ──────► CORS Middleware, Router Registry
    │
    ├───────────────────────────┬───────────────────────────┐
    ▼                           ▼                           ▼
/api/papers                 /api/ai                     /api/research
(Paper Search Gateway)      (RAG Synthesis & XAI)       (Comparative Review Engine)
    │                           │                           │
    ▼                           ▼                           ▼
[ services/retrieval.py ]   [ services/assistant/       [ services/assistant/
(Hybrid BM25 + Chroma)       enhanced_rag.py ]           comparison_engine.py ]
    │                           │                           │
    ├───────────────────────────┤                           │
    ▼                           ▼                           ▼
[ services/local_evidence.py ]  [ services/assistant/   [ services/assistant/
(Local KB Index Querying)        claim_verifier.py ]     synthesis_engine.py ]
    │                           │                           │
    ▼                           ▼                           ▼
SQLAlchemy / ChromaDB       [ services/assistant/       Research Matrix &
Database Lookups             citation_repair.py ]        Gap Analysis
                                │                           │
                                └─────────────┬─────────────┘
                                              ▼
                                Structured JSON Response
                                (Content, Citations, Claims, XAI)
`

---

## 2. Core Service Modules

1. **Server Bootstrap (main.py):**
   - Initializes FastAPI instance, configures CORS origins (localhost:5173).
   - Registers route modules: i.router, papers.router, 
esearch.router, uth.router.

2. **Retrieval Pipeline (services/retrieval.py & local_evidence.py):**
   - query_bm25_all(): Evaluates inverted index BM25 scores.
   - query_chromadb(): Calculates dense cosine distance against passage vectors.
   - 
eciprocal_rank_fusion(): Combines ranks via (d) = \sum \frac{1}{60 + r(d)}$.
   - 
erank_with_bge(): Cross-encoder scoring via BAAI/bge-reranker-large.

3. **Synthesis & Verification (enhanced_rag.py & claim_verifier.py):**
   - Injects retrieved context into prompt templates.
   - Invokes llm_provider.py (Groq/Gemini).
   - Decomposes output into atomic claims via claim_extractor.py.
   - Runs NLI verification against chunk text to output Entailed / Contradicted / Unverified labels.
   - Formats citation markers and packages the Explainable AI (XAI) provenance trace.
