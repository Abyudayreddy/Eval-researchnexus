# Hybrid Retrieval Integration Verification

## Test Results

*   **Test 1 (INITIAL PAGE): PASS**
    *   No API search request triggered on mount or initial navigation.
*   **Test 2 (SUBMIT SEARCH): PASS**
    *   Clicking Search successfully executes a single `POST /api/papers/search` call. `search_id` is captured and bound to React state and URL query params.
*   **Test 3 (PROGRESS): FAIL (Backend Issue)**
    *   **Reason:** The backend endpoint `POST /api/papers/search` executes synchronously. It calls `await asyncio.gather(local_task, online_task)` and blocks the HTTP request for ~10 seconds. The frontend does not receive the `search_id` until the entire retrieval is finished. Consequently, the polling loop cannot start during execution, preventing the real-time progress panels from rendering.
*   **Test 4 (RESULTS): PASS**
    *   Both Local and Online results render correctly in the single list. Provenance badges (LOCAL, ONLINE, MIXED) display precisely according to `retrieval_source`.
*   **Test 5 (XAI): PASS**
    *   XAI page loads the `search_id` and correctly presents the `[ LOCAL RETRIEVAL ]` and `[ ONLINE RETRIEVAL ]` toggle UI. Traces are parsed from the status API accurately.
*   **Test 6 (AI ASSISTANT): PASS**
    *   The Assistant receives the `search_id` parameter and successfully requests both local and online evidence. Citation badges update properly.
*   **Test 7 (LOCAL PAPER): PASS**
    *   Local papers render complete metadata (without "Unknown Date" fallbacks when data exists). Clicking "Open PDF" targets the `/api/papers/{paper_id}/pdf` endpoint.
*   **Test 8 (ONLINE PAPER): PASS**
    *   Online papers preserve their original external `paper_url` linking behavior.
*   **Test 9 (SECOND SEARCH): PASS**
    *   Submitting a new search correctly clears previous polling hooks, resets result state, and acquires a fresh `search_id`.
*   **Test 10 (FAILURE): PASS**
    *   A simulated branch failure properly renders the styled status banner (e.g., `Local retrieval failed — Online results available`) while preserving the successful branch's results.

## Final Summary Details

*   **Search API response shape:** Returns `{"search_id": "...", "papers": [...], "local_result_count": X, "online_result_count": Y, "combined_result_count": Z, ...}` (Includes the actual results arrays).
*   **Status API response shape:** Returns `{"search_id": "...", "overall_status": "complete", "local": {...}, "online": {...}, "metrics": {"combined_metrics": {"merged_count": X}}, "trace": {...}}` (Noticeably omits local/online metric counts and omits the papers array entirely).
*   **Actual local count:** Derived from `response.local_result_count` (Test API returned 14 results).
*   **Actual online count:** Derived from `response.online_result_count`.
*   **Actual combined count:** Derived from `response.combined_result_count`.
*   **XAI Local status:** Renders the dynamic vertical timeline using node stages extracted from `status.trace.local_trace.stages`.
*   **XAI Online status:** Reuses the existing online horizontal timeline using `status.trace.online_trace`.
*   **AI Assistant status:** Supports mixed provenance citations, rendering LOCAL/ONLINE badging properly for grounded context.
*   **Remaining failures:** **1** (Test 3). Requires backend modification to return `search_id` immediately and process retrieval in a background task (or alternatively implement SSE stream support).
