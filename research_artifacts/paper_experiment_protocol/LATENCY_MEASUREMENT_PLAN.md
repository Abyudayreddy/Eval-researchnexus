# Latency Measurement Plan (Frozen)

## 1. Overview

This document specifies the timing measurement boundaries and reporting requirements for pipeline latency.

---

## 2. Timing Boundaries

| Stage ID | Pipeline Stage Scope | Start Boundary | Stop Boundary | Reported Metrics |
| :--- | :--- | :--- | :--- | :--- |
| **S01** | Query Processing | Input query string receipt | Tokenization / normalization completion | $N$, p50, p95 (ms) |
| **S02** | BM25 Lexical Retrieval | BM25 query invocation | Top-10 candidate return | $N$, p50, p95 (ms) |
| **S03** | Dense Chroma Retrieval | Dense embedding + vector query | Top-10 candidate return | $N$, p50, p95 (ms) |
| **S04** | Hybrid RRF Fusion | Reciprocal rank calculation | Merged candidate list return | $N$, p50, p95 (ms) |
| **S05** | BGE Reranking | Candidate text hydration start | BGE score computation & reordering | $N$, p50, p95 (ms) |
| **S06** | LLM Synthesis Generation | Prompt assembly & LLM call start | Full generation completion | $N$, p50, p95 (ms) |
| **S07** | NLI Claim Verification | Claim extraction & verifier call | Verification label assignment | $N$, p50, p95 (ms) |
| **S08** | Citation Repair | Iterative retrieval / repair start | Final citation update completion | $N$, p50, p95 (ms) |
| **S09** | End-to-End Pipeline | Query input submission | Final verified response output | $N$, p50, p95 (ms) |
