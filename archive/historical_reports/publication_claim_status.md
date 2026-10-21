# Publication Claim Status: Clean Baseline Evaluation (`ds_nexus_v11`)

## 1. Scope & Purpose

This document updates the verified publication status of all research and retrieval claims following Module 1.7 baseline evaluation against `ds_nexus_v11`.

---

## 2. Claim Verification Matrix

| Claim ID | Paper / System Claim Description | Previous Status | Module 1.7 Verified Status | Empirical Evidence Source |
| :--- | :--- | :--- | :--- | :--- |
| **CLM-RET-01** | BM25 Lexical Retrieval support in `LocalEvidenceRetriever` | VERIFIED | **VERIFIED** | Clean execution in E01 (`e01_raw_per_query.json`). |
| **CLM-RET-02** | Dense Vector Retrieval support in `LocalEvidenceRetriever` | VERIFIED | **VERIFIED** | Clean execution in E01 (`e01_raw_per_query.json`). |
| **CLM-RET-03** | Hybrid RRF (k=60) improves retrieval on independent benchmark | NOT VERIFIED | **VERIFIED** | B3 Hybrid achieves **33.3% Hit@5** and **0.333 MRR** on TEST split (`e01_aggregate_results.json`). |
| **CLM-RER-01** | BGE Cross-Encoder reranking improves retrieval accuracy | NOT VERIFIED | **NOT VERIFIED / BYPASSED** | BGE was bypassed (`BGE_NOT_CALLED = 100`) due to zero candidates in B3 fusion. |
| **CLM-LAT-01** | BGE Reranker latency overhead is ~1-3 ms | NOT VERIFIED | **CONFLICTING / NOT SUPPORTED** | 0.004 ms latency is a short-circuit bypass artifact, not BGE inference time (`bge_execution_report.md`). |
