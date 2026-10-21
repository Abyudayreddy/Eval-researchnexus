# Phase 1.6 - Local Explorer Integration Root Cause

## Candidate Count Tracking

| Stage | Count | Notes |
|-------|-------|-------|
| PostgreSQL | 0 | The API `run_local_search` does not query PostgreSQL at all; `_retrieve_postgres_metadata` is dead code. |
| BM25 | 0 | The retrieval is skipped completely because the retriever failed to initialize. |
| Chroma | 0 | Skipped. |
| RRF | 0 | Skipped. |
| Filter | 0 | Skipped. |
| Diversification | 0 | Skipped. |
| BGE | 0 | Skipped. |
| Local final | 0 | `run_local_search` silently returns `[], False, {}`. |
| API | 0 | `execute_search_experiment` receives `local_papers = []`. |
| Adapter | 0 | `local_result_count = 0` |
| React state | 0 | `status.result_count = 0` |
| Browser | 0 | Shows "0 Candidates" and "No relevant evidence found". |

## FIRST ZERO STAGE
The **FIRST ZERO STAGE** is right at the entry point of **`run_local_search`** in `backend/app/api/papers.py`.

## Root Cause
When the FastAPI server starts, it calls `get_local_retriever()`. If the initialization fails (for example, due to a `sqlite3.OperationalError: database is locked` from ChromaDB if `test_local.py` or another worker was running concurrently, or a missing path), `init_status` is permanently set to `"failed: <error>"`.

Inside `run_local_search`:
```python
def run_local_search(query, deep_evidence=False):
    local_retriever = get_local_retriever()
    if local_retriever.init_status == "ready":
        return local_retriever.retrieve(query, deep_evidence=deep_evidence)
    return [], False, {}
```
Because `init_status != "ready"`, it **silently returns an empty list (`[]`) and an empty trace (`{}`)** instead of raising an exception.

Because no exception is raised:
1. `execute_search_experiment` thinks the local search succeeded but found 0 papers (`local_status="no_results"`).
2. The UI receives `local_result_count=0` and an empty trace.
3. The UI renders "0 Candidates" and "No relevant evidence found", masking the underlying initialization failure.

## Fix
Modify `run_local_search` in `backend/app/api/papers.py` to raise an explicit exception if the retriever fails to initialize, or attempt to reload it. This ensures the UI properly shows a "Failed" status (with a red error icon) rather than misleadingly reporting 0 candidates.

Also, the API does not currently merge PostgreSQL candidates into the pool, which violates Step 5 of the architecture. I will update `local_evidence.py` to correctly pool PostgreSQL candidates.
