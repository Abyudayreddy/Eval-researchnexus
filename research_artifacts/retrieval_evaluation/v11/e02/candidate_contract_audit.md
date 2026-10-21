# Candidate Contract Audit & Candidate Schema Specification

## 1. Executive Overview

This document records the empirical candidate contract audit conducted as part of **Module 1.8** of the ResearchNexus evaluation pipeline.

Prior to Module 1.8, evaluation runs bypassed the BGE Cross-Encoder reranking stage (`BAAI/bge-reranker-base`) because `retrieve_hybrid_rrf` returned lightweight candidate dictionaries containing rank/score metadata but lacking hydrated text chunks (`PaperChunk.text`).

Through this audit, we established the exact schema produced by `retrieve_hybrid_rrf`, verified the text hydration pathway in `rerank_and_build_evidence`, and resolved index key alignment between BM25 and SQLite `PaperChunk` records, enabling **100% genuine BGE execution** across all 100 benchmark items in `ds_nexus_v11`.

---

## 2. Model & Candidate Schema Specifications

### 2.1 Hybrid RRF Output Schema (`retrieve_hybrid_rrf`)
`LocalEvidenceRetriever.retrieve_hybrid_rrf` returns a tuple `(candidates, trace_hybrid)`, where `candidates` is a list of dictionaries formatted as follows:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "HybridRRFCandidate",
  "type": "object",
  "properties": {
    "chunk_id": {
      "type": "string",
      "description": "Unique identifier of the database PaperChunk (e.g., paper_res_001_chunk_000)"
    },
    "rrf_score": {
      "type": "number",
      "description": "Reciprocal Rank Fusion score computed with k=60"
    },
    "bm25_rank": {
      "type": ["integer", "null"],
      "description": "1-based rank from BM25 retrieval, or null if omitted from top-k BM25"
    },
    "dense_rank": {
      "type": ["integer", "null"],
      "description": "1-based rank from Dense Chroma retrieval, or null if omitted from top-k Dense"
    }
  },
  "required": ["chunk_id", "rrf_score"]
}
```

### 2.2 Text Hydration Requirement for Cross-Encoder Input
The BGE Cross-Encoder reranker (`BAAI/bge-reranker-base`) requires text pairs: `[query_text, candidate_text]`.

Because `retrieve_hybrid_rrf` returns only structural IDs and RRF scores, the downstream function `rerank_and_build_evidence` performs database query text hydration:

```python
db_chunks = db.query(PaperChunk).filter(PaperChunk.chunk_id.in_(candidate_c_ids)).all()
chunk_map = {c.chunk_id: c for c in db_chunks}
```

If `chunk_id` in `candidates` does not match the database `PaperChunk.chunk_id` (e.g. legacy BM25 mapping mismatch), `chunk_map` fails to hydrate text, returning empty candidate lists and causing a BGE bypass.

---

## 3. Root Cause Analysis & Resolution

1. **Mismatch Identified**:
   - `bm25_mapping.json` previously contained legacy keys formatted as `local:Artificial_Intelligence:...`.
   - SQLite `paper_chunks` stored canonical IDs formatted as `paper_res_XXX_chunk_YYY`.
   - Hybrid RRF inherited BM25 keys, causing `db.query(PaperChunk)` lookups to fail during text hydration.

2. **Fix Implemented & Re-indexed**:
   - Rebuilt `bm25_index.pkl` and `bm25_mapping.json` directly from SQLite `paper_chunks` for `ds_nexus_v11`.
   - Verified that `retrieve_hybrid_rrf` outputs valid SQLite chunk IDs.
   - Verified that `rerank_and_build_evidence` correctly populates candidate texts and invokes `FlagReranker.compute_score`.

---

## 4. Audit Verification Outcome

- **BGE Call Rate**: **100/100 (100%)** queries in `ds_nexus_v11` successfully hydrated candidate texts and executed BGE reranking.
- **BGE Bypass Rate**: **0/100 (0%)** bypasses.
- **Contract Integrity Status**: **VERIFIED_VALID**.
