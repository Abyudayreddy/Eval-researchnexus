# Metric Inventory Report

## 1. Overview

This document lists all evaluated retrieval and generation metrics, specifying their data source, audit status, and publication usability.

---

## 2. Metric Inventory Table

| Metric Name | Scope / Split | Measured Value (B3 Hybrid) | Measured Value (B4 Hybrid+BGE) | Data Source | Verification Status | Publication Usability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hit@1** | ALL ($N=100$) | 0.0600 | 0.1500 | Raw JSON | `VERIFIED` | YES |
| | DEV ($N=70$) | 0.0571 | 0.1857 | Raw JSON | `VERIFIED` | YES |
| | **TEST ($N=15$)** | **0.0000** | **0.0000** | Raw JSON | `VERIFIED` | YES |
| **Hit@5** | ALL ($N=100$) | 0.2500 | 0.5700 | Raw JSON | `VERIFIED` | YES |
| | DEV ($N=70$) | 0.2714 | 0.6714 | Raw JSON | `VERIFIED` | YES |
| | **TEST ($N=15$)** | **0.0000** | **0.0000** | Raw JSON | `VERIFIED` | YES |
| **Recall@5** | ALL ($N=100$) | 0.2200 | 0.5200 | Raw JSON | `VERIFIED` | YES |
| | DEV ($N=70$) | 0.2714 | 0.6714 | Raw JSON | `VERIFIED` | YES |
| | **TEST ($N=15$)** | **0.0000** | **0.0000** | Raw JSON | `VERIFIED` | YES |
| **MRR** | ALL ($N=100$) | 0.1487 | 0.2822 | Raw JSON | `VERIFIED` | YES |
| | DEV ($N=70$) | 0.1613 | 0.3379 | Raw JSON | `VERIFIED` | YES |
| | **TEST ($N=15$)** | **0.0000** | **0.0000** | Raw JSON | `VERIFIED` | YES |
| **NDCG@5** | ALL ($N=100$) | 0.1280 | 0.3298 | Raw JSON | `VERIFIED` | YES |
| | DEV ($N=70$) | 0.1497 | 0.4195 | Raw JSON | `VERIFIED` | YES |
| | **TEST ($N=15$)** | **0.0000** | **0.0000** | Raw JSON | `VERIFIED` | YES |
| **Pure BGE Latency p50** | ALL ($N=100$) | N/A | 531.41 ms | `final_latency_analysis.json` | `VERIFIED` | YES |
| **Pure BGE Latency p95** | ALL ($N=100$) | N/A | 4,246.05 ms | `final_latency_analysis.json` | `VERIFIED` | YES |
| **RAG Synthesis Faithfulness** | N/A | N/A | N/A | None | `NOT_TESTED` | NO |
| **Citation Precision / Recall** | N/A | N/A | N/A | None | `NOT_TESTED` | NO |
