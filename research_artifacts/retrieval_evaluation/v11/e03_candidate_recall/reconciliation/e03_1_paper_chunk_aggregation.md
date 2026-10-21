# Paper vs Chunk Aggregation Architecture

## 1. Overview

This document specifies the exact aggregation pipeline converting chunk-level retrieval output to paper-level evaluation metrics.

---

## 2. Pipeline Sequence

```
[Query Execution] ──> Raw Chunk Results List: [{chunk_id: paper_res_XXX_chunk_YYY, score: S}]
                            │
                            ▼
[Paper ID Extraction] ──> Extract paper_id = "paper_res_XXX"
                            │
                            ▼
[Deduplication] ────────> Deduplicate paper IDs preserving first occurrence rank
                            │
                            ▼
[Top-k Selection] ──────> Select top-k unique paper IDs
                            │
                            ▼
[Metric Evaluation] ────> Compute Recall@k and Hit@k against expected_paper_ids
```
