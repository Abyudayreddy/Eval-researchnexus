# ResearchNexusAI — Key Metrics to Memorize for Review & Defense

> **Status:** ✅ Reconciled to Authoritative V4 Canonical Evidence  
> **Source Directory:** `evaluation/Re-evaluation of mistakes/`  

---

| Concept | Canonical Value | Exact Context / Definition | Authoritative Source |
|---|---|---|---|
| **Corpus Size** | **687 papers** | Peer-reviewed PDFs across AI, Environmental, Interdisciplinary | `ResearchMind_LocalKB/manifests/` |
| **Benchmark Size** | **100 items (N=15 TEST)** | DEV=70, VAL=15, TEST=15 (`ds_nexus_v11`) | `canonical_benchmark_manifest.json` |
| **TEST Split Structure** | **10 Ans, 5 Unans** | 5 synthesis, 5 adversarial, 5 unanswerable | `canonical_benchmark_manifest.json` |
| **Hit@20 (All 15 TEST)** | **66.7% (10/15)** | BM25, Hybrid RRF, and BGE Rerank hit 10/15 queries | `canonical_retrieval_metrics.csv` |
| **Recall@20 (10 Answerable)**| **100.0% (10/10)** | All 10 answerable test queries find gold paper in Top-20 | `canonical_retrieval_metrics.csv` |
| **BM25 MRR (All 15)** | **0.0759** | Lexical baseline MRR (0.1139 on answerable 10) | `canonical_retrieval_metrics.csv` |
| **Hybrid RRF MRR (All 15)** | **0.0431** | Hybrid RRF baseline MRR (0.0647 on answerable 10) | `canonical_retrieval_metrics.csv` |
| **BGE Rerank MRR (All 15)** | **0.0480** | Reranker gives modest promotion (0.0720 on answerable) | `canonical_retrieval_metrics.csv` |
| **RRF Constant** | **k = 60** | Reciprocal Rank Fusion smoothing parameter | `retrieval.py` |
| **Automated NLI Precision** | **100.0% (7/7)** | 4/4 Naive RAG, 3/3 Verified RAG factual assertions | `canonical_grounding_metrics.json` |
| **Factual Assertion Sample** | **N = 7 claims** | Small factual sample size across test split | `canonical_grounding_metrics.json` |
| **Abstention Accuracy** | **100.0% (5/5)** | Model correctly refused all 5 unanswerable queries | `canonical_grounding_metrics.json` |
| **Human Evaluation Status** | **NOT MEASURED** | 0 human annotators (designated as future work) | `canonical_grounding_metrics.json` |
| **Applied Repairs** | **0** | 4 candidate repairs rejected due to ambiguity | `canonical_claim_accounting.csv` |
| **Citation Coverage** | **20.0% (1/5)** | 1 out of 5 eligible factual claims grounded across C0, C1, C2 | `canonical_claim_accounting.csv` |
| **Refinement Grounding Gain**| **0.0% (p = 1.000)** | Iterative refinement gives 0 net gain with +106% latency | `v4_reconciliation_report.md` |
| **BM25 Latency p50** | **0.69 ms** | Component-level CPU lexical lookup | `canonical_latency_results.csv` |
| **Hybrid RRF Latency p50** | **6.56 ms** | Component-level candidate set combination & RRF | `canonical_latency_results.csv` |
| **BGE Cross-Encoder p50** | **531.41 ms** | Neural cross-attention reranking inference | `canonical_latency_results.csv` |
| **Total Request Mean Latency**| **12.12 s** | Complete end-to-end request (dominated by LLM call) | `canonical_latency_results.csv` |
