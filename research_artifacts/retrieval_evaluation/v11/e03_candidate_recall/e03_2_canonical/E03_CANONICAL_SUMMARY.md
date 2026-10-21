# Authoritative E03 Canonical Summary (E03.2)

## 1. Executive Summary

This document presents the official, canonical retrieval evaluation metrics for ResearchNexus under **Paper-Level Deduplicated Semantics**.

All metrics are recomputed directly from raw retrieval outputs and frozen benchmark gold labels (`ds_nexus_v11`).

---

## 2. Authoritative Canonical Metrics Across Benchmark Splits

### 2.1 Benchmark Overall (`N=100`)

| Configuration | Metric | $k=5$ | $k=10$ | $k=20$ | $k=50$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B1_Dense** | **Recall@k** | 0.0500 | 0.0500 | 0.0500 | 0.0500 |
| | **Hit@k** | 0.0500 | 0.0500 | 0.0500 | 0.0500 |
| **B2_BM25** | **Recall@k** | 0.5700 | 0.9500 | 0.9750 | **1.0000** |
| | **Hit@k** | 0.6200 | **1.0000** | 1.0000 | 1.0000 |
| **B3_Hybrid_RRF** | **Recall@k** | 0.2700 | 0.5700 | **0.9500** | **1.0000** |
| | **Hit@k** | 0.3000 | 0.6200 | **1.0000** | 1.0000 |

---

### 2.2 Primary Publication TEST Split (`N=15`)

| Configuration | Metric | $k=5$ | $k=10$ | $k=20$ | $k=50$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B1_Dense** | **Recall@k** | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| | **Hit@k** | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| **B2_BM25** | **Recall@k** | 0.0000 | 0.6667 | 0.8333 | **1.0000** |
| | **Hit@k** | 0.0000 | 0.6667 | 0.8333 | **1.0000** |
| **B3_Hybrid_RRF** | **Recall@k** | 0.0000 | 0.0000 | **0.6667** | **1.0000** |
| | **Hit@k** | 0.0000 | 0.0000 | **0.6667** | **1.0000** |

---

## 3. Authoritative Downstream E04 Generation Eligibility

| Context Cutoff ($k$) | Benchmark Overall ($N=100$) | TEST Split ($N=15$) | RAG Generation Context Status |
| :--- | :--- | :--- | :--- |
| **Top-5 Context ($k=5$)** | **25 / 100 (25.0%)** | **0 / 15 (0.0%)** | Strict small context window |
| **Top-10 Context ($k=10$)** | **57 / 100 (57.0%)** | **0 / 15 (0.0%)** | Standard RAG context window |
| **Top-20 Context ($k=20$)** | **95 / 100 (95.0%)** | **10 / 15 (66.7%)** | Deep RAG context window |
| **Top-50 Context ($k=50$)** | **95 / 100 (95.0%)** | **10 / 15 (66.7%)** | Max candidate pool depth |
