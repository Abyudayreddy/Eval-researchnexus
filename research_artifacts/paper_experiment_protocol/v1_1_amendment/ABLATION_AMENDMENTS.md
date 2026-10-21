# Ablation Amendments (V1.1 Amendment)

## 1. Executive Summary & Rationale

In V1.0, ablation configurations A1–A4 contained confounded component combinations. V1.1 replaces the ablation matrix with single-factor interventions that isolate each component relative to the Full ResearchNexus pipeline (A0).

---

## 2. Corrected System Ablation Matrix

| Config ID | Configuration Name | Hybrid RRF | BGE Reranker | NLI Verification | Citation Repair | Iterative Refinement | Component Isolated by Comparison |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A0 (Full)** | **ResearchNexus Full System** | **ON** | **ON** | **ON** | **ON** | **ON** | Reference Full Pipeline |
| **A1** | Full - Iteration | ON | ON | ON | ON | **OFF** | Isolates **Iterative Refinement** ($A0 \text{ vs. } A1$) |
| **A2** | Full - Citation Repair | ON | ON | ON | **OFF** | ON | Isolates **Citation Repair** ($A0 \text{ vs. } A2$) |
| **A3** | Naive RAG Baseline | ON | ON | **OFF** | **OFF** | **OFF** | Isolates **Full Verification & Repair Pipeline** ($A0 \text{ vs. } A3$) |
| **A4** | Full - BGE Reranker | ON | **OFF** | ON | ON | ON | Isolates **BGE Cross-Encoder Reranking** ($A0 \text{ vs. } A4$) |
| **A5** | Dense Only Baseline | OFF (Dense) | OFF | OFF | OFF | OFF | Dense-only retrieval baseline |
| **A6** | BM25 Only Baseline | OFF (BM25) | OFF | OFF | OFF | OFF | BM25-only retrieval baseline |
