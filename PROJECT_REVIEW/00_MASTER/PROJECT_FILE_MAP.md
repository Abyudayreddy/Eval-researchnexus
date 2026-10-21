# ResearchNexusAI — Master Project File Map

---

## 1. Top-Level Directory Navigation

```text
SDC2/
|-- PROJECT_REVIEW/          <-- CENTRAL STUDY & REVIEW LAYER (10 Submodules)
|   |-- 00_MASTER/           (Master guides, file maps, documentation classification)
|   |-- 01_PROJECT/          (Overview, architecture, tech stack, complete flow)
|   |-- 02_CODE/             (23 A+ core files, preparation matrix, frontend/backend flow)
|   |-- 03_RAG/              (Retrieval, RRF, BGE rerank, Generation, Verification, XAI)
|   |-- 04_DATA_KB/          (Dataset distribution, local KB, indexing pipeline)
|   |-- 05_EVALUATION/       (V4 canonical results, metrics to remember, pipeline)
|   |-- 06_PAPER/            (Paper evidence map, LaTeX update guidance)
|   |-- 07_REVIEW_QA/        (Basic, architecture, code, RAG, evaluation, tricky Q&A)
|   |-- 08_VIVA/             (30-sec pitch, 2-min summary, 5-min talk, full viva)
|   +-- 99_ARCHIVE/          (Archived historical review material)
|
|-- src/                     <-- FRONTEND SOURCE (React 18 + TypeScript + Vite)
|   |-- App.tsx              (Client routing & auth protection)
|   |-- pages/               (HybridSearch, Assistant, LiteratureReview, XAI, etc.)
|   |-- store/               (Zustand stores: auth, papers, research, XAI)
|   +-- utils/               (api.ts typed Axios HTTP client)
|
|-- backend/                 <-- BACKEND SOURCE (FastAPI + SQLAlchemy)
|   +-- app/
|       |-- main.py          (FastAPI entry point & middleware)
|       |-- api/             (ai.py, papers.py, research.py)
|       |-- models/          (paper.py, session.py, document.py)
|       +-- services/        (retrieval.py, local_evidence.py, enhanced_rag.py, claim_verifier.py)
|
|-- ResearchMind_Dataset/    <-- PRESERVED CORPUS (687 PDFs across 3 domains)
|-- ResearchMind_LocalKB/    <-- KNOWLEDGE BASE (BM25 pkl, ChromaDB, extracted text)
|
|-- evaluation/              <-- EVALUATION EVIDENCE
|   +-- Re-evaluation of mistakes/  <-- AUTHORITATIVE V4 CANONICAL PACKAGE
|       |-- paper_readiness_gate.md
|       |-- v4_reconciliation_report.md
|       |-- canonical_retrieval_metrics.csv
|       |-- canonical_grounding_metrics.json
|       +-- CURRENT_LATEX_V4_UPDATE_INSTRUCTIONS.md
|
|-- ieee_paper/              <-- IEEE CONFERENCE MANUSCRIPT
|   |-- ResearchNexus_AI_Paper.tex  (LaTeX manuscript source)
|   +-- ResearchNexus_AI_Paper.pdf  (Compiled PDF draft)
|
|-- paper_figures/           <-- PUBLICATION PLOTS (PNG, SVG, PDF)
|-- paper_tables/            <-- PUBLICATION TABLES (LaTeX, CSV, Markdown)
|-- research_artifacts/      <-- FROZEN EXPERIMENTAL RUNS (E01-E11)
|-- archive/                 <-- ARCHIVED EARLIER DEVELOPMENT WORK
+-- scratch/                 <-- TEMPORARY SCRATCH SCRIPTS
```
