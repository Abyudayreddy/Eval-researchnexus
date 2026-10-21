# Phase 1.7 - Local Runtime Failure Root Cause

## 1. Exact Exception
`KeyError: '_type'`
This exception originated from `chromadb.api.configuration.py` during `get_collection('researchnexus_local_v1_bgebase')`.

## 2. Runtime Environment
- **Python executable:** `C:\Users\Abyureddy\anaconda3\envs\researchnexus\python.exe`
- **Working directory:** The API operates from the standard root directory (`C:\Users\Abyureddy\OneDrive\Desktop\SDC2`) as verified via path resolution logging.
- **DATABASE_URL:** Same as standard PostgreSQL configuration.
- **ChromaDB version:** The API virtual environment had ChromaDB `0.5.4` installed. The database files were likely generated with a newer version (e.g., `1.5.x` or `0.5.5+`).

## 3. Chroma Diagnosis
ChromaDB failed to initialize the `PersistentClient` collection because it attempted to parse the SQLite configuration JSON using an older schema parser that did not understand the newer `_type` property used in the stored JSON blob. 

## 4. BM25 Diagnosis
BM25 initialized correctly, but was skipped during the search pipeline because the overall `local_retriever.init_status` failed at the Chroma step.

## 5. PostgreSQL Diagnosis
PostgreSQL database and models successfully load and process queries within the API runtime context.

## 6. Embedding Model Diagnosis
The embedding model (`BAAI/bge-base-en-v1.5`) initializes correctly when Chroma successfully loads.

## 7. Local Retriever Diagnosis
Failed at initialization. Masking the failure allowed the UI to interpret it as 0 results instead of a system crash.

## 8. Root Cause
The `researchnexus` conda environment used by the API server contained an outdated version of `chromadb` (`0.5.4`) that was incompatible with the underlying SQLite database schema created by the ingestion script. The `KeyError: '_type'` caused `get_local_retriever()` to fail.

## 9. Fix
1. Captured and printed the full traceback in `local_evidence.py` to identify the `KeyError: '_type'`.
2. Upgraded `chromadb` to `1.5.9` within the `researchnexus` conda environment (`pip install --upgrade chromadb`).
3. Touched `main.py` to force `uvicorn` to restart with the updated dependencies.

## 10. API Verification
The API successfully passes requests to the `LocalEvidenceRetriever`, which now correctly loads the ChromaDB collection without throwing a schema validation error.

## 11. Local-only Browser Verification
Local-only execution completes successfully. The retrieval pipeline completes with valid `local_result_count > 0` and surfaces the local paper.

## 12. Mixed Browser Verification
The hybrid execution successfully populates results from both the Local and Online retrievers, merging them accurately and preventing duplicates while preserving provenance.

## 13. Final Component Health

| COMPONENT | STATUS |
|-----------|--------|
| PostgreSQL | PASS |
| BM25 | PASS |
| ChromaDB | PASS |
| Embedding Model | PASS |
| Local Retriever Init | PASS |
| RRF | PASS |
| Relevance Filter | PASS |
| BGE | PASS |
| Metadata Hydration | PASS |
