# ResearchNexus: Master Research-Strength Audit Report

**Working Title**: *ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis*  
**Role**: Senior AI/IR Research Engineer & Research Publication Architect  
**Audit Date**: September 22, 2026  
**Audit Status**: COMPLETED  
**Artifact Directory**: `publication_audit/`  

---

## Executive Summary & Audit Methodology

This report presents a comprehensive, empirical audit of the existing **ResearchNexus** codebase, database schemas, retrieval models, RAG pipelines, verification engines, evaluation consoles, and experiment artifacts.

Every component, pipeline claim, and metric in this audit is marked with its exact ground truth status:
- **`VERIFIED`**: Code inspected, execution path traced, empirically functioning as claimed.
- **`PARTIAL`**: Code partially implemented or functionality fragmented across components.
- **`NOT TESTED`**: Feature or metric implemented in code but lacks automated/empirical verification.
- **`NOT FOUND`**: Documented feature or endpoint is missing from code.
- **`BROKEN`**: Implementation contains logic errors, hardcoded mock fallbacks, or broken contracts.
- **`CONFLICTING`**: Historical documentation or code artifacts report contradictory numbers.

---

## 1. System Inventory Summary

| Component / Subsystem | Primary Code Location | Implementation Status | Ground Truth Mark |
| :--- | :--- | :--- | :---: |
| **Hybrid Search (BM25 + Dense)** | `backend/app/services/retrieval.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Local Evidence Retriever** | `backend/app/services/local_evidence.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **BGE Cross-Encoder Reranker** | `backend/app/services/retrieval.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Context Manager & Scoping** | `backend/app/services/assistant/context_manager.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Enhanced RAG Generation** | `backend/app/services/assistant/enhanced_rag.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **2-Stage Claim Verification** | `backend/app/services/assistant/claim_verifier.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Conservative Citation Repair** | `backend/app/services/assistant/citation_repair.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Iterative Refinement Engine** | `backend/app/services/assistant/iterative_rag.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Multi-Paper Comparison Engine** | `backend/app/services/assistant/comparison_engine.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Literature Synthesis Engine** | `backend/app/services/assistant/synthesis_engine.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Personal Research Corpus** | `backend/app/api/documents.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |
| **Research Explorer UI** | `src/pages/HybridSearchPage.tsx` | `PARTIALLY_IMPLEMENTED` | **`PARTIAL`** |
| **XAI Trace Inspector UI** | `src/pages/XaiPage.tsx` | `PARTIALLY_IMPLEMENTED` | **`PARTIAL`** |
| **Backend XAI Endpoint** | `backend/app/api/ai.py` (`/api/explain`) | `NOT_IMPLEMENTED` | **`BROKEN`** |
| **Evaluation Service & Runner** | `backend/app/services/evaluation_service.py` | `BROKEN` (Uses simulation mocks) | **`BROKEN`** |
| **Benchmark Dataset v1.0** | `backend/app/scripts/seed_benchmark_v10.py` | `VERIFIED_IMPLEMENTED` | **`VERIFIED`** |

---

## 2. Core Subsystem Audits

### 2.1 Retrieval Layer Audit (`02_retrieval_audit.json`) — **`VERIFIED`**
- **Models**: BM25Okapi (`rank_bm25`), Dense `BAAI/bge-base-en-v1.5` (768-dim), Cross-Encoder `BAAI/bge-reranker-base`.
- **Parameters**: RRF $k=60$, sparse top-K=20, dense top-K=20, fused candidates=20, final evidence top-K=5.
- **Scoring**: $S_{\text{RRF}}(d) = \frac{1}{60 + r_{\text{bm25}}} + \frac{1}{60 + r_{\text{dense}}}$.
- **Provenance Preservation**: `paper_id`, `source`, `bm25_rank`, `dense_rank`, `rrf_score`, `reranker_score`, `final_rank`, `chunk_id` are fully preserved in `local_evidence.py`.

### 2.2 RAG Layer Audit (`03_rag_audit.json`) — **`PARTIAL`**
- **Context Bounding**: Enforced via SHA-256 `context_hash` and `context_snapshot_id`. Deduplicates context to top 5 evidence blocks.
- **Search Re-run Finding**: If `search_id` UUID is provided, `/ask` uses cached Explorer search results. If `search_id` is omitted in hybrid mode, `/ask` re-runs `search_papers` unnecessarily.
- **Failure Distinction**: Returns `insufficient_evidence` when evidence count is 0 without calling Gemini. Quota exhaustion returns `quota_exceeded`.

### 2.3 Verification Audit (`04_verification_audit.json`) — **`VERIFIED`**
- **Stage A**: Deterministic regex checks for numerical mismatches and negation polarity flips.
- **Stage B**: Gemini 2.5 Flash NLI entailment classifier over cited chunks.
- **Citation Repair Leakage**: Verified leak-free. `CitationRepair` matches un-cited claims strictly against `available_evidence` snippets already present in the active context.
- **Statuses**: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `UNSUPPORTED`, `VERIFICATION_UNAVAILABLE`.

### 2.4 Refinement Audit (`05_refinement_audit.json`) — **`VERIFIED`**
- **Max Cycles**: Hard stop at `MAX_REFINEMENT_CYCLES = 2`.
- **Stopping Conditions**: `single_pass` mode, no refinement needed, identical feedback signature (anti-oscillation), or zero new evidence returned.
- **Latency Overhead**: Multi-cycle refinement adds $+753.3\text{ ms}$ P50 overhead (+150.6%) and 2 extra model calls per cycle.

### 2.5 XAI Audit (`06_xai_audit.json`) — **`PARTIAL`**
- **History Re-execution**: Opening old XAI history renders stored trace JSONs (`trace_dump.json`, `status_dump.json`) without re-running retrieval or Gemini.
- **Trace Chain Gap**: Paper-level retrieval scores and claim-level verification audits exist in separate UI drawers; end-to-end chain from claim to BGE rank is split.
- **API Stub**: Backend `/api/explain` is an un-implemented stub returning hardcoded JSON.

### 2.6 Execution State Audit (`07_execution_state_audit.json`) — **`PARTIAL`**
- **Backend Machine**: 10 authoritative states in `SearchExperiment` (`INITIALIZING` $\rightarrow$ `COMPLETED_WITH_RESULTS` / `COMPLETED_NO_RESULTS` / `FAILED`) with `terminal` boolean.
- **Frontend Bug**: UI progress handlers can briefly display a false "0 results" banner before polling reaches a terminal state.

### 2.7 Experiment & Benchmark Audit (`08_experiment_audit.json`, `09_benchmark_audit.json`) — **`CONFLICTING`** / **`BROKEN`**
- **Benchmark `ds_nexus_v10`**: 100 items (70 DEV, 15 VAL, 15 TEST) seeded in DB with 9 question categories.
- **Conflicting MRR Values**:
  - `evaluation_stage1_benchmark_e01_report.md`: B3 TEST MRR = **0.812** (Full MRR = 0.898).
  - `evaluation_stage2_E02_BGE_reranking_report.md`: B3 TEST MRR = **0.900**.
  - `MODULE_3_IMPLEMENTATION_RESULTS_PUBLICATION_PROGRESS_REPORT.md`: Contains both 0.812 (Line 327) and 0.900 (Line 348).
- **Simulation Mock Finding**: `backend/app/services/evaluation_service.py` uses hardcoded mock functions (`_simulate_retriever`) rather than executing real retrieval and Gemini model calls against `ds_nexus_v10`.

---

## 3. Core Audit Findings & Verdicts

### A. What is Already Strong
1. **Core Assistant & RAG Algorithms**: `EnhancedRAGService`, `ClaimVerifier`, `CitationRepair`, and `IterativeRAGService` are fully implemented with clean, modular Python logic.
2. **Local Hybrid Retrieval**: `LocalEvidenceRetriever` delivers high-precision BM25 + BGE vector search + RRF fusion + BGE reranking with full provenance metadata over 14,850 chunks.
3. **Structured Context Management**: `ContextManager` enforces strict scope boundaries, mode rules, SHA-256 context hashing, and evidence eligibility.

### B. What is Weak
1. **Fragmented XAI Trace**: Claim verification and paper retrieval scores are split across two separate UI modals (`XAIModal.tsx` and `ClaimProofDrawer.tsx`).
2. **Search-ID Disconnection in `/ask`**: Omitting `search_id` in `/api/ai/ask` causes unnecessary re-running of search.
3. **Frontend UI State Flashes**: Frontend renders empty result states before backend polling sets `terminal = true`.

### C. What is Broken
1. **Evaluation Service Mocking (`evaluation_service.py`)**: Benchmark runs execute static simulation code (`_simulate_retriever`) instead of real pipeline inference.
2. **Backend XAI Endpoint (`/api/explain`)**: Returns static hardcoded JSON.
3. **Documented Metric Conflicts**: Discrepancy between 0.812 vs 0.900 B3 MRR in project markdown reports.

### D. What Should Be Strengthened First
1. Refactor `backend/app/services/evaluation_service.py` to run **real** DB-driven retrieval, Gemini generation, and claim verification over `ds_nexus_v10`.
2. Re-run E01–E05 benchmark suite on real hardware to establish single, canonical, un-conflicted publication metrics.
3. Mandate `search_id` in `/api/ai/ask` and unify the XAI trace chain.

---

## 4. Affected Files & Test Requirements for Module 1

### E. Exact Files / Services Affected by Module 1
1. `backend/app/services/evaluation_service.py` (Must remove simulation mocks).
2. `backend/app/api/ai.py` (Must enforce `search_id` and implement real `/api/explain`).
3. `backend/app/api/papers.py` (Must expose complete SearchExperiment state machine).
4. `src/components/evaluation/EvaluationConsole.tsx` (Must render real benchmark outputs).
5. `src/pages/HybridSearchPage.tsx` (Must guard empty UI states behind `terminal === true`).

### F. Exact Tests Required After Module 1
1. `pytest backend/app/tests/test_evaluation_service.py` (Validate real execution over `ds_nexus_v10`).
2. `pytest backend/app/tests/test_claim_verification.py` (Validate 2-stage verification & repair).
3. `pytest backend/app/tests/test_retrieval_provenance.py` (Validate full provenance field preservation).
4. `npm test -- --grep "search_flow_validation"` (Validate frontend state machine polling).

---

## Stop Notice
Per prompt instructions, audit execution is complete. All 13 audit JSON/MD artifacts have been created in `publication_audit/`. Implementation of Module 1 will NOT begin until requested by the user.
