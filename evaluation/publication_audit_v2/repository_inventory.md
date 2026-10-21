# Repository Inventory & Structural Audit

## 1. Executive Summary
This document provides an exhaustive structural and functional audit of the ResearchNexusAI codebase and research experimental artifacts as part of the IEEE Publication Audit v2.

## 2. Directory Structure and Responsibilities
- **backend/**: Core production and research pipeline implementation.
  - `app/services/vector_store.py`: ChromaDB dense retrieval, embedding generation, collection management.
  - `app/services/hybrid_search.py`: Lexical BM25 (rank_bm25 / Okapi), Dense query execution, and Reciprocal Rank Fusion (RRF with k=60).
  - `app/services/reranker.py`: Cross-encoder neural reranking via BAAI/bge-reranker-base.
  - `app/services/verification.py`: Claim extraction, NLI-based claim verification, citation extraction, bracket alignment.
  - `app/services/refinement.py`: Iterative synthesis refinement loop for grounding improvement.
  - `app/core/config.py`: Authoritative LLM runtime configuration (Gemini 2.5 Flash, temperature 0.0).
- **research_artifacts/**: Historical experiment records (E01-E10), frozen benchmarks (ds_nexus_v11), legacy freeze tables.
- **evaluation/**:
  - `audit/`: Phase 0 pre-experiment audit and historical readiness checks.
  - `module_01/`: Canonical frozen retrieval benchmark run (15 test queries, BM25, Dense, RRF, Reranker).
  - `module_02/`: Canonical frozen answer grounding and claim verification (56 claims, factual vs refusal taxonomy).
  - `module_03/`: Canonical frozen citation validation and repair evaluation (CitationRepair coverage & safety analysis).
  - `publication_audit_v2/`: Current master publication audit and reconciliation package.

## 3. Core Component Verification
| Component | Implementation File | Verified State | Notes |
| :--- | :--- | :---: | :--- |
| Lexical Retrieval | `backend/app/services/hybrid_search.py` | VERIFIED | Uses rank_bm25 Okapi BM25 |
| Dense Retrieval | `backend/app/services/vector_store.py` | VERIFIED | BAAI/bge-base-en-v1.5, 768 dims |
| Hybrid Fusion | `backend/app/services/hybrid_search.py` | VERIFIED | RRF k=60 |
| Reranker | `backend/app/services/reranker.py` | VERIFIED | BAAI/bge-reranker-base |
| Claim Verifier | `backend/app/services/verification.py` | VERIFIED | NLI-based claim grounding |
| Citation Repair | `backend/app/services/citation_repair.py` | VERIFIED | Deterministic candidate matching |
