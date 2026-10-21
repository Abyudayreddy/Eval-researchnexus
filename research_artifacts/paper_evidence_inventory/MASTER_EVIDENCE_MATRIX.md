# Master Evidence Matrix

## 1. Overview

This document contains the complete evidence inventory for the ResearchNexus working paper:
*“ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis”*

Every experimental output, dataset manifest, and metric computation across the repository has been audited, categorized, and assigned an explicit publication verification status.

---

## 2. Inventory Evidence Matrix

| Artifact Path | Experiment Name | Dataset / Version | Split Scope | Sample Size ($N$) | Model / Configuration | Measured Metrics | Raw vs. Derived | Verification Status | Publication Usability | Known Limitations | Dependent Publication Claims |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `benchmark_v11/test_manifest.json` | v11 Benchmark Freeze | `ds_nexus_v11` | TEST | 15 | Frozen SQLite & Chroma | SHA256 integrity hash (`91a38a...`) | Raw | `VERIFIED` | YES | 15 items in TEST split | CLAIM-02 |
| `v11/e01/raw/e01_raw_per_query.json` | E01 Clean Baseline Retrieval | `ds_nexus_v11` | ALL / DEV / VAL / TEST | 100 | B1_Dense, B2_BM25, B3_Hybrid_RRF | Hit@1, Hit@5, Recall@5, Prec@5, MRR, NDCG@5, Latency | Raw | `VERIFIED` | YES | 0.0 recall on TEST top-10 candidates | CLAIM-01, CLAIM-03 |
| `v11/e02/raw/e02_raw_per_query.json` | E02 Genuine BGE Reranking | `ds_nexus_v11` | ALL / DEV / VAL / TEST | 100 | B4_Hybrid_BGE (`bge-reranker-base`) | Hit@1, Hit@5, Recall@5, Prec@5, MRR, NDCG@5, BGE Latency | Raw | `VERIFIED` | YES | TEST Hit@5 = 0.0000 (pre-candidate recall bottleneck) | CLAIM-04, CLAIM-05, CLAIM-06 |
| `v11/final_latency_analysis.json` | Pure BGE Inference Latency | `ds_nexus_v11` | ALL | 100 | BAE/bge-reranker-base (10 pairs/query) | `bge_p50_ms` = 531.41ms, `bge_p95_ms` = 4246.05ms | Derived | `VERIFIED` | YES | Measured on single-thread CPU environment | CLAIM-07 |
| `e02_aggregate_results.json` (Legacy) | Legacy BGE Bypass Overhead | `ds_nexus_v10` / early `v11` | ALL | 100 | BGE (Bypassed due to empty text array) | Latency = ~0.004 ms | Derived | `INVALID_DO_NOT_USE` | NO | Measured empty array return overhead, not BGE model inference | Permanently classified as INVALID_BYPASS_LATENCY |
| `module_1_5/diagnostic_matrix.csv` | Legacy v10 Retrieval Audit | `ds_nexus_v10` | ALL | 100 | BM25 / Dense / Hybrid | Hit@1, Hit@5, Recall@5, MRR, NDCG@5 | Derived | `INVALID_DO_NOT_USE` | NO | Synthetic query template mismatch & retriever-dependent labels | Retired legacy benchmark |
| `v11/e02_statistical_analysis.json` | E02 Paired Statistical Testing | `ds_nexus_v11` | DEVELOPMENT | 70 | B3_Hybrid vs B4_Hybrid_BGE | Paired t-test $t=5.63, p=3.61e-7$ (NDCG@5) | Derived | `VERIFIED_WITH_LIMITATION` | YES (DEV scoped) | Significant on DEV ($N=70$); zero-variance on TEST ($N=15$) | CLAIM-06 |
| `module_1_9_1/independently_verified_rank_movement.json` | Genuine Rank Movement | `ds_nexus_v11` | ALL / DEV / VAL / TEST | 100 | B3 vs B4 Reranking | 42 Improved (42%), 2 Unchanged (2%), 8 Worsened (8%), 48 Absent | Derived | `VERIFIED` | YES | 100% of TEST gold items remained absent from top-10 candidates | CLAIM-06 |
| `backend/app/services/rag_service.py` | Multi-Stage RAG Synthesis | N/A | N/A | 0 | LLM Generation / Hallucination Verification | None (Not evaluated) | N/A | `NOT_TESTED` | NO | Code implementation exists, but zero evaluation artifacts exist | CLAIM-08 |
