# Module 1: Historical vs Controlled Results Reconciliation

This document explicitly contrasts historical evaluation artifacts against the newly generated, controlled Module 1 results.

---

## 1. Metric Comparison Table (Frozen TEST Split, $N=15$)

| Configuration | Metric | Historical Value | Controlled Module 1 Value | Same Protocol? | Same Entity Level? | Same Benchmark? | Reusable? | Root Cause Analysis & Reconciliation |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **B1: BM25** | Paper MRR | 0.0759 | **0.0759** | YES | YES | YES | **REUSABLE** | Exact match. BM25 scoring and ranking identical. |
| **B1: BM25** | Paper Hit@5 | 0.0000 | **0.0000** | YES | YES | YES | **REUSABLE** | Exact match. Gold paper sits at rank 8–9, outside top 5. |
| **B1: BM25** | Paper Recall@10 | 1.0000 | **1.0000** | YES | YES | YES | **REUSABLE** | Gold paper appears within top 10 for all 10 answerable queries. |
| **B1: BM25** | Paper Recall@20 | 1.0000 | **1.0000** | YES | YES | YES | **REUSABLE** | Exact match. |
| **B2: Dense** | Paper MRR | 0.0000 | **0.0000** | YES | YES | YES | **REUSABLE** | Exact match. Dense alone fails to retrieve gold papers for these numerical queries. |
| **B2: Dense** | Paper Recall@20 | 0.0000 | **0.0000** | YES | YES | YES | **REUSABLE** | Dense candidate pool lacks gold items in top 50. |
| **B3: Hybrid RRF** | Paper MRR | 0.0431 | **0.0431** | YES | YES | YES | **REUSABLE** | Exact match. RRF ranks gold papers at ranks 15–17. |
| **B3: Hybrid RRF** | Paper Recall@20 | 1.0000 | **1.0000** | YES | YES | YES | **REUSABLE** | Exact match with E03.3 canonical live table. |
| **B4: BGE Reranked**| Paper MRR | — | **0.0480** | CONTROLLED | YES | YES | **CONTROLLED** | BGE reranks candidates in top 20, slightly boosting MRR from 0.0431 to 0.0480. |
| **B4: BGE Reranked**| Paper Recall@20 | — | **1.0000** | CONTROLLED | YES | YES | **CONTROLLED** | Cross-encoder retains 100% candidate recall at $k=20$. |

---

## 2. Key Insights
1. **Perfect Consistency with Canonical E03.3**:
   The newly executed Module 1 evaluation perfectly replicates the canonical metrics recorded in `e03_3_canonical_results_live.json` and `table_e01_test_results.csv`.
2. **Resolution of the Stale Metric Ambiguity**:
   The old historical confusion where BM25 had Recall@5 = 0.0000 in E01 but Recall@10 = 1.0000 in E03 is now fully explained by the rank forensic analysis: the gold papers sit strictly at ranks 8 and 9 under BM25, perfectly bridging the gap between $K=5$ and $K=10$.
