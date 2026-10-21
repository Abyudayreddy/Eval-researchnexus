# Master Experiment Protocol (Frozen)

## 1. Overview

This document specifies the 11 frozen experiments (E01 through E11) for ResearchNexus.

---

## 2. Frozen Experiment Definitions

| Experiment ID | Experiment Name | Model / Pipeline Configurations | Dataset / Split | Primary Objective |
| :--- | :--- | :--- | :--- | :--- |
| **E01** | Baseline Retrieval Comparison | B1_Dense (Chroma), B2_BM25, B3_Hybrid_RRF ($k=60$) | `ds_nexus_v11` (ALL/DEV/VAL/TEST) | Evaluate baseline lexical vs. dense vs. hybrid retrieval |
| **E02** | Cross-Encoder Reranking | B3_Hybrid vs. B4_Hybrid_BGE (`bge-reranker-base`) | `ds_nexus_v11` (ALL/DEV/VAL/TEST) | Measure impact of BGE reranking under fixed candidate set |
| **E03** | Candidate Recall Curve | Top-$k \in \{5, 10, 20, 50\}$ cutoffs across retrievers | `ds_nexus_v11` (ALL/DEV/VAL/TEST) | Identify candidate recall bottlenecks |
| **E04** | Naive vs. Verified RAG | Naive RAG vs. ResearchNexus Verified RAG | `ds_nexus_v11` (ALL/DEV/VAL/TEST) | Evaluate claim-level grounding under identical context |
| **E05** | Claim Verification Evaluation | NLI Verifier on generated claims | `ds_nexus_v11` (DEV/VAL/TEST) | Measure verification Precision, Recall, F1, FPR, FNR |
| **E06** | Citation Repair Evaluation | Automatic Citation Repair module | `ds_nexus_v11` (DEV/VAL/TEST) | Evaluate Citation Repair Success Rate & unsupported claim delta |
| **E07** | One-Pass vs. Iterative RAG | Single-pass synthesis vs. Multi-pass refinement | `ds_nexus_v11` (DEV/VAL/TEST) | Measure iterative quality gains vs. latency trade-off |
| **E08** | XAI Provenance Evaluation | Full provenance trace extractor | `ds_nexus_v11` (TEST) | Evaluate Trace Completeness & Link Accuracy |
| **E09** | End-to-End Latency | Disaggregated pipeline stage timing | `ds_nexus_v11` (ALL) | Measure p50/p95 latency breakdown across all stages |
| **E10** | System Ablation Study | Full system minus (Reranking / Verification / Repair) | `ds_nexus_v11` (DEV/VAL/TEST) | Isolate component contributions to system accuracy |
| **E11** | Error Taxonomy Analysis | 14-category error classifier | `ds_nexus_v11` (TEST) | Characterize system failure modes |
