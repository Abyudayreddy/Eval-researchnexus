# Phase 1.9 Research Explorer Product Integrity Report

## 1. Paper Reader
Implemented an in-app paper reading experience (`/read`) via `PaperReaderPage` to display PDFs directly without forcing a local download.

## 2. Local Read Behavior
`PaperCard` routes LOCAL source papers to the `/read?paper_id=...&search_id=...` reader rather than opening the PDF direct URL in a new tab. The backend canonical endpoint `GET /api/papers/{paper_id}/pdf` serves the file.

## 3. Online Read Behavior
ONLINE source papers correctly bypass the in-app reader and open their configured external sources/URLs using existing behavior. MIXED papers prefer the local PDF viewer when one is available, otherwise they gracefully fall back to the external URL.

## 4. Sorting
Implemented purely client-side sorting applied to `displayedResults`.
- **Most Relevant**: Falls back to the original backend sort array.
- **Newest**: Orders by `publication_date`/`year` DESC. Null dates are assigned epoch `0` to naturally drop to the end.
- **Oldest**: Orders by `publication_date`/`year` ASC. Null dates are assigned `Infinity` to forcefully drop to the end.
- Both sorts maintain the stable secondary ordering of the original relevancy array.

## 5. Filters
Implemented missing filters in the UI (Publication Year, Source, Evidence). All filtering logic is strictly client-side via `useMemo` on the `results` array, completely avoiding `POST /search` reruns.

## 6. History Creation
Ensured that the backend API generates exactly one `SearchHistory` record per `search_id`. Repeated searches for the same query naturally yield separate history sessions due to generating a new `search_id`.

## 7. History Deduplication
The React frontend logic correctly avoids accidentally dispatching multiple `POST /search` triggers on a single submission, preventing spurious duplicate search generation. 

## 8. History Persistence
Backend `_update_experiment` was enhanced to explicitly synchronize final `local_result_count`, `online_result_count`, and `result_count` directly into the Postgres `search_history` table upon completion.

## 9. History Counts
Recent Research UI now displays authentic counts rather than the stale "0 Local / 0 Online" default state by utilizing the newly synced data.

## 10. History Restore
Clicking a history item sets the `urlSearchId` and leverages `startPolling` to fetch the status/results from the server via a `GET` request. No new `POST /search` is instantiated.

## 11. search_id Continuity
The `search_id` perfectly survives page reloads through URL parameters, and propagates transparently to downstream workflows (Ask AI, Explain, Literature Builder, Reader).

## 12. Research Context
The history loader explicitly restores context and links all subsequent contextual actions to the active `search_id`.

## 13. Explorer Actions
All downstream Explorer actions pass the requisite context (`search_id`, `paper_id`) smoothly via route parameters.

## 14. Network-Call Validation
Browser tracing confirms that changing sorting or applying filters operates instantly in the UI with zero outbound network calls, fulfilling the offline-first design pattern for explorer state.

## 15. Browser Verification
Browser UI confirms complete functionality of `PaperReaderPage`, filtering permutations, sorting logic, and history persistence.
