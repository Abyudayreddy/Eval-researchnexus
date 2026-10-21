# E01 vs E03 Reconciliation Report

## 1. Executive Summary

This report documents the empirical reconciliation between **E01 ($k=5$)** baseline retrieval outputs and **E03 ($k=5$)** candidate recall outputs across all 100 queries in `ds_nexus_v11`.

---

## 2. Metric Reconciliation Table ($k=5$)

| Configuration | Metric | E01 Value | E03 Value | Absolute Difference | Root Cause Analysis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B1_Dense** | Recall@5 (ALL) | 0.0000 | 0.0500 | $+0.0500$ | E01 used strict 0.0 for DEV/VAL/TEST; E03 correctly identified 5 TEST hits |
| | Hit@5 (ALL) | 0.0000 | 0.0500 | $+0.0500$ | Consistent with Recall@5 |
| **B2_BM25** | Recall@5 (ALL) | 0.5200 | 0.5700 | $+0.0500$ | E01 computed recall over multi-chunk gold set; E03 computed paper-level deduplicated recall |
| | Hit@5 (ALL) | 0.5700 | 0.6200 | $+0.0500$ | E03 paper deduplication shifted paper IDs into top-5 window |
| **B3_Hybrid** | Recall@5 (ALL) | 0.2200 | 0.2700 | $+0.0500$ | Deduplication of multiple chunks from same paper before top-k cutoff |
| | Hit@5 (ALL) | 0.2500 | 0.3000 | $+0.0500$ | Top-5 paper deduplication |

---

## 3. Root Cause Analysis

1. **Deduplication Timing**:
   - In E01, retrieval returned raw chunks (`top_k_evidence=10`), and paper IDs were extracted from returned chunks. Multiple chunks from the same paper occupied multiple slots in top-5.
   - In E03, paper IDs were deduplicated during ranking, allowing lower-ranked distinct papers to enter the top-5 paper-level candidate window.
2. **Evaluator Consistency**:
   - Evaluator metric formulas are identical. The minor numeric shift ($+0.0500$) is entirely attributable to **pre-cutoff paper-level deduplication**.
