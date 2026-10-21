# Identifier Contract Audit Report

## 1. Audit Overview

This report documents the verification of identifier matching across the database, BM25 index, Dense Chroma vector store, and evaluation item labels for `ds_nexus_v11`.

---

## 2. Identifier Representation Audit

- **Canonical Database Format**: `paper_res_XXX` (Papers), `paper_res_XXX_chunk_YYY` (Chunks).
- **BM25 Index Representation**: `paper_res_XXX_chunk_YYY` (Matching canonical SQLite keys).
- **Dense Chroma Vector Metadata**: `paper_id: paper_res_XXX`, `chunk_id: paper_res_XXX_chunk_YYY`.
- **Evaluation Item Expected IDs**: `["paper_res_XXX"]` (Paper IDs), `["paper_res_XXX_chunk_YYY"]` (Chunk IDs).

---

## 3. Discrepancy Checks

1. **Prefix Mismatch**: None detected (`paper_res_` uniform across DB, BM25, and Chroma).
2. **Zero-Padding Mismatch**: None detected (3-digit zero-padded integers `001..040` used consistently).
3. **String/Int Conversion Errors**: None detected (IDs consistently loaded as standard strings).
4. **Stale Index State**: BM25 index and Chroma collection were fully rebuilt from SQLite `PaperChunk` records for `ds_nexus_v11`.

---

## 4. Final Contract Verdict

> **IDENTIFIER_CONTRACT_STATUS**: **VERIFIED_EXACT_MATCH**
> All components share 100% exact string identifier representations. No ID mismatch bug exists.
