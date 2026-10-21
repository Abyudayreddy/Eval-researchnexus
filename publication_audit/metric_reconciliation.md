# Metric Reconciliation: Simulated Audit vs Real Evaluation Baseline

## 1. Executive Summary

This document reconciles the differences between the pre-implementation mock simulation audit findings (derived from legacy hardcoded returns) and the empirical results from **Module 1 (Real Retrieval Evaluation & Experiment Integrity)** using `LocalEvidenceRetriever` over the `ds_nexus_v10` benchmark.

---

## 2. Quantitative Metric Reconciliation

| System Baseline / Config | Audit Mock Claim (Hit@5) | Audit Mock Claim (MRR) | Audit Mock Latency (p50) | Module 1 Empirical Hit@5 | Module 1 Empirical MRR | Module 1 Empirical Latency (p50) | Discrepancy Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **B1: Dense Vector Retrieval** | 72.0% | 0.650 | 120 ms | **1.0% (N=100) / 0.0% (TEST N=15)** | **0.002 (N=100) / 0.000 (TEST N=15)** | **167.88 ms** | **DISPROVED / MOCK FABRICATION** |
| **B2: BM25 Lexical Retrieval** | 68.0% | 0.580 | 45 ms | **0.0% (N=100) / 0.0% (TEST N=15)** | **0.002 (N=100) / 0.000 (TEST N=15)** | **287.74 ms** | **DISPROVED / MOCK FABRICATION** |
| **B3: Hybrid Fusion (RRF k=60)** | 84.0% | 0.780 | 140 ms | **0.0% (N=100) / 0.0% (TEST N=15)** | **0.000 (N=100) / 0.000 (TEST N=15)** | **269.68 ms** | **DISPROVED / MOCK FABRICATION** |
| **B4: Hybrid + BGE Reranker** | 91.0% | 0.860 | 310 ms | **0.0% (N=100) / 0.0% (TEST N=15)** | **0.000 (N=100) / 0.000 (TEST N=15)** | **1.39 ms (bypass)** | **DISPROVED / MOCK FABRICATION** |

---

## 3. Key Findings & Research Integrity Conclusions

1. **Complete Removal of Mock Simulation Logic**:
   - `evaluation_service.py` no longer contains pseudo-random latency generation or artificial metric returns.
   - All evaluations execute real DB queries and execute live `LocalEvidenceRetriever` calls.

2. **Root Causes of Empirical Metric Differences**:
   - **Legacy Audit Mock Metrics**: Were hardcoded values (`0.91`, `0.84`, `0.72`) written into `evaluation_service.py` functions without executing index search or evaluating benchmark ground truth.
   - **Empirical Baseline Performance**: Real `LocalEvidenceRetriever` over 100 benchmark items currently yields low Hit@5 / MRR baseline performance on un-tuned corpus chunking.
   - **BGE Reranking Latency**: In `B4_Hybrid_BGE`, when 0 top-K candidates are retrieved from candidate fusion, reranking is short-circuited in ~1.39 ms rather than taking 310 ms.

3. **Publication Impact**:
   - The paper cannot cite 91.0% Hit@5 or 0.860 MRR.
   - Real baseline metrics must be reported as the true pre-optimization baseline for Module 1.
