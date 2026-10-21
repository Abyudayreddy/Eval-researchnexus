# Latency Instrumentation Audit Report

## 1. Overview

This document records the verification of latency instrumentation boundaries in the ResearchNexus retrieval evaluation pipeline.

---

## 2. Disaggregated Latency Quantities

| Quantity ID | Latency Measurement Quantity | Code Boundary Scope | Sample Size | p50 (ms) | p95 (ms) | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Quantity A** | **Hybrid Retrieval Latency** | `retrieve_hybrid_rrf` (BM25 + Dense + RRF fusion) | 100 | 6.56 | 19.12 | `VERIFIED_VALID` |
| **Quantity B** | **Pure BGE Inference Latency** | `FlagReranker.compute_score` inference time | 100 | **531.41** | **4,246.05** | `VERIFIED_GENUINE_BGE` |
| **Quantity C** | **Total Stage Latency** | `rerank_and_build_evidence` end-to-end time | 100 | 535.06 | 4,251.51 | `VERIFIED_VALID` |

---

## 3. Permanently Classified Historical Bypass

> The previous `~0.004 ms` bypass measurement remains permanently classified as **`INVALID_BYPASS_LATENCY`** and must NEVER be used as actual BGE model inference time.
