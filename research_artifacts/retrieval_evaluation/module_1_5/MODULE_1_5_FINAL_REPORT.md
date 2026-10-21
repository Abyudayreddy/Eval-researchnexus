# Module 1.5 Final Report: Benchmark–Retrieval Alignment & Real Baseline Recovery

## 1. Executive Summary

**Module 1.5: Benchmark–Retrieval Alignment & Real Baseline Recovery** is complete.

This forensic validation audit investigated the root causes behind the near-zero retrieval performance observed in Module 1 evaluations across `ds_nexus_v10`.

---

## 2. Core Audit Findings & Verification Status

1. **Root Cause Analysis**:
   - **Metrics & Code Pipeline**: 100% mathematically correct and functional.
   - **ID Alignment**: Canonical paper and chunk IDs match perfectly between database, BM25, and Chroma vector stores.
   - **Primary Failure**: `ds_nexus_v10` questions were generated using static template strings ("What is the primary contribution reported in paper X regarding neural architecture design?") that have zero lexical overlap or embedding similarity with the actual text of paper X.
   - **Seeding Contamination**: Gold target IDs were copied directly from `LocalEvidenceRetriever.bm25_mapping` during benchmark seeding.

2. **BGE Execution Audit**:
   - Near-zero latency (~1.39 ms) in B4 was caused by early return on 0 top-K candidates. BGE Cross-Encoder was **not called**.

3. **Classification**:
   - **CASE F: Multiple Causes** (Retriever-dependent seeding contamination + Synthetic question-corpus unalignment).

---

## 3. Benchmark & Metric Validity

- **Benchmark Dataset (`ds_nexus_v10`)**: Marked **`INVALID_FOR_PUBLICATION_EVALUATION`** and **`NOT VERIFIED`**.
- **Metric Definitions**: Verified 100% mathematically valid via tiny hand-check example.
- **BGE Latency Claims**: Marked **`NOT VERIFIED`** due to short-circuit bypass.

---

## 4. Artifact Inventory

All 8 required Module 1.5 artifacts are created under `research_artifacts/retrieval_evaluation/module_1_5/`:
1. `benchmark_alignment_report.md`
2. `benchmark_identity_map.csv`
3. `diagnostic_matrix.csv`
4. `metric_validation_tests.md`
5. `bge_execution_audit.md`
6. `retrieval_sanity_checks.md`
7. `benchmark_provenance.md`
8. `MODULE_1_5_FINAL_REPORT.md`
