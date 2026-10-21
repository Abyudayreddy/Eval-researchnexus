# BGE Execution & Short-Circuit Audit Report

## 1. Executive Summary

In Module 1 evaluation runs (E02), B4 (Hybrid + BGE Reranker) reported a median latency of **1.39 ms (p50)** and **2.25 ms (p95)**.

This forensic audit confirms that these near-instantaneous latencies occurred because BGE Cross-Encoder inference was **bypassed/short-circuited** due to zero candidates returned by upstream hybrid candidate fusion.

---

## 2. Quantitative Execution Breakdown

| Query Subset | Total Queries ($N$) | BGE Candidates Received | Queries Short-Circuited (`BGE_NOT_CALLED`) | Queries Invocated (`BGE_CALLED`) | Avg Latency (BGE_NOT_CALLED) | Avg Latency (BGE_CALLED) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Full Benchmark** | 100 | 0 | **100** | **0** | **1.39 ms** | N/A (0 calls) |
| **TEST Split** | 15 | 0 | **15** | **0** | **1.60 ms** | N/A (0 calls) |

---

## 3. Findings & Integrity Impact

1. **BGE Latency Claims**:
   - Reporting 1.39 ms as "BGE Cross-Encoder Reranking Latency" is **invalid and false**.
   - 1.39 ms represents the overhead of checking an empty candidate array and returning early.

2. **Required Publication Correction**:
   - Claim `BGE reranking has Y ms latency` MUST remain **`NOT VERIFIED`**.
   - BGE inference latency must only be measured and reported on queries where candidates are actually passed to `CrossEncoder.predict()`.
