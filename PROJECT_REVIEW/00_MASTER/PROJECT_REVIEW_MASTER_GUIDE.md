# ResearchNexusAI — Master Project Review & Defense Guide

> **Authoritative Entry Point for Faculty Review, Viva Defense, and Paper Preparation**  
> **Repository:** `C:\Users\Abyureddy\Downloads\SDC2`  
> **Date:** October 2026  

---

## 1. What is ResearchNexusAI?
ResearchNexusAI is an Explainable Multi-Stage Retrieval-Augmented Generation (RAG) framework engineered for multi-document scientific literature synthesis. It integrates:
- Dual-channel hybrid retrieval (Okapi BM25 + ChromaDB dense BGE embeddings) fused with Reciprocal Rank Fusion ($k=60$).
- Cross-encoder reranking via `BAAI/bge-reranker-large`.
- Multi-provider LLM generation for comparative synthesis.
- Automated Natural Language Inference (NLI) claim verification.
- Interactive Explainable AI (XAI) provenance graphing linking synthesized claims to source PDF chunks.

---

## 2. Repository Navigation Guide

| Directory | Exact Purpose | Status / Action |
|---|---|---|
| `PROJECT_REVIEW/` | **Central Study & Review Layer** (Architecture, Code, RAG, Viva) | **Study this folder deeply** |
| `src/` | Frontend React 18 + TypeScript + Vite web application | Active source code (Do not modify) |
| `backend/` | FastAPI backend services, API routers, database models | Active source code (Do not modify) |
| `ResearchMind_Dataset/` | 687 research papers (PDFs) across AI, Environmental, Interdisciplinary | Preserved corpus dataset |
| `ResearchMind_LocalKB/` | Precomputed BM25 indices, ChromaDB vector store, extracted texts | Active knowledge base |
| `evaluation/Re-evaluation of mistakes/` | **Authoritative V4 canonical evaluation package** | Authoritative experimental truth |
| `ieee_paper/` | IEEE conference paper LaTeX draft (`ResearchNexus_AI_Paper.tex`) | Active paper submission files |
| `paper_figures/` & `paper_tables/` | Publication plots and camera-ready LaTeX tables | Active paper artifacts |
| `research_artifacts/` | Frozen experimental outputs from E01 through E11 | Historical research evidence |
| `archive/` & `scratch/` | Historical development iterations and temporary scripts | Reference / Do-not-study |

---

## 3. What to Study vs. What NOT to Study

### MUST STUDY (The 23 A+ Core Files)
Focus your preparation on `PROJECT_REVIEW/02_CODE/CORE_CODE_FILES.md`:
1. `src/App.tsx`
2. `backend/app/main.py`
3. `backend/app/api/ai.py`
4. `backend/app/api/papers.py`
5. `backend/app/api/research.py`
6. `backend/app/models/paper.py`
7. `backend/app/services/assistant/enhanced_rag.py`
8. `backend/app/services/assistant/iterative_rag.py`
9. `backend/app/services/retrieval.py`
10. `backend/app/services/local_evidence.py`
11. `chunk_corpus.py`
12. `embed_corpus.py`
13. `build_indexes.py`
14. `backend/app/services/llm_provider.py`
15. `backend/app/services/assistant/synthesis_engine.py`
16. `backend/app/services/assistant/claim_verifier.py`
17. `backend/app/services/assistant/citation_repair.py`
18. `src/utils/api.ts`
19. `src/pages/HybridSearchPage.tsx`
20. `src/pages/AssistantPage.tsx`
21. `src/pages/LiteratureReviewPage.tsx`
22. `src/pages/XaiPage.tsx`
23. `evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py`

### DO NOT STUDY
- Do not memorize the 151 temporary/scratch scripts (`scratch/*`, `fix_*.py`).
- Do not memorize the 255 static benchmark raw JSON outputs (`research_artifacts/*`).
- Do not memorize superseded early audit reports. Use only the V4 canonical package.
