# Benchmark Retirement Report: Retirement of `ds_nexus_v10`

## 1. Executive Summary

Dataset `ds_nexus_v10` is hereby officially **RETIRED** and classified as **`INVALID_FOR_PUBLICATION_EVALUATION`**.

---

## 2. Technical Reasons for Retirement

1. **Retriever-Dependent Contamination**:
   - Gold paper and chunk IDs were populated by querying `LocalEvidenceRetriever.bm25_mapping` at seeding time.

2. **Synthetic Prompt Template Mismatch**:
   - Question text was generated via static string templates ("What is the primary contribution reported in paper X...") that bear zero lexical or embedding overlap with the actual scientific text of paper X.

3. **Short-Circuited BGE Evaluations**:
   - BGE Cross-Encoder reranking was never invoked during E02 because 0 top-K candidates were retrieved.

---

## 3. Historical Preservation Notice

`ds_nexus_v10` is retained strictly for historical audit trail purposes and MUST NOT be used for any future paper metrics or comparative baselines.
