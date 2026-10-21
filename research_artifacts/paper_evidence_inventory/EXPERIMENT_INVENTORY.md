# Experiment Inventory Report

## 1. Overview

This document categorizes all completed and unexecuted retrieval, reranking, and generation experiments in ResearchNexus.

---

## 2. Completed & Verified Experiments

1. **E01 Baseline Retrieval (`ds_nexus_v11`)**:
   - **Configurations**: B1_Dense (Chroma), B2_BM25, B3_Hybrid_RRF ($k=60$).
   - **Sample Size**: $N=100$ (70 DEV, 15 VAL, 15 TEST).
   - **Artifacts**: `e01_raw_per_query.json`, `e01_aggregate_results.json`, `figure_1_e01_retrieval.csv`, `table_e01_test_results.csv`.
   - **Publication Status**: **VERIFIED**.

2. **E02 Cross-Encoder Reranking (`ds_nexus_v11`)**:
   - **Configuration**: B4_Hybrid_BGE (`BAAI/bge-reranker-base`).
   - **Sample Size**: $N=100$ (70 DEV, 15 VAL, 15 TEST).
   - **Artifacts**: `e02_raw_per_query.json`, `e02_aggregate_results.json`, `bge_execution_report.md`, `e02_results.md`, `figure_2_e02_reranking.csv`, `table_e02_test_results.csv`.
   - **Publication Status**: **VERIFIED**.

3. **BGE Pure Inference Latency Benchmark**:
   - **Measurement**: Isolated `FlagReranker.compute_score` inference across 1,000 candidate pairs (10 candidates / query).
   - **Artifacts**: `final_latency_analysis.json`, `figure_4_latency.csv`, `table_latency.csv`.
   - **Publication Status**: **VERIFIED** (p50 = 531.41 ms, p95 = 4,246.05 ms).

---

## 3. Unexecuted & Missing Experiments (Module 2 Pipeline)

1. **RAG Baseline Generation (No Verification)**: End-to-end LLM literature synthesis using retrieved context.
2. **Multi-Stage Verified RAG Generation**: LLM synthesis with NLI claims extraction and evidence verification.
3. **Citation Repair / Iterative RAG**: Automatic retrieval correction for unverified or unsupported claims.
4. **Explainable AI (XAI) Attribution Tracing**: Fine-grained provenance mapping from generated text back to SQLite chunk offset.
