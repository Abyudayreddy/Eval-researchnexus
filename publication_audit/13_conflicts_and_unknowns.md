# Conflicts, Discrepancies, & Unknowns Report

**Auditor Status**: CONFLICTING / UNKNOWN  
**Date**: September 22, 2026  

---

## 1. Documented Metric Conflicts

### Conflict 1: Baseline B3 Hybrid MRR Value on Frozen TEST Split (N=15)
* **Conflict Statement**: Different project documents report conflicting MRR values for the B3 Hybrid baseline on the same 15-item TEST split.
* **Source A**: `evaluation_stage1_benchmark_e01_report.md` Section 3.1 reports B3 Hybrid MRR on TEST split (N=15) is **0.812** (and 0.898 on full N=100 benchmark).
* **Source B**: `evaluation_stage2_E02_BGE_reranking_report.md` Section 2 reports B3 Hybrid MRR on TEST split (N=15) is **0.900**.
* **Source C**: `MODULE_3_IMPLEMENTATION_RESULTS_PUBLICATION_PROGRESS_REPORT.md` Line 327 reports B3 TEST MRR = **0.812**, while Line 348 reports B3 TEST MRR = **0.900**.
* **Auditor Verdict**: **`CONFLICTING`**. The code base contains both numbers in documentation. The actual value must be re-calculated by running un-simulated code over `ds_nexus_v10`.

### Conflict 2: Full Benchmark (N=100) vs TEST Split (N=15) Metric Reporting
* **Conflict Statement**: Some sections quote 100-item metrics while others quote 15-item TEST split metrics without clear demarcation.
* **Example**: E02 BGE reranking report lists B3 MRR = 0.900 $\rightarrow$ B4 MRR = 0.972 (TEST split N=15), whereas MODULE_3 Line 352 notes that on the full 100-item benchmark, B3 MRR is 0.812 $\rightarrow$ B4 MRR is 0.887.
* **Auditor Verdict**: **`CONFLICTING`**. Published paper tables must consistently report both N=100 and N=15 columns side-by-side to prevent reviewer confusion.

---

## 2. Implementation vs Documentation Discrepancies

### Discrepancy 1: Benchmark Runner Simulation Mock
* **Documentation Claim**: Evaluation Console and reports claim automated, empirical execution of benchmark experiments E01–E05 over `ds_nexus_v10`.
* **Implementation Truth**: `backend/app/services/evaluation_service.py` contains `_simulate_retriever`, `_execute_generation_pipeline`, and hardcoded return metric dictionaries.
* **Auditor Verdict**: **`BROKEN`**.

### Discrepancy 2: Stubbed XAI Explain Endpoint
* **Documentation Claim**: Complete REST API `/api/explain` for XAI trace retrieval.
* **Implementation Truth**: `backend/app/api/ai.py` line 305 defines `@router.get('/explain')` returning `{"message": "AI Explain endpoint"}`.
* **Auditor Verdict**: **`NOT_IMPLEMENTED`**.

---

## 3. Unverified Assumptions & Unknowns

1. **Human Evaluation Scores**: Marked as `NOT MEASURED` across all reports. No double-blind human rating data exists.
2. **Real BGE Reranker Execution in Test Suite**: Pytest tests pass using `MockCrossEncoder` if sentence-transformers is not loaded in dev environment. Real BGE model performance requires explicit verification with `USE_REAL_BGE=true`.
3. **Gemini API Quota Fallback Behavior**: Dynamic fallback to secondary models or local Ollama is implemented in `LLMProviderManager`, but behavior under heavy burst concurrency is not stress-tested.
