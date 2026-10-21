# ResearchNexusAI — Paper Evidence Mapping

> **Target Manuscript:** `ieee_paper/ResearchNexus_AI_Paper.tex`  
> **Source Evidence:** `evaluation/Re-evaluation of mistakes/`  

---

## 1. Section-to-Evidence Mapping

| Manuscript Section | Content / Claim | Authoritative Evidence File | Reconciled Status |
|---|---|---|---|
| **Abstract & Intro** | Hybrid RRF Hit@20 retrieval capability | `canonical_retrieval_metrics.csv` | **86.7% (78/90)** verified |
| **Section IV (Retrieval)** | Table I: BM25 vs Dense vs Hybrid vs Rerank | `canonical_retrieval_metrics.csv` | Exactly matches V4 table |
| **Section IV (Retrieval)** | Claim of BGE reranking statistical gain | `superseded_claims_register.csv` | **Withdrawn:** Reranker matches Hybrid Hit@20 |
| **Section V (Grounding)** | Grounding Precision & Recall | `canonical_grounding_metrics.json` | **88.4% Precision, 81.2% Recall** |
| **Section V (Citation)** | Citation coverage & repair demonstration | `canonical_claim_accounting.csv` | **20.0% coverage (1/5 claims); Not Demonstrated** |
| **Section VI (XAI)** | Provenance DAG & latency trade-offs | `canonical_latency_results.csv` | Retrieval ~82ms, Rerank ~313ms |
