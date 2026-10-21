# Pre-Evaluation Integrity & Lock Verification Report (`ds_nexus_v11`)

## 1. Verification Summary

Prior to launching Module 1.7 baseline evaluation experiments (E01 & E02), a strict pre-evaluation verification audit was performed on `ds_nexus_v11`.

---

## 2. Integrity Verification Checklist

- [x] **Dataset Presence**: `ds_nexus_v11` exists in SQLite database with status `READY` and `is_frozen = TRUE`.
- [x] **Total Item Count**: 100 items ($N=100$) present in database.
- [x] **TEST Split Lock**: Exactly 15 TEST items allocated (`DEVELOPMENT`: 70, `VALIDATION`: 15, `TEST`: 15).
- [x] **TEST Manifest Hash Lock**: Computed SHA256 of TEST items (`5c7684d44d890a4b6c8860ec2be222b4aed9412ee31611f0e19feb0b2e1bde0f`) **matches `test_manifest.json` 100% identically**.
- [x] **Vector Store Readiness**: Chroma `papers` collection is populated with 80 text chunks across 40 scientific papers.
- [x] **BM25 & Model Assets**: BM25 index and model files (`BAAI/bge-base-en-v1.5`, `BAAI/bge-reranker-base`) verified ready.

---

## 3. Execution Clearance

All pre-evaluation integrity locks are **PASSED**. Evaluation Service is cleared to execute E01 and E02 experiments against `ds_nexus_v11`.
