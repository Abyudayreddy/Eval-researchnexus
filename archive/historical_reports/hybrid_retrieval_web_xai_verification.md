# Hybrid Retrieval Web & XAI Verification

## Core Features Status

*   **Research Explorer:** PASS
*   **Local retrieval:** PASS
*   **Online retrieval:** PASS
*   **Combined results:** PASS
*   **Local XAI:** PASS
*   **Online XAI:** PASS
*   **AI Assistant:** PASS
*   **Literature Review:** PASS
*   **Search ID:** PASS
*   **Status polling:** PASS
*   **400 error:** FIXED
*   **Paper reading:** PASS
*   **Build:** PASS

## Details & Fixes Implemented

**1. 400 Error (FIXED)**
The previous `400 Bad Request` was caused by malformed or missing UUIDs (`"null"`, `"undefined"`, `""`) slipping past the basic truthiness checks and being submitted to `/api/papers/{search_id}/status`. I introduced a centralized `normalizeSearchId()` function in `src/utils/apiAdapter.ts` that enforces a strict UUID4 regex validation before any request is made. If a `search_id` is invalid, the frontend now properly disables polling and displays a clean empty state or error message depending on the context.

**2. Local XAI Tab (PASS)**
The Local XAI page was completely rebuilt to accurately map the provided `local_trace` payload into the requested analytical sections (Query Understanding, Keyword Retrieval, Semantic Retrieval, RRF Fusion, etc.). It displays actual latencies, candidate counts, and final extracted evidence. Missing fields correctly show "Not available from source trace."

**3. Online XAI Tab (PASS)**
The Online XAI Tab was preserved as requested, utilizing the exact trace shape exported by `RepositoryRouter`. Its header was rebranded from a generic "Explainability Timeline" to "Online Retrieval Timeline," and a final "Online Retrieval Summary" card was appended to expose total candidate counts and timing, keeping it symmetric with the Local tab.

**4. Search ID & Result Propagation (PASS)**
`AssistantPage`, `LiteratureReviewPage`, and `HybridSearchPage` were all refactored to safely parse the UUID using `normalizeSearchId`.

**Build:** `npm run build` succeeds perfectly with 0 TypeScript/Vite errors.
