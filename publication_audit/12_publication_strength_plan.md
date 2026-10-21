# Publication Strength Plan & Remediation Roadmap

**Auditor Status**: VERIFIED  
**Date**: September 22, 2026  

---

## 1. Plan Objective

This document outlines the mandatory remediation steps required to transform the ResearchNexus codebase into a 100% empirical, publication-ready research platform. These steps address all identified simulation mocks, state discrepancies, and API stubs before any new feature work (Module 1) is initiated.

---

## 2. Mandatory Remediation Phases

### Phase A: Evaluation & Benchmark Engine Hardening (Priority 1)
1. **Eliminate Mock Simulation Code**:
   - Replace `_simulate_retriever`, `_execute_generation_pipeline`, and `_execute_verification_pipeline` in `backend/app/services/evaluation_service.py` with real calls to `LocalEvidenceRetriever`, `EnhancedRAGService`, and `ClaimVerifier`.
2. **Database-Driven Benchmark Execution**:
   - Update `EvaluationService` to query `EvaluationItem` database records (`ds_nexus_v10`) directly during benchmark runs.
3. **Artifact Generation & Hash Locking**:
   - Automatically log raw JSON execution trajectories for all 100 items upon benchmark completion, producing cryptographically hashed output packages (`ds_nexus_v10_eval_results.json`).

### Phase B: Retrieval & Pipeline Grounding (Priority 2)
1. **Strict BGE Model Enforcement**:
   - Modify `get_reranker()` in `backend/app/services/retrieval.py` and `local_evidence.py` to raise an explicit exception if `sentence_transformers` or `BAAI/bge-reranker-base` fails to load during evaluation mode, preventing silent fallback to `MockCrossEncoder`.
2. **Context Preservation & `search_id` Enforcement**:
   - Update `/api/ai/ask` in `backend/app/api/ai.py` to require a valid `search_id`. Ensure that `/ask` retrieves context exclusively from stored `SearchExperiment` results, eliminating redundant search re-runs.

### Phase C: Explainability & State Machine Alignment (Priority 3)
1. **Unified XAI Provenance Trace**:
   - Implement the complete trace chain (`FINAL CLAIM -> CITATION -> EVIDENCE BLOCK -> PAPER -> BGE RANK -> RRF -> BM25/DENSE ORIGIN`) in a unified backend DTO.
   - Implement real dynamic logic in `/api/explain/{claim_id}` in `backend/app/api/ai.py`.
2. **Authoritative UI Execution Guards**:
   - Update frontend progress components (`LocalProgressPanel.tsx`, `ExplorePapersWorkspace.tsx`) to guard empty-result state displays behind `terminal === true && (status === 'COMPLETED_NO_RESULTS' || status === 'FAILED')`.

---

## 3. Verification & Validation Protocol

After completing Phases A–C, the following validation commands must be executed to verify publication readiness:
1. `pytest backend/app/tests/test_evaluation_service.py` (Verify real evaluation execution without mock fallbacks).
2. `pytest backend/app/tests/test_claim_verification.py` (Verify 2-stage claim verification and citation repair).
3. `pytest backend/app/tests/test_retrieval_provenance.py` (Verify end-to-end rank and score preservation).
