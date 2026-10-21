# Minimal Defensible System Ablation Plan (Frozen)

## 1. Overview

This document specifies the minimal defensible ablation matrix to isolate component contributions.

---

## 2. Ablation Configurations Matrix

| Config ID | Configuration Name | Hybrid RRF | BGE Reranker | NLI Verification | Citation Repair | Iterative Refinement | Target Evaluation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A0 (Full)** | **ResearchNexus Full System** | ON | ON | ON | ON | ON | Full System Benchmark |
| **A1** | w/o Iterative Refinement | ON | ON | ON | ON | OFF | Measure iteration gain |
| **A2** | w/o Citation Repair | ON | ON | ON | OFF | OFF | Measure repair impact |
| **A3** | w/o NLI Verification (Naive RAG) | ON | ON | OFF | OFF | OFF | Measure verification impact |
| **A4** | w/o BGE Reranker | ON | OFF | OFF | OFF | OFF | Measure reranking impact |
| **A5** | Dense Only Baseline | OFF (Dense) | OFF | OFF | OFF | OFF | Single retrieval baseline |
| **A6** | BM25 Only Baseline | OFF (BM25) | OFF | OFF | OFF | OFF | Single retrieval baseline |
