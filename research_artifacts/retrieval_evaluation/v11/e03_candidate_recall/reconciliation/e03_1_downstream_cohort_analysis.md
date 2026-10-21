# Downstream E04 Cohort Analysis & Recommendation Report

## 1. Overview

This report provides the evidence-based downstream cohort analysis for E04 (Naive vs. Verified RAG) based on the corrected E03.1 `first_gold_k` distribution.

---

## 2. Evidence-Eligible Query Counts Across Cutoffs (`B3_Hybrid_RRF`)

| Context Depth Cutoff ($k$) | Benchmark Overall ($N=100$) | TEST Split ($N=15$) | Downstream RAG Context Characterization |
| :--- | :--- | :--- | :--- |
| **Top-5 Context ($k=5$)** | **25 / 100 (25.0%)** | **0 / 15 (0.0%)** | Strict small context window; 0 TEST items contain gold evidence |
| **Top-10 Context ($k=10$)** | **57 / 100 (57.0%)** | **0 / 15 (0.0%)** | Standard RAG context window; 0 TEST items contain gold evidence |
| **Top-20 Context ($k=20$)** | **95 / 100 (95.0%)** | **10 / 15 (66.7%)** | Deep RAG context window; 10 TEST items contain gold evidence |
| **Top-50 Context ($k=50$)** | **95 / 100 (95.0%)** | **10 / 15 (66.7%)** | Max candidate pool depth |

---

## 3. Methodological Recommendation for E04

> **Recommendation**: For E04 generation evaluation, supply top-20 retrieved context ($k=20$) or run a dual-context comparison ($k=5$ vs. $k=20$). At $k=20$, **95% of overall queries** and **66.7% of TEST queries** are evidence-eligible, eliminating the 0-recall bottleneck while preserving controlled generation comparison rules.
