# Publication Claim-Evidence Mapping Report

## 1. Overview

This document maps every publication claim of ResearchNexus directly to its underlying experimental artifacts.

---

## 2. Claim Evidence Mapping Matrix

| Claim ID | Claim Statement | Verification Status | Primary Supporting Artifact | Empirical Key Result |
| :--- | :--- | :--- | :--- | :--- |
| **CLAIM-01** | Real non-simulated retrieval evaluation pipeline | **VERIFIED** | `v11/e01/raw/e01_raw_per_query.json` | 100 queries evaluated dynamically against SQLite & Chroma |
| **CLAIM-02** | Independent, frozen scientific benchmark (`ds_nexus_v11`) | **VERIFIED** | `benchmark_v11/test_manifest.json` | SHA256 frozen test set hash (`91a38a...`), 100 items from 40 ArXiv papers |
| **CLAIM-03** | Clean baseline retrieval evaluation (E01) | **VERIFIED** | `v11/e01_test_publication_results.json` | BM25 Hit@5=0.57 (ALL), Hybrid Hit@5=0.25 (ALL), Dense Hit@5=0.0 |
| **CLAIM-04** | Candidate schema & database text hydration contract | **VERIFIED** | `v11/e02/candidate_contract_audit.md` | 100% of candidate IDs mapped to non-empty SQLite `PaperChunk` texts |
| **CLAIM-05** | Genuine BGE Cross-Encoder reranking execution | **VERIFIED** | `v11/e02/bge_execution_report.md` | Calls=100 (100%), Bypasses=0 (0%), 1,000 pair computations |
| **CLAIM-06** | BGE reranker performance improvement over hybrid RRF | **VERIFIED_WITH_LIMITATION** | `v11/e02_statistical_analysis.json` | DEV NDCG@5 gain $+0.2697$ ($p=3.61e-7$); TEST Hit@5 = 0.0000 |
| **CLAIM-07** | Pure BGE Cross-Encoder inference latency | **VERIFIED** | `v11/final_latency_analysis.json` | Pure BGE model inference p50 = 531.41 ms, p95 = 4,246.05 ms |
| **CLAIM-08** | Multi-stage verified RAG synthesis & citation repair | `NOT_TESTED` | None | Awaiting Module 2 implementation & evaluation |
