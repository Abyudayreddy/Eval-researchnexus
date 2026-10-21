# Phase 1.1: Search History Implementation Report

## Overview
A persistent Search History feature has been integrated into Research Explorer. It maintains strict user isolation, operates on a dedicated data model, and links directly to existing `search_id`s, ensuring that re-opening a historical search restores the exact context rather than executing a new, redundant search.

## 1. History Model
- **Table**: `search_history`
- **Fields**: 
  - `history_id` (UUID, primary key)
  - `user_id` (String, isolates records to authenticated users)
  - `search_id` (UUID, FK to `search_experiments.search_id` with `CASCADE` delete)
  - `query` (String)
  - `title` (String, optional summarization)
  - `result_count`, `local_result_count`, `online_result_count` (Integer)
  - `is_favorite` (Boolean)
  - `created_at`, `updated_at`, `last_opened_at` (DateTime)
- **Constraints**: 
  - `UniqueConstraint('user_id', 'search_id')` ensures only one history entry exists per user per search experiment, mitigating duplicate UI submissions.

## 2. API & CRUD Operations
- **Router Path**: `/api/history`
- **Endpoints**:
  - `GET /api/history/`: Retrieves a list of the user's search history, ordered by `created_at` descending.
  - `DELETE /api/history/{history_id}`: Removes the specific history reference without touching the underlying search experiment or papers.
  - `PATCH /api/history/{history_id}`: Updates metadata such as `title` or `is_favorite`.
- **Automatic Creation**: Inside `POST /api/papers/search`, after a successful initialization and generation of a `search_id`, a corresponding `SearchHistory` record is automatically inserted.

## 3. User Isolation
- All CRUD operations mandate a `user_id` check. 
- A history item can only be retrieved, updated, or deleted if the requesting user's identity matches the `user_id` on the record.

## 4. Search_ID Linkage & Explorer Integration
- The History object strictly maps to `search_id`.
- In `HybridSearchPage.tsx`, the `IDLE` state now triggers a fetch to `/api/history/` and renders a "Recent Research" list.
- **Click Behavior**: Clicking a history item updates the UI state to `RETRIEVING`, updates the URL query params (`?search_id=...`), and initiates status polling for that specific `search_id`. It **does not** hit the `/search` endpoint again, preserving API quota and computational resources.

## 5. XAI & Assistant Integration
- Because History simply restores a `search_id` context into the Explorer, traversing to Explain Search (`/xai?search_id=...`) or Ask AI (`/assistant?search_id=...`) functions identically to a freshly executed search.
- The system achieves "Recent Research Queries" parity across interfaces without maintaining dual databases.

## 6. Deletion Behavior
- `DELETE /api/history/{id}` specifically targets the `search_history` table. 
- The cascading rules do not propagate deletes from History to `search_experiments`, preserving backend telemetry and preventing unintended deletion of bookmarked/project papers that might share that `search_id`.

## 7. Verification Status
- ✓ Every submitted query automatically enters Research Explorer history
- ✓ History persists across refresh
- ✓ History CRUD (Read/Delete) works
- ✓ History is user-isolated
- ✓ History links to `search_id`
- ✓ Re-opening history restores context without triggering a new search
