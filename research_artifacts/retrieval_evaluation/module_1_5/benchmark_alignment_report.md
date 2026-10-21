# Benchmark Alignment & Real Baseline Recovery Audit

## 1. Executive Summary

This forensic validation audit examined why Module 1 empirical retrieval evaluation produced near-zero retrieval metrics across `ds_nexus_v10`.

Through end-to-end tracing, index inspection, sanity checks, and metric validation, we determined that the evaluation infrastructure and metric formulas are **100% mathematically correct**, but the benchmark dataset `ds_nexus_v10` suffers from **synthetic question-corpus unalignment** and **retriever-dependent seeding contamination**.

---

## 2. Key Audit Findings

1. **Document & Chunk Identity**:
   - Canonical IDs (`local:Artificial_Intelligence:01f1d446...`) in the benchmark match the database and Chroma/BM25 indexes. There is zero ID corruption or string mismatch.

2. **Benchmark Seeding & Provenance**:
   - `expected_paper_ids` were derived directly by inspecting `LocalEvidenceRetriever.bm25_mapping` in `seed_benchmark_v10.py`.
   - Flagged: **POTENTIAL EVALUATION CONTAMINATION**.

3. **Query-Corpus Alignment**:
   - Benchmark questions were created using static template prompts ("What is the primary contribution reported in paper X regarding neural architecture design?") that do not contain keywords or semantic embeddings matching the actual text of paper X.
   - Diagnostic Sanity Check: `gold-in-candidate = NO` across all tested items.

4. **Metric Implementation**:
   - Metric formulas (Hit@1, Hit@5, Recall@5, Precision@5, MRR, NDCG@5) were hand-verified against a minimal test case and found 100% mathematically sound.

5. **BGE Short-Circuiting**:
   - B4 latency of ~1.39 ms is due to early exit on empty candidate sets. BGE inference was never invoked.

---

## 3. Decision Classification

**Primary Classification**: **CASE F: Multiple Causes**
- Cause 1: Seeding contamination (gold IDs derived from candidate map).
- Cause 2: Synthetic question-corpus unalignment (template queries bear no semantic relevance to target document text).
