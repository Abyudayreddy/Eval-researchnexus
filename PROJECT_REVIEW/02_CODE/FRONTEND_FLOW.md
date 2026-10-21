# ResearchNexusAI — Frontend Execution Flow

> **Scope:** Client-side React TypeScript Application (src/)  
> **Entry:** src/main.tsx → src/App.tsx  

---

## 1. High-Level Flow Architecture

`	ext
User Browser
    │
    ▼
[ src/main.tsx ] ────────► Wraps ReactDOM Root
    │
    ▼
[ src/App.tsx ] ─────────► Evaluates Route & ProtectedRoute Guard
    │
    ├─────────────────────────────┬─────────────────────────────┐
    ▼                             ▼                             ▼
Public Views              Unauthenticated Access        Authenticated Views
( / , /login, /register )  ( Redirect to /login )        ( Mounts <AppLayout /> shell )
                                                                │
                 ┌──────────────────────────────┬───────────────┴──────────────┬──────────────────────────────┐
                 ▼                              ▼                              ▼                              ▼
     [ HybridSearchPage.tsx ]         [ AssistantPage.tsx ]       [ LiteratureReviewPage.tsx ]          [ XaiPage.tsx ]
         │                              │                              │                              │
         ▼                              ▼                              ▼                              ▼
  Query / Filters               Chat / Synthesis Prompts       Multi-Paper Comparison         Provenance & Claim Audit
         │                              │                              │                              │
         └──────────────────────────────┼──────────────────────────────┴──────────────────────────────┘
                                        ▼
                                [ src/utils/api.ts ] ──► (Typed Axios HTTP Client)
                                        │
                                        ▼
                               FastAPI Backend Server
`

---

## 2. Key Frontend Components & State Management

1. **Routing Guard (src/App.tsx):**
   - Intercepts protected URLs.
   - Triggers checkAuth() against backend /api/auth/me.
   - Prevents unauthenticated requests from firing against research APIs.

2. **Global State (src/store/*.ts via Zustand):**
   - uthStore.ts: Session tokens, user profile.
   - paperStore.ts: Active search query, returned candidate papers, selected corpus.
   - 
esearchStore.ts: Generated synthesis blocks, comparison matrices, literature reviews.
   - xaiStore.ts: Evidence provenance nodes, attention weights, token saliency scores.

3. **API Bridge (src/utils/api.ts & src/utils/apiAdapter.ts):**
   - Injects JWT Bearer tokens into request headers.
   - Normalizes snake_case backend responses to camelCase frontend TypeScript interfaces.
   - Manages unified network error toasts and timeout handling.
