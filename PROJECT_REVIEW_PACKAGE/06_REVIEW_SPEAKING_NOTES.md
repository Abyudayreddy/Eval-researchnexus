# Speaking Notes: ResearchNexus AI Faculty Review

**Project:** "An Explainable Research Assistant Using Hybrid Retrieval, XAI and Enhanced RAG"

## Key Facts
- **Corpus:** 706 local papers, 26,179 embeddings, 3 domains + isolated user upload collections
- **Retrieval:** BM25 + Dense (ChromaDB) + RRF(k=60) + BGE reranking
- **Online Sources:** arXiv, OpenAlex, PMC, AGRIS, NASA ADS (5 live connectors)
- **XAI:** 10-stage local timeline, 8-stage online timeline, WhyThisPaper provenance breakdown
- **Enhanced RAG:** Claim verification (5 statuses), citation repair, iterative refinement (max 2 cycles)
- **Context Engine:** 5 modes, 5 scopes, SHA-256 context hashing
- **Evaluation Console (Phase 3.10):** 8 locked baselines (B0-B7), RRF sensitivity, ablation matrix, blinded human evaluation, reproducible exports, **NOT MEASURED** metric governance
- **Tech Stack:** React 19, FastAPI, PostgreSQL, ChromaDB, Gemini Flash
- **Status:** **82.5% overall completion** (code implementation ~92%, evaluation infrastructure 100% complete and tested)

## Anticipated Questions & Answers

### 1. What is completed?
- **Core Pipelines:** Local (hybrid RRF + BGE) and 5 online retrieval connectors fully functional.
- **Explainability (XAI):** 10-stage local and 8-stage online transparency timelines operational.
- **Enhanced RAG Engine:** Claim verification, citation repair, evidence deduplication, and iterative refinement built.
- **Evaluation & Publication Console (Phase 3.10):** Complete evaluation models, FastAPI routes, baseline locking (B0-B7), ablation matrix, human eval UI, reproducible exporter, and 30 backend unit tests passed.

### 2. What is novel?
- **Integration:** Combines hybrid retrieval, XAI transparency, context-bound RAG, claim verification, and an integrated evaluation console.
- **Scientific Governance:** Enforces explicit provenance cells and strict UI display of **NOT MEASURED** for unrun metrics, preventing LLM metric fabrication.
- **Evaluation Infrastructure:** Built-in baseline locking (B0-B7), paired comparisons, RRF sensitivity sweeps, and blinded human evaluation in a single system.

### 3. Why hybrid retrieval?
- **Precision:** BM25 captures exact, critical keyword matches that dense vectors often miss.
- **Semantics:** Dense embeddings (ChromaDB) capture conceptual similarities and synonyms.
- **Robust Fusion:** Reciprocal Rank Fusion (RRF, k=60) effectively merges both signals without needing learned, domain-specific weights.

### 4. Why XAI?
- **Trust:** Researchers need transparency for critical decisions; black-box systems are insufficient.
- **Justification:** Users must understand *why* a paper was selected (BM25 rank vs Dense rank vs BGE score), not just *that* it was.
- **Traceability:** Exposes the 10-stage local and 8-stage online execution timelines for auditing.

### 5. Why Enhanced RAG & Claim Verification?
- **Grounding:** Basic RAG often hallucinates or relies on internal knowledge instead of provided text.
- **Strict Scoping:** Enforces strict adherence to user-defined context boundaries.
- **Verification & Repair:** Automatically extracts 6 claim types, evaluates deterministic & semantic alignment, and executes conservative citation repair.

### 6. What is Phase 3.10 Evaluation & Publication Console?
- **Purpose:** Makes the system experimentally defensible and publication-ready.
- **Baselines:** Locks 8 system variants from zero-shot LLM (`B0`) up to full iterative RAG (`B7`).
- **Ablation & Sensitivity:** Automates component removal studies and RRF parameter sweeps.
- **Human Eval:** Blinded 7-dimension scoring panel for human feedback.
- **Export:** One-click generation of JSON packages containing tables, metrics, and claim audit logs for paper submission.

### 7. Why do unrun metrics display as "NOT MEASURED"?
- **Scientific Integrity:** The system forbids displaying placeholder percentages (e.g., 75-85%) or 0% before experiments are executed.
- **Audit Policy:** Until an experiment is run through the Evaluation Console, metrics explicitly state **NOT MEASURED**.

### 8. How does it differ from Google Scholar?
- **Beyond Search:** Google Scholar stops at retrieving document links.
- **Transparency:** ResearchNexus details the exact 10-stage execution trace of why a document matched.
- **Synthesis:** Provides evidence-grounded, synthesized answers with verified claims, rather than just a list of links.

### 9. How does it differ from OpenScholar?
- **Scale:** OpenScholar uses massive parameter models (45M papers, 8B parameter retriever).
- **Our Approach:** ResearchNexus uses a focused local corpus (706 papers) and off-the-shelf BGE reranking without custom training.
- **Focus:** We emphasize XAI pipeline transparency, isolated personal corpora, and an integrated baseline-locked evaluation console.

### 10. What testing has been performed?
- **Backend Unit Tests:** 30 dedicated tests for the Evaluation Console (`test_evaluation_console.py`) passing 100%.
- **XAI Tests:** 37 XAI trace validation tests passed.
- **Build Verification:** Frontend builds cleanly via `npm run build` with 0 TypeScript errors.

### 11. What is the current completion percentage?
- **Overall:** **82.5%** overall completion.
- **Code Implementation:** ~92% finished.
- **Evaluation Infrastructure:** 100% complete (framework built and verified).
- **Benchmark Execution:** Ready to run.

### 12. What remains before final submission?
- **Execution:** Launch evaluation runs on the console to populate empirical metrics.
- **Human Eval:** Submit blinded ratings via the Human Evaluation Panel.
- **Writing:** Finalize the IEEE manuscript with exported reproducibility package tables.
