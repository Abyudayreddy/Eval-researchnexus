# Research Questions Specification (Frozen)

## 1. Overview

This document freezes the official working Research Questions (RQs) for the ResearchNexus conference paper.

---

## 2. Frozen Research Questions Matrix

| RQ ID | Research Question Statement | Primary Evaluation Scope | Primary Experimental Mapping |
| :--- | :--- | :--- | :--- |
| **RQ1** | How do lexical, dense, and hybrid retrieval strategies differ in effectiveness for scientific literature retrieval? | Baseline IR metrics across splits | **E01** (BM25 vs. Dense vs. Hybrid RRF) |
| **RQ2** | Under a fixed hybrid candidate pool, what effect does BGE cross-encoder reranking have on ranking quality? | Ranking quality & precision | **E02** (Hybrid RRF vs. Hybrid + BGE Reranker) & **E03** (Multi-cutoff recall) |
| **RQ3** | Does evidence-bounded and verified RAG improve claim-level grounding compared with naive RAG under the same retrieved context? | Generation claim grounding | **E04** (Naive RAG vs. ResearchNexus Verified RAG) |
| **RQ4** | How accurately does the claim verification component detect supported, unsupported, and contradicted claims? | NLI verification accuracy | **E05** (Claim Verification Precision/Recall/F1) |
| **RQ5** | Does citation repair improve citation correctness and completeness for claims that require correction? | Citation repair quality | **E06** (Citation Repair Success Rate) |
| **RQ6** | Can ResearchNexus provide complete and correct provenance from final answer claims back to supporting evidence and retrieval stages? | XAI provenance tracing | **E08** (Trace Resolution & Completeness) |
| **RQ7** | What latency overhead is introduced by verification, citation repair, and iterative refinement? | End-to-end pipeline latency | **E07** (One-pass vs. Iterative) & **E09** (Latency Breakdown) |
