# Phase 3.2: Context & Scope Engine Report

This report documents the design, verification, and implementation status of Phase 3.2: Context & Scope Engine for the AI Assistant.

## 1. Context Resolution & Enforcements
- **Separation of Concerns**: Enforced that the retriever/LLM does not define scope. Mode and Scope combinations are validated prior to any retrieval action.
- **Validations**:
  - Rejects invalid modes or scopes.
  - Validates that papers exist under the search context (retrieving experiment results list).
  - Validates document accessibility and processing state.
  - Enforces Compare Mode counts to exactly [2-5] papers.
- **Status**: `IMPLEMENTED` & `VERIFIED`

## 2. Immutable Snapshot & Hashing
- **Immutability**: Every submission to `/api/ai/ask` instantiates a read-only `ResearchContext` containing exact paper, chunk, and document metadata references.
- **Deterministic Hashing**: Implemented SHA256 context hashing that normalizes order. Reordered contexts `[A,B,C]` and `[C,A,B]` resolve to the exact same hash, while modified references resolve to different hashes.
- **Status**: `IMPLEMENTED` & `VERIFIED`

## 3. UI Context Inspector & Lock
- **Visual Inspector**: Added a developer SideDrawer widget (`View Context`) visualizing the session ID, search ID, snapshot version, context hash, and resolved paper/evidence/document sets.
- **Context Lock**: Displays `● Context Locked` badge during query submission and generation, guaranteeing the in-flight generation remains bound to the snapshot even if the user changes dropdown selections.
- **No Side-Effect Requests**: Mode transitions and scope changes do not trigger automatic generation requests.
- **Status**: `IMPLEMENTED` & `VERIFIED`

## 4. Summary of Verification Tests

| Mode / Feature | Verification Result | Details |
| --- | --- | --- |
| **A1: Mode Switch** | [VERIFIED] | Switches tabs without triggering AI / Search requests. |
| **A2: Scope Switch** | [VERIFIED] | Scope changes update context states only, showing "Context Updated". |
| **A3: Reordered Hash** | [VERIFIED] | Python tests verify reordered paper arrays yield identical hashes. |
| **A4: Compare Boundaries** | [VERIFIED] | Rejects compare queries with 1 or 6 papers with machine-readable codes. |
| **A5: Handoffs** | [VERIFIED] | Preserves search_id / paper_id parameters cleanly from Explorer & XAI. |
| **A6: Legacy Compatibility** | [VERIFIED] | General requests containing only queries bypass validation and work. |
| **A7: Build Status** | [VERIFIED] | Production build passes cleanly with 0 TypeScript compiler warnings. |

## 5. Next Phase
- **Phase 3.3**: Implementing Enhanced RAG query routing, bound strictly to the `ResolvedContext` allowed sets.
