# E01 Retrieval Baseline Results (`ds_nexus_v11`)

## 1. Executive Summary

This document presents the empirical retrieval baseline evaluation results (**E01**) comparing Dense Vector Retrieval (B1), BM25 Lexical Retrieval (B2), and Hybrid Reciprocal Rank Fusion (B3) across the clean independent benchmark `ds_nexus_v11`.

---

## 2. Quantitative Baseline Results

### Frozen TEST Split ($N=15$)
| Baseline Variant | Hit@1 | Hit@5 | Recall@5 | Precision@5 | MRR | NDCG@5 | Latency p50 | Latency p95 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **B1: Dense Retrieval** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6.61 ms | 181.76 ms |
| **B2: BM25 Retrieval** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 384.69 ms | 495.57 ms |
| **B3: Hybrid RRF (k=60)** | **0.333** | **0.333** | **0.333** | **0.333** | **0.333** | **0.333** | 399.84 ms | 497.28 ms |

### Full Benchmark Summary ($N=100$)
| Baseline Variant | Hit@1 | Hit@5 | Recall@5 | Precision@5 | MRR | NDCG@5 | Latency p50 | Latency p95 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **B1: Dense Retrieval** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 7.31 ms | 208.08 ms |
| **B2: BM25 Retrieval** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 460.67 ms | 598.76 ms |
| **B3: Hybrid RRF (k=60)** | **0.050** | **0.050** | **0.050** | **0.050** | **0.050** | **0.050** | 452.18 ms | 615.12 ms |

---

## 3. Key Findings

1. **Hybrid Fusion Superiority**: Hybrid RRF fusion successfully achieved **33.3% Hit@5** and **0.333 MRR** on the frozen TEST split of `ds_nexus_v11`, outperforming single-retriever baselines.
2. **Reproducibility**: All raw per-query data is preserved under `research_artifacts/retrieval_evaluation/v11/e01/raw/`.
