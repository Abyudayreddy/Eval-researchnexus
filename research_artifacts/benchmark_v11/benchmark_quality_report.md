# Benchmark Quality & Pre-Retrieval Validation Report: `ds_nexus_v11`

## 1. Quality Audit Overview

`ds_nexus_v11` was subjected to a strict **Pre-Retrieval Quality Audit** without invoking BM25, Dense vectors, RRF, or BGE models.

---

## 2. Pre-Retrieval Validation Checklist

- [x] **Corpus Grounding**: All 95 answerable questions are directly derived from actual text content of indexed scientific papers.
- [x] **Independent Gold Selection**: Gold evidence passages were selected by inspecting paper text prior to any retrieval indexing call.
- [x] **Zero Retriever Dependency**: Seeding scripts contain 0 import dependencies on `LocalEvidenceRetriever`, `bm25_mapping`, or Chroma query methods (`retriever_independent = true`).
- [x] **Provenance Traceability**: 100% of items have full provenance recorded in `benchmark_provenance.csv`.
- [x] **Frozen Test Split**: The isolated 15-item TEST split has been hashed and locked in `test_manifest.json`.
- [x] **Unanswerable Rigor**: All 5 UNANSWERABLE items request non-existent quantum gravity constants that are unsupported by the corpus.
- [x] **Multi-Evidence Mapping**: Comparative and synthesis questions map to all required target papers and evidence chunks.

---

## 3. Publication Readiness Decision

- **Status**: **`PUBLICATION_READY`**
- **Dataset ID**: `ds_nexus_v11`
- **Version**: `v1.1`
