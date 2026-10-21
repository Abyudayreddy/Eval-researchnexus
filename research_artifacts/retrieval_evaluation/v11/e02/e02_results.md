# E02 Retrieval Evaluation Results: B3 Hybrid vs B4 Hybrid + BGE Reranker

## 1. Executive Summary

This document reports the comparative baseline evaluation results for **E02 (B4_Hybrid_BGE)** against **B3_Hybrid** on the frozen `ds_nexus_v11` benchmark.

Genuine BGE Cross-Encoder reranking (`BAAI/bge-reranker-base`) was executed across all 100 queries. The empirical results demonstrate significant performance gains over un-reranked hybrid retrieval across ALL and DEVELOPMENT splits.

---

## 2. Comparative Retrieval Performance

### 2.1 Overall Benchmark (`N=100`)

| Baseline / Config | Hit@1 | Hit@5 | Recall@5 | Precision@5 | MRR | NDCG@5 | Latency p50 (ms) | Latency p95 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B3_Hybrid** | 0.0600 | 0.2500 | 0.2200 | 0.0500 | 0.1487 | 0.1280 | 6.56 | 19.12 |
| **B4_Hybrid_BGE** | **0.1500** | **0.5700** | **0.5200** | **0.1140** | **0.2822** | **0.3298** | 535.06 | 4,251.51 |
| **Relative Gain** | **+150.0%** | **+128.0%** | **+136.4%** | **+128.0%** | **+89.8%** | **+157.7%** | — | — |

---

### 2.2 Split-by-Split Performance breakdown

#### DEVELOPMENT Split (`N=70`)
- **Hit@1**: B3 (0.0571) $\rightarrow$ B4 (**0.1857**) [**+225.2%**]
- **Hit@5**: B3 (0.2714) $\rightarrow$ B4 (**0.6714**) [**+147.4%**]
- **Recall@5**: B3 (0.2714) $\rightarrow$ B4 (**0.6714**) [**+147.4%**]
- **MRR**: B3 (0.1613) $\rightarrow$ B4 (**0.3379**) [**+109.5%**]
- **NDCG@5**: B3 (0.1497) $\rightarrow$ B4 (**0.4195**) [**+180.2%**]

#### VALIDATION Split (`N=15`)
- **Hit@1**: B3 (0.1333) $\rightarrow$ B4 (**0.1333**) [Unchanged]
- **Hit@5**: B3 (0.4000) $\rightarrow$ B4 (**0.6667**) [**+66.7%**]
- **MRR**: B3 (0.2383) $\rightarrow$ B4 (**0.3044**) [**+27.7%**]
- **NDCG@5**: B3 (0.1543) $\rightarrow$ B4 (**0.2410**) [**+56.2%**]

#### TEST Split (`N=15`)
- **Hit@1 / Hit@5 / MRR / NDCG@5**: 0.0000 across both B3 and B4.
- **Rank Movement Analysis**: All 10 TEST queries (items `v11_086` to `v11_095`) had gold evidence chunks outside the top-10 hybrid RRF candidate set (`pre_bge_rank = N/A`, `movement = not_present`). Because BGE reranks only top-10 candidates, BGE could not elevate gold evidence into top-5 for TEST queries.

---

## 3. Key Research Insights

1. **BGE Cross-Encoder Impact**: Reranking top-10 candidates with `BAAI/bge-reranker-base` dramatically improves precision, MRR, and NDCG@5 (more than doubling Hit@5 from 0.25 to 0.57 overall).
2. **Candidate Recall Bottleneck on TEST Split**: Reranking cannot recover evidence if initial retriever stages (BM25 + Dense) produce 0 recall in top-10 candidates. This establishes a clear baseline mandate for future retrieval stages (Module 2+).
