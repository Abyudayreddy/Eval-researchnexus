# V4 Canonical Evidence Reconciliation Report
**Package**: `evaluation/publication_audit_v2/v4_reconciliation/`  
**Dataset**: `ds_nexus_v11` ($N=100$: DEV=70, VAL=15, TEST=15)  
**Status**: CANONICAL SOURCE-OF-TRUTH ESTABLISHED

---

## 1. Executive Summary

This report establishes the final, authoritative canonical evidence package for the future six-page IEEE manuscript. It supersedes all contradictory, incomplete, or hard-coded claims from previous audit passes without deleting historical records.

### Key Resolutions:
1. **Canonical Test Split Manifest**:
   - The authoritative benchmark `benchmark_items.json` defines TEST items `item_v11_086` through `item_v11_090` as **SYNTHESIS (Answerable, 1 gold paper each)**, items `091` through `095` as **ADVERSARIAL (Answerable, 1 gold paper each)**, and items `096` through `100` as **UNANSWERABLE (0 gold papers, 0 gold chunks)**.
   - Stale manifests in earlier audits incorrectly assigned items 86-90 as unanswerable. This has been corrected in [`canonical_benchmark_manifest.json`](canonical_benchmark_manifest.json).
2. **Retrieval Metrics Reconciled**:
   - **BM25 Lexical**: In raw per-query records (`e01_raw_per_query.json`), all 10 answerable test items hit gold papers at ranks 8-9. Therefore:
     - Hit@5 = **0.0000 (0/15)**.
     - Hit@10 = **0.6667 (10/15)**.
     - Hit@20 = **0.6667 (10/15)**.
     - Recall@20 (Answerable queries) = **1.0000 (10/10)**.
     - MRR across all 15 queries = **0.0759**; MRR across 10 answerable queries = **0.1139**.
   - **Dense Chroma**: Stale claim of 0.6000 was synthetic; raw e01 test baseline achieved 0.0000 in top-20 on TEST split.
   - **Hybrid RRF ($k=60$)**: Canonical Module 01 live candidate pool achieved **10/15 (0.6667) Hit@20**, and **10/10 (1.0000) Recall@20 on answerable queries**. Stale 11/15 claim is permanently withdrawn. Canonical MRR is **0.0431** (all 15) / **0.0647** (10 answerable).
   - **BGE Reranker**: Synthetic values (MRR 0.5444 and +47.7% gain) are withdrawn. Canonical Module 01 records show BGE Reranker MRR is **0.0480** (all 15) / **0.0720** (10 answerable) with Hit@20 = **0.6667**.
3. **Claim Taxonomy & Grounding Accounting**:
   - Across the 56 extracted sentences (`reclassified_claims.json`):
     - **Appropriate Abstentions**: 30 sentences.
     - **Insufficient Evidence Findings**: 19 sentences.
     - **Factual Assertions**: 7 sentences total (4 in Naive RAG, 3 in Verified RAG).
     - **Supported Factual Claims**: 4/4 in Naive RAG (100%), 3/3 in Verified RAG (100%) under automated NLI.
     - **Unanswerable Abstention Accuracy**: 5/5 (100.0%) for both systems.
   - **Human Ground Truth**: Formally confirmed as **`HUMAN_VALIDATION_BLOCKED / NOT_MEASURED`**.
4. **Model Configuration Provenance**:
   - Historical comparison E04 was executed on `gemini-2.5-flash` ($T=0.0$).
   - Authoritative comparison E04.1 was executed on `gemini-3.5-flash-lite` ($T=0.0$).
   - Current backend codebase targets `gemini-2.5-flash` ($T=0.0$).
   - Model evolution across experiments is documented as an internal-validity threat.
5. **Latency Accounting**:
   - Disaggregated component latencies: BM25 p50 = **0.69 ms**, Dense p50 = **13.51 ms**, Hybrid RRF p50 = **6.56 ms**, Pure BGE Reranker inference p50 = **531.41 ms**, Combined Hybrid+BGE stage p50 = **535.06 ms**.
   - Complete request end-to-end pipeline mean latency is **12.12 seconds** (E10 ablation). Component percentiles are non-additive.
