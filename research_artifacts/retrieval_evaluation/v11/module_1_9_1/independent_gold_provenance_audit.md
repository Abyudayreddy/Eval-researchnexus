# Independent Gold-Label Provenance Audit Report

## 1. Provenance Audit Purpose

This audit independently traces the benchmark creation process for `ds_nexus_v11` by examining the underlying SQLite database records and dataset manifests to verify whether gold labels (`expected_paper_ids` and `expected_evidence_ids`) were created independently of retrieval models.

---

## 2. Benchmark Code & Database Provenance Evidence

1. **Source Data**: `ds_nexus_v11` was created by ingesting **40 real scientific ArXiv PDFs** into SQLite `papers` and `paper_chunks` tables.
2. **Question Generation**: 100 questions (70 DEVELOPMENT, 15 VALIDATION, 15 TEST) were formulated across 8 research categories directly from document chunk content.
3. **Gold Evidence Assignment**: Expected paper IDs (`paper_res_001` through `paper_res_040`) and evidence chunk IDs (`paper_res_XXX_chunk_YYY`) were assigned strictly from document chunk positions before any BM25 index or Chroma dense vector collection was built.
4. **Contamination Check**: Zero retrieval output was used to generate questions or set gold labels. No candidate pools or RRF rankings influenced the dataset ground truth.

---

## 3. Provenance Classification Verdict

```
GOLD_LABEL_PROVENANCE = INDEPENDENT
```

> The ground truth labels for `ds_nexus_v11` are 100% independent of all baseline retrievers (BM25, Dense Chroma, Hybrid RRF) and Cross-Encoder rerankers (BGE).
