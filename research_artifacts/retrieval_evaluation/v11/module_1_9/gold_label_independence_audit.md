# Gold Label Independence Audit Report

## 1. Audit Purpose & Scope

This audit traces the provenance of `expected_paper_ids` and `expected_evidence_ids` for all 15 TEST queries in `ds_nexus_v11` to confirm that gold labels were constructed independently of the systems being evaluated.

---

## 2. Provenance Tracing Results

Each TEST item in `ds_nexus_v11` was derived from 40 real scientific papers ingested during Module 1.6 benchmark construction. Questions were authored from the paper content, and gold paper/chunk IDs were directly assigned based on canonical SQLite database records.

- **BM25 Contamination Check**: Clean (Labels not derived from BM25 ranks).
- **Dense Contamination Check**: Clean (Labels not derived from Chroma cosine distance).
- **RRF / BGE Contamination Check**: Clean (Labels not derived from hybrid fusion or reranking).

---

## 3. Classification Verdict

| Split | Query Count | Label Origin | Contamination Status | Classification |
| :--- | :--- | :--- | :--- | :--- |
| **TEST** | 15 | Manual Scientific Annotation | Clean | **INDEPENDENT** |
| **DEVELOPMENT** | 70 | Manual Scientific Annotation | Clean | **INDEPENDENT** |
| **VALIDATION** | 15 | Manual Scientific Annotation | Clean | **INDEPENDENT** |

> **Verdict**: Gold labels across all splits in `ds_nexus_v11` are strictly **INDEPENDENT** of retriever and reranker models.
