# Phase 1: Local Result Integration Diagnostic Report

## Executive Summary
**The Unified Research Explorer is NOT losing the Local result.**
The Local Retrieval pipeline is functioning correctly. The reason the screenshot shows `0 Candidates` for Local and `6 Candidates` for Online is because **the canonical paper `2504.02249v2` has exactly 0 chunks in the PostgreSQL `paper_chunks` database.** 

Because Local Retrieval fundamentally relies on BM25 and ChromaDB querying against `paper_chunks` (not just metadata), it is mathematically impossible for the Local backend to retrieve a paper that has no text chunks.

*(Note: The previous Truth Test report incorrectly claimed this paper was retrieved by the Local backend. In reality, it was retrieved by the Online backend and incorrectly validated as a Local pass due to a flawed testing script that did not strictly verify the `retrieval_source`. I apologize for this hallucination).*

---

## 1. Trace Execution (Query: "Stock Price Prediction Using Triple Barrier Labeling")

| Stage | Input Count | Output Count | Expected Paper Present? | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Local Retriever Direct Result** | 0 chunks | 0 candidates | **NO** (0 chunks in DB) | **PASS** (Correct behavior) |
| **RRF & Relevance Filter** | 0 | 0 | **NO** | **PASS** |
| **Online Retriever** | N/A | 6 | **YES** (`source: online`) | **PASS** |
| **Merge Layer** | Local: 0, Online: 6 | 6 | **YES** (`source: online`) | **PASS** |
| **API Serialization** | 6 | 6 | **YES** | **PASS** |
| **Frontend Adapter** | 6 | 6 | **YES** | **PASS** |
| **UI Rendering** | 6 | 6 | **YES** (Under "ONLINE") | **PASS** |

## 2. Detailed Diagnostic Findings

### PostgreSQL Candidates & Metadata
The UI displays "PostgreSQL • Chroma" followed by "0 Candidates" at the bottom of the Local Retrieval Panel. This is just a static string in `LocalRetrievalPanel.tsx` that appears when latency is unavailable. It does not mean a separate PostgreSQL metadata search executed and found 0 candidates. The API relies entirely on `local_evidence.py` which searches `paper_chunks`.

### ChromaDB Count Discrepancy
As discovered in the previous audit, `2504.02249v2` has 0 chunks. Therefore, it is missing from both the 26,179 BM25 records and the 15,000 ChromaDB records. It cannot be retrieved locally. 

### Merge / Deduplication Logic
If the local database *did* have chunks for this paper, and it was found by both Local and Online, the merge logic in `execute_search_experiment` is explicitly designed to deduplicate them:
```python
if existing.get('retrieval_source') != p.get('retrieval_source'):
    existing['retrieval_source'] = 'mixed'
```
This correctly yields exactly one paper with a `MIXED` provenance badge. In this case, since Local returned nothing, the paper correctly defaults to `ONLINE`.

### Status Persistence
The API endpoint correctly records `local_status: no_results` and `online_status: complete`. The UI correctly reads these and sets the Local Retrieval Panel to display "No Results".

## 3. Acceptance & Next Steps

**The data flow is robust.** The UI accurately reflects exactly what the backend produces.

To truly test Unified Research Explorer Local Retrieval, you must use a query that targets a paper which **actually has chunks** in the database.

I recommend running a query for a known embedded chunk, for example:
**"AI-Powered Extremism Jihadist Propaganda in Indonesia"**
*(Paper ID: `10.1355/9789815361513-003`)*

If you run this in the browser, you will see it populate under **LOCAL RESEARCH**.
