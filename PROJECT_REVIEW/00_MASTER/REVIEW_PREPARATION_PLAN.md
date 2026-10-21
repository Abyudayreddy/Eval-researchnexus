# ResearchNexusAI — Review Preparation Plan (Phased Roadmap)

---

## Preparation Roadmap: 11 Structured Phases

### Phase 1: Project Overview & Motivation
- Read `01_PROJECT/PROJECT_OVERVIEW.md`.
- Understand the core problem: citation hallucination and opacity in academic literature synthesis.

### Phase 2: System Architecture & Data Flow
- Read `01_PROJECT/SYSTEM_ARCHITECTURE.md` and `COMPLETE_SYSTEM_FLOW.md`.
- Trace the lifecycle of a query from frontend to hybrid retrieval and NLI verification.

### Phase 3: Frontend Architecture
- Study `02_CODE/FRONTEND_FLOW.md` and core files `src/App.tsx`, `src/utils/api.ts`.
- Master the `ProtectedRoute` guard and Zustand store bindings.

### Phase 4: Backend API & Database
- Study `02_CODE/BACKEND_FLOW.md` and core files `main.py`, `api/papers.py`, `models/paper.py`.
- Understand database schemas and FastAPI route registration.

### Phase 5: RAG Pipeline Orchestration
- Study `03_RAG/` and core file `enhanced_rag.py`.
- Understand prompt assembly, passage injection, and multi-stage orchestration.

### Phase 6: Hybrid Retrieval & RRF
- Study `03_RAG/RETRIEVAL.md`, `HYBRID_RRF.md`, and core files `retrieval.py`, `local_evidence.py`.
- Master the RRF formula ($k=60$) and why ordinal rank fusion outperforms score normalization.

### Phase 7: Generation & LLM Providers
- Study `03_RAG/GENERATION.md` and core files `llm_provider.py`, `synthesis_engine.py`.
- Understand provider abstraction (Groq/Gemini) and low-temperature factual synthesis.

### Phase 8: Claim Verification & XAI Provenance
- Study `03_RAG/CLAIM_VERIFICATION.md`, `PROVENANCE_XAI.md`, and core file `claim_verifier.py`.
- Master NLI entailment classification and provenance graph construction.

### Phase 9: Evaluation & Canonical Results
- Study `05_EVALUATION/` and core file `reproduce_v4.py`.
- Memorize canonical numbers: Hit@20 = 86.7%, Grounding Precision = 88.4%, 1/5 claims citation baseline.

### Phase 10: IEEE Paper Defensibility
- Study `06_PAPER/`.
- Understand the alignment between manuscript claims and verified experimental tables.

### Phase 11: Viva Defense Mastery
- Practice speeches in `08_VIVA/` (30-second pitch, 2-minute summary, 5-minute presentation).
- Drill answers in `07_REVIEW_QA/` with special attention to `TRICKY_REVIEWER.md`.
