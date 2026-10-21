# ResearchNexus Publication Claim Status Tracking

## 1. Overview

This document tracks the official verification status of publication claims for the working paper:
*“ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis”*

All statuses are assigned based strictly on empirical evidence generated from the frozen **`ds_nexus_v11`** benchmark during **Module 1 Final Closure Audit**.

---

## 2. Claim Verification Matrix

| Claim ID | Claim Description | Benchmark Scope & Metrics | Status | Supporting Evidence Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **CLAIM-01** | Real Retrieval Evaluation Infrastructure | Non-simulated metric evaluation engine | **VERIFIED** | [e01_test_publication_results.json](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e01_test_publication_results.json) |
| **CLAIM-02** | Independent Benchmark Frozen State | `ds_nexus_v11` SHA256 frozen test set | **VERIFIED** | [ds_nexus_v11_manifest.json](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/benchmark_v11/ds_nexus_v11_manifest.json) |
| **CLAIM-03** | Clean Baseline Retrieval Evaluation (E01) | BM25, Dense, Hybrid RRF baseline results | **VERIFIED** | [e01_test_publication_results.json](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e01_test_publication_results.json) |
| **CLAIM-04** | Candidate Text Hydration Contract | SQLite `PaperChunk` text hydration before BGE | **VERIFIED** | [candidate_contract_audit.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e02/candidate_contract_audit.md) |
| **CLAIM-05** | Genuine BGE Reranker Execution | 100/100 non-bypassed Cross-Encoder calls | **VERIFIED** | [bge_execution_report.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e02/bge_execution_report.md) |
| **CLAIM-06** | BGE Reranker Performance Gains (Overall/DEV) | Hit@5 0.25 $\rightarrow$ 0.57 (ALL), 0.27 $\rightarrow$ 0.67 (DEV) | **VERIFIED_WITH_LIMITATIONS** | [e02_statistical_analysis.json](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e02_statistical_analysis.json) ($p=3.61 \times 10^{-7}$ on DEV; 0.0 recall on TEST) |
| **CLAIM-07** | Pure BGE Model Inference Latency | Isolated Cross-Encoder model latency | **VERIFIED** | [final_latency_analysis.json](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/final_latency_analysis.json) (`bge_p50_ms` = 531.41 ms, `bge_p95_ms` = 4,246.05 ms) |
| **CLAIM-08** | Multi-Stage RAG Synthesis & Verification | RAG generation, claim verification, UI | `PENDING_MODULE_2` | Awaiting Module 2 implementation |

---

## 3. Verified Claim Statements for Paper Draft

1. **Overall/DEV Reranking Gain**: *"On the development split of ds_nexus_v11 (N=70), BAE/bge-reranker-base Cross-Encoder reranking significantly improved Hybrid RRF NDCG@5 from 0.1497 to 0.4195 (paired t-test $t=5.63$, $p=3.61 \times 10^{-7}$) and MRR from 0.1613 to 0.3379 ($p=2.73 \times 10^{-4}$)."*
2. **Test Set Limitation**: *"On the primary frozen test split (N=15), all 15 queries exhibited zero top-10 candidate recall across dense and BM25 baseline retrievers, resulting in 0.0000 Hit@5, MRR, and NDCG@5 for both un-reranked and reranked pipelines."*
3. **Inference Latency**: *"Pure BGE Cross-Encoder inference latency across 100 benchmark queries averaged a median p50 of 531.41 ms and a p95 of 4,246.05 ms (10 candidates per query)."*

---

## 4. Module 1 Final Closure Verdict

**MODULE_1_PUBLICATION_STATUS**: **`READY_WITH_LIMITATIONS`**
