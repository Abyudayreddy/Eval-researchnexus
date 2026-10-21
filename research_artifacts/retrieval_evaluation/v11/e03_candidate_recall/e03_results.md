# E03 Candidate Recall Curve Results & Analysis

## 1. Executive Summary

This report documents the empirical findings of **E03: Candidate Recall Curve Experiment** on `ds_nexus_v11`.

---

## 2. Candidate Recall & Hit Rates Across Cutoffs ($k \in \{5, 10, 20, 50\}$)

### 2.1 Overall Benchmark (`N=100`)

| Retriever | Metric | $k=5$ | $k=10$ | $k=20$ | $k=50$ | Latency p50 ($k=50$) | Latency p95 ($k=50$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B1_Dense** | **Recall@k** | 0.0500 | 0.0500 | 0.0500 | 0.0500 | 11.38 ms | 35.82 ms |
| | **Hit@k** | 0.0500 | 0.0500 | 0.0500 | 0.0500 | — | — |
| **B2_BM25** | **Recall@k** | 0.5700 | 0.9500 | 0.9750 | **1.0000** | 1.05 ms | 1.83 ms |
| | **Hit@k** | 0.6200 | **1.0000** | 1.0000 | 1.0000 | — | — |
| **B3_Hybrid_RRF** | **Recall@k** | 0.2700 | 0.5700 | 0.9500 | **1.0000** | 14.29 ms | 20.06 ms |
| | **Hit@k** | 0.3000 | 0.6200 | **1.0000** | 1.0000 | — | — |

---

### 2.2 Primary Publication TEST Split (`N=15`)

| Retriever | Metric | $k=5$ | $k=10$ | $k=20$ | $k=50$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B1_Dense** | **Recall@k** | 0.3333 | 0.3333 | 0.3333 | 0.3333 |
| **B2_BM25** | **Recall@k** | 0.3333 | **1.0000** | 1.0000 | **1.0000** |
| **B3_Hybrid_RRF** | **Recall@k** | 0.3333 | 0.3333 | **1.0000** | **1.0000** |
| **B3_Hybrid_RRF** | **Hit@k** | 0.3333 | 0.3333 | **1.0000** | **1.0000** |

---

## 3. `first_gold_k` Diagnostic Distribution (`N=100`)

| Retriever | $k=5$ | $k=10$ | $k=20$ | $k=50$ | Never (by $k=50$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B1_Dense** | 5 (5.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 95 (95.0%) |
| **B2_BM25** | 62 (62.0%) | 38 (38.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| **B3_Hybrid_RRF** | 30 (30.0%) | 32 (32.0%) | 38 (38.0%) | 0 (0.0%) | 0 (0.0%) |

---

## 4. Key Downstream Impact on BGE Reranking & Evidence-Eligible Cohort

1. **Top-5 Context Evidence Eligibility**: Under a generation context window of $k=5$, B3_Hybrid_RRF provides **30.0% evidence eligibility** (30/100 queries have gold context in top-5). On the TEST split ($N=15$), exactly 5 queries (33.3%) are evidence-eligible under $k=5$.
2. **Top-10 Reranking Candidate Bottleneck**: Under $k=10$, B3_Hybrid_RRF reaches **62.0% Hit@10** overall and **33.3% Hit@10** on TEST (5/15 items).
3. **Deep Retrieval Recovery ($k=20$)**: Expanding candidate depth to $k=20$ elevates B3_Hybrid_RRF Recall@20 to **95.0% overall** and **100.0% on TEST ($N=15$)**.

---

## 5. Status Verdict

```
E03_STATUS = VERIFIED
```
