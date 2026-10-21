# Final Implementation Lock Report

## 1. Project Overview

**Project Name:** ResearchNexus AI
**Project Type:** Explainable AI Research Paper Assistant / Research Operating System

**Core Concepts:**
- **Hybrid Domain-Based Knowledge Strategy:** Combines a pre-built local knowledge base (for immediate, high-quality responses) with dynamic retrieval from external repositories when local data is insufficient.
- **Hybrid Retrieval:** Uses a combination of BM25 (keyword matching) and semantic vector search (ChromaDB) to retrieve the most relevant chunks.
- **Dynamic Data Ingestion:** Automatically searches academic repositories, downloads, processes, and embeds new papers if the local knowledge base cannot answer a query adequately.
- **Enhanced Retrieval-Augmented Generation (RAG):** Uses Gemini 2.5 Flash to generate accurate, context-aware answers grounded entirely in the retrieved literature.
- **Explainable AI:** Provides full transparency into how an answer was generated, showing retrieved papers, relevant chunks, and citation mappings.
- **Research Workspace:** An integrated environment (OS) featuring notebooks, projects, literature review builders, and analytics to manage the entire research lifecycle.

These concepts work together to create a seamless workflow: A user asks a complex question, the system retrieves relevant data locally (or dynamically if needed), ranks the best information, uses LLMs to synthesize an answer, transparently explains the synthesis, and saves the context into a unified workspace.

---

## 2. Current Website Audit

Based on a thorough review of the existing React/Vite codebase.

**Current Functionality:**
The current website is a high-fidelity frontend prototype. The routing, layouts, and UI components are fully built. However, all data is static or managed via local state (Zustand). There is no active backend, no real database, and no live AI integration. 

**Current UI:**
The UI features a premium, white academic theme with glassmorphism touches. It utilizes `lucide-react` for iconography, Tailwind CSS for styling, and Radix UI primitives. Important layouts include responsive sidebars, grid-based dashboard cards, animated tab panels, filtering sidebars, and interactive research session cards. 

**Current Data:**
The module strictly uses:
- **Static mock data** (e.g., `src/mock/data.ts`, hardcoded arrays in pages).
- **Local state / Zustand** (`src/store/researchSessionStore.ts`) for managing UI interactions and session history.
- **localStorage** (via Zustand persist) for preserving mock sessions across reloads.
- **No API, Backend, or Database** is currently implemented.

### Module Audit

| Module Name | Current Status |
| :--- | :--- |
| **Dashboard** | UI only (Mock functionality) |
| **Research Domains** | UI only (Mock functionality) |
| **Research Explorer (Hybrid Search)** | UI only (Mock functionality) |
| **AI Research Assistant** | UI only (Mock functionality) |
| **Research Workspace (Projects)** | UI only (Mock functionality) |
| **Explainable AI (XAI)** | UI only (Mock functionality) |
| **Literature Review Builder** | UI only (Mock functionality) |
| **Notebook** | UI only (Mock functionality) |
| **Paper Library** | UI only (Mock functionality) |
| **Analytics** | UI only (Mock functionality) |
| **Notifications** | UI only (Mock functionality) |
| **Global Search** | UI only (Mock functionality) |

---

## 3. Final Module List

| Module | Purpose & User Action | Data / Backend / AI Requirements | Status |
| :--- | :--- | :--- | :--- |
| **Dashboard** | Overview of activity, domains, and quick actions. | **Backend:** Aggregated stats. **DB:** User profile, recent activity. | UI/Mock |
| **Research Domains** | Browse papers by 8 specific domains. | **Backend:** Domain filtering API. **DB:** PostgreSQL/ChromaDB. | UI/Mock |
| **Research Explorer** | Search and discover literature via Hybrid Search. | **AI/Backend:** BM25 + ChromaDB retrieval, RRF ranking. | UI/Mock |
| **AI Research Assistant** | Chat interface to ask complex research queries. | **AI:** Gemini 2.5 Flash + RAG pipeline. | UI/Mock |
| **Research Workspace** | Manage ongoing research projects. | **DB:** PostgreSQL (projects, links to papers). | UI/Mock |
| **Explainable AI** | View transparency metrics on RAG responses. | **Backend:** Expose retrieval metadata, rankings, and chunk mapping. | UI/Mock |
| **Literature Review** | Synthesize multiple papers into a structured review. | **AI:** Gemini 2.5 synthesis. **DB:** PostgreSQL (save reviews). | UI/Mock |
| **Notebook** | Markdown-based notes linked to papers. | **DB:** PostgreSQL (notes, highlights). | UI/Mock |
| **Projects** | Group papers, notes, and chats. | **DB:** PostgreSQL (relational mapping). | UI/Mock |
| **Paper Library** | View saved/bookmarked papers. | **DB:** PostgreSQL (bookmarks, user library). | UI/Mock |
| **Analytics** | View research statistics. | **Backend:** Usage aggregation. | UI/Mock |
| **Notifications** | Alerts for ingestion or system updates. | **Backend:** Notification API/WebSockets. | UI/Mock |
| **Global Search** | Universal search across the workspace. | **Backend:** Multi-table search. | UI/Mock |

---

## 4. Final User Roles

**Primary Users:**
- **Undergraduate Students:** Finding core literature for assignments and basic understanding of domains.
- **Postgraduate Students:** Conducting deep literature reviews and structuring thesis research.
- **Research Scholars:** Managing massive libraries, synthesizing state-of-the-art findings, and tracking domain trends.

**Secondary Users:**
- **Faculty Members:** Verifying literature, guiding students, and keeping up with interdisciplinary trends.
- **Scientists:** Extracting specific methodologies and data points from dense papers.
- **Industry Researchers:** Quickly pivoting into new domains and generating comprehensive reports for R&D.

---

## 5. Final System Input Specification

**Primary Input:**
Natural-language research query.
*Example:* "Compare Retrieval-Augmented Generation models in Healthcare."

**Optional Inputs:**
- Research domain
- Keywords
- Paper title
- Author name
- DOI
- Publication year
- Document type
- Search filters
- Preferred source

**Flow:** Inputs are captured via the React frontend, bundled into a JSON payload, and sent via REST/HTTP POST to the FastAPI backend to trigger the retrieval and generation pipeline.

---

## 6. Final Dataset Specification

**Local Pre-built Knowledge Base (Total: 670 papers):**
- Artificial Intelligence: 300
- Environmental Science: 190
- Interdisciplinary Research: 180

*Note: These papers are already collected, processed, chunked, and embedded. They do NOT require fresh ingestion during queries.*

**Dynamic Domains (Dynamic Retrieval):**
- Healthcare → PubMed Central
- Agriculture → AGRIS
- Data Science → arXiv + OpenAlex
- Space Science → NASA ADS
- Energy → OpenAlex

**Role Definition:** The local KB acts as the immediate, primary source of truth. Dynamic ingestion is only triggered as a fallback when local retrieval yields insufficient relevance scores.

---

## 7. Final Document Intelligence Pipeline

This pipeline applies to both the pre-built dataset and dynamically ingested papers.

1. **Research Paper (PDF/XML)**
   ↓
2. **PyMuPDF:** Text and layout extraction
   ↓
3. **Text Extraction & Cleaning:** Normalize formatting, remove headers/footers
   ↓
4. **Section Detection:** Identify Abstract, Intro, Methodology, etc.
   ↓
5. **LlamaIndex:** Framework orchestration
   ↓
6. **Semantic Chunking:** Break text into coherent chunks with overlap
   ↓
7. **Chunk ID / Chunk Metadata:** Assign metadata (Paper ID, Section, Page)
   ↓
8. **BAAI/bge-base-en-v1.5:** Generate dense embeddings
   ↓
9. **PostgreSQL + ChromaDB:** Store relational metadata (SQL) and vector embeddings (Chroma)

---

## 8. Final Online Query Workflow

User Query
↓
Query Processing
↓
Local Knowledge Base Search
↓
**Check Whether Relevant Results Are Sufficient**
- *If sufficient:* Continue directly to retrieval ranking.
- *If insufficient:*
  ↓
  Dynamic Data Ingestion
  ↓
  Search appropriate academic repositories
  ↓
  Download relevant papers
  ↓
  Process using PyMuPDF → Clean + section detection → Semantic chunking (LlamaIndex) → Generate embeddings (BAAI/bge-base-en-v1.5) → Update PostgreSQL + ChromaDB
  ↓
  Return to retrieval
↓
**Hybrid Retrieval**
↓
BM25 Keyword Retrieval & ChromaDB Semantic Vector Search
↓
Reciprocal Rank Fusion (RRF)
↓
BAAI/bge-reranker-base Cross-Encoder Re-ranking
↓
Top Papers & Relevant Chunks
↓
Context Construction
↓
Gemini 2.5 Flash
↓
Enhanced RAG Response
↓
Explainable AI (Map response to citations)
↓
Response to User
↓
Research Workspace

---

## 9. Explainable AI Specification

The XAI module will expose the inner workings of the RAG pipeline.

**Must Include:**
- Retrieved papers
- Relevant chunks used in context
- Retrieval information (BM25 vs Semantic scores)
- Supporting evidence (direct quotes)
- Citation mapping (inline links to chunks)
- Confidence information (Reranker scores)
- Explanation of how the answer was generated (Retrieved → Ranked → Selected → Generated)

*Note:* Do not claim to expose hidden LLM chain-of-thought reasoning; only expose the retrieval and grounding mechanics.

---

## 10. Final Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React.js (Vite) | Web interface |
| **UI** | Tailwind CSS | Interface styling |
| **Backend** | FastAPI | APIs and application logic |
| **Data Ingestion** | FastAPI + HTTP Requests | Academic repository retrieval |
| **PDF Processing** | PyMuPDF | PDF text/metadata extraction |
| **Document Intelligence** | LlamaIndex | Document processing and semantic chunking |
| **Embeddings** | BAAI/bge-base-en-v1.5 | Chunk/query embeddings |
| **Metadata Database** | PostgreSQL | Structured metadata and application data |
| **Vector Database** | ChromaDB | Embeddings and semantic retrieval |
| **Keyword Retrieval** | BM25 | Keyword-based retrieval |
| **Rank Fusion** | RRF | Combining retrieval rankings |
| **Re-ranking** | BAAI/bge-reranker-base | Re-ranking retrieved chunks |
| **LLM** | Gemini 2.5 Flash | RAG response generation |
| **Version Control** | Git + GitHub | Source control |
| **IDE** | VS Code | Development |

**Deployment:** Frontend → Vercel, Backend → Render

---

## 11. Database Specification

### PostgreSQL (Relational Data)
**Required for Implementation:**
- `Users` (id, credentials, preferences)
- `Papers` (id, title, abstract, authors, publish_date, url, domain_id)
- `Domains` / `Sub-domains` (id, name)
- `Projects` (id, user_id, name, description, created_at)
- `Notes` (id, user_id, project_id, paper_id, content)
- `Bookmarks` (id, user_id, paper_id)
- `Conversations` (id, user_id, session_id, message_log)

**Optional (Phase 2):**
- `Literature_Reviews`, `Collections`, `Notifications`, `Reading_status`

### ChromaDB (Vector Data)
- **Collection Structure:** Segmented by domains or one large indexed collection.
- **Schema:**
  - `id`: Chunk ID
  - `embedding`: BGE Vector
  - `document`: Chunk text
  - `metadata`: { `paper_id`, `section`, `domain`, `page_number` }

*Relationship:* PostgreSQL handles application logic and paper-level metadata; ChromaDB handles chunk-level semantic search. They map via `paper_id`.

---

## 12. Research Domain Structure

**1. Artificial Intelligence:** Machine Learning, Deep Learning, Retrieval-Augmented Generation
**2. Healthcare:** Medical AI, Disease Prediction, Clinical Research, Drug Discovery, Biotechnology
**3. Agriculture:** Precision Agriculture, Crop Prediction, Smart Farming, Soil Analysis, Agricultural IoT
**4. Data Science:** Data Analytics, Statistics, Big Data, Predictive Analytics
**5. Environmental Science:** Climate Change, Pollution Analysis, Sustainability, Water Resource Management
**6. Space Science:** Astronomy, Satellites, Astrophysics, Space Exploration
**7. Energy:** Solar Energy, Wind Energy, Hydrogen Energy, Battery Technology, Smart Grids
**8. Interdisciplinary Research:** Smart Cities, Sustainable Development, Industry 4.0, Digital Twins, Green Computing, Computational Biology

*Representation:* Displayed as specific categories in UI filters. Used as metadata tags in ChromaDB to restrict vector search spaces, and as foreign keys in PostgreSQL.

---

## 13. Frontend → Backend API Requirements

| Endpoint | Method | Purpose | Required Systems |
| :--- | :--- | :--- | :--- |
| `/api/auth/login` | POST | Authentication | PostgreSQL |
| `/api/dashboard/stats` | GET | Dashboard data | PostgreSQL |
| `/api/papers/search` | POST | Hybrid search (BM25 + Chroma) | ChromaDB, BM25, Reranker |
| `/api/papers/{id}` | GET | Paper details | PostgreSQL |
| `/api/ai/ask` | POST | RAG response generation | ChromaDB, Gemini 2.5 Flash |
| `/api/ai/explain` | GET | Explainability metrics | Backend Logs/Metadata |
| `/api/projects` | GET/POST | Manage Projects | PostgreSQL |
| `/api/notes` | GET/POST | Manage Notes | PostgreSQL |
| `/api/bookmarks` | POST/DELETE | Toggle Bookmarks | PostgreSQL |

---

## 14. Frontend State & Data Flow

- **Zustand State (UI state):** Sidebar toggles, active tabs, modal visibility, theme.
- **Server Data (React Query/Fetch):** Paper lists, project details, user profile. Must be fetched from FastAPI.
- **AI Conversation State:** Managed locally during the session, persisted to the backend on close.
- **Workspace State:** Draft notes held in local state, auto-saved to backend periodically.

*Principle:* UI state ≠ Database state. Mock data in Zustand must be replaced with async API calls.

---

## 15. Authentication & User Data

**Flow:** Register → Login → JWT Authentication → Dashboard Access.
User data includes profile, projects, notes, bookmarked papers, and conversation history. 
*Constraint:* Custom JWT authentication via FastAPI. Do not use external providers (Auth0/Firebase) unless explicitly approved.

---

## 16. Current Mock Functionality vs Final Backend Functionality

| Current Frontend | Final Implementation |
| :--- | :--- |
| Mock papers (`data.ts`) | PostgreSQL + ChromaDB |
| Mock search (Zustand) | BM25 + Semantic Retrieval (FastAPI) |
| Mock AI response | Gemini 2.5 Flash + RAG |
| Mock domains (Hardcoded UI) | Domain database/configuration |
| Mock projects/notes | PostgreSQL |
| Mock bookmarks | PostgreSQL |
| Mock explainability | Actual Retrieval metadata + citations |

---

## 17. Deployment Architecture

**User Browser** → **Vercel** (React Frontend)
↓ (HTTPS/REST API)
**Render** (FastAPI Backend)
↓
**Research Engine** (LlamaIndex, BM25, RRF, BGE Reranker)
↓
**Databases:** PostgreSQL (Render/Neon), ChromaDB (Render/Hosted)
**External APIs:** Gemini 2.5 API, Academic Repositories (PubMed, arXiv, etc.)

*Required Configs:* `CORS_ORIGINS`, `DATABASE_URL`, `GEMINI_API_KEY`, `CHROMA_URL`.

---

## 18. Security Requirements

- JWT-based authentication.
- Passwords hashed via bcrypt.
- API keys hidden in backend environment variables (never exposed to frontend).
- Strict CORS policies allowing only Vercel frontend.
- Input sanitization and parameterized queries to prevent SQL injection.
- Secure API communication (HTTPS).

---

## 19. Performance Requirements

- **Strategy:** Prioritize fast local retrieval from the pre-built 670-paper knowledge base.
- **Vector Search:** Efficient indexing via ChromaDB.
- **Dynamic Fallback:** Background ingestion triggered *only* when local RRF confidence scores fall below a threshold.
- Avoid unnecessary re-ingestion by checking DOI/titles against PostgreSQL before processing.

---

## 20. Features NOT to Change (Locked Features)

> [!IMPORTANT]
> The following elements are finalized and MUST NOT be redesigned or altered without explicit approval.

- ResearchNexus AI branding
- Current overall UI direction and White premium academic theme
- Research OS concept
- 8-domain structure
- Local-first retrieval strategy with Dynamic ingestion fallback
- Hybrid Retrieval (BM25 + Chroma)
- Reciprocal Rank Fusion (RRF) & BGE re-ranking
- Enhanced RAG with Gemini 2.5 Flash
- Explainable AI transparency requirements
- Research Workspace concept
- Final module structure

---

## 21. Features That Are Future Scope

*Do not implement these in the current phase:*
- Knowledge graph visualization
- Collaborative research (multiplayer)
- Multi-language support
- Personalized recommendations
- User PDF upload (unless separately approved)

---

## 22. Implementation Phases

- **Phase 1:** Backend foundation + PostgreSQL setup
- **Phase 2:** Local knowledge-base integration (Loading the 670 papers)
- **Phase 3:** Hybrid Retrieval implementation (BM25 + Chroma + RRF + BGE)
- **Phase 4:** Dynamic Data Ingestion logic
- **Phase 5:** Gemini 2.5 Flash + Enhanced RAG integration
- **Phase 6:** Explainable AI metric tracking
- **Phase 7:** Connect frontend modules to APIs (replacing mock data)
- **Phase 8:** Authentication + user workspace integration
- **Phase 9:** Testing + evaluation
- **Phase 10:** Deployment (Vercel + Render)

---

## 23. Testing & Evaluation Plan

- **Retrieval:** Test precision/recall of the 670 local papers. Verify RRF and BGE reranking quality.
- **RAG:** Evaluate answer relevance, strict evidence grounding, correct citation mappings, and zero hallucination.
- **System:** Monitor API response times, database consistency, and successful dynamic ingestion fallback.
- **User Experience:** Verify search usability, workspace persistence, and clear XAI metrics.

---

## 24. Final Acceptance Criteria

1. User can register/login.
2. User can search using natural language.
3. Local 670-paper knowledge base is successfully searched.
4. BM25 and semantic retrieval execute correctly.
5. RRF combines results and BGE reranker refines them.
6. Dynamic ingestion safely activates when local results are insufficient.
7. New papers are processed, chunked, and indexed.
8. Gemini generates answers using strictly retrieved context.
9. Answers contain supporting inline citations.
10. Explainability information is clearly displayed.
11. Users can save papers, projects, and notes successfully.
12. Literature Review Builder functions.
13. Frontend and backend communicate correctly without relying on mock data.
14. Production deployment is live and functioning.

---

## 25. FINAL IMPLEMENTATION LOCK

### LOCKED — DO NOT CHANGE
- The premium UI design, glassmorphism theme, and component layouts.
- The 8-domain architectural structure.
- The 670-paper local knowledge base requirement.
- The Hybrid Retrieval pipeline (BM25 + Chroma + RRF + BGE + Gemini 2.5 Flash).
- The dynamic ingestion fallback logic.

### IMPLEMENT — REQUIRED
- Complete FastAPI backend construction.
- PostgreSQL and ChromaDB setup and schema creation.
- Python data ingestion and document intelligence pipeline (PyMuPDF + LlamaIndex).
- Replacement of all Zustand mock data with React Query/Fetch API calls.
- JWT Authentication flow.
- The Explainable AI backend logic to track and return chunk rankings and citations.

### PENDING DECISION
- **Dynamic Ingestion Threshold:** What specific confidence score/threshold dictates when local results are "insufficient"?
- **API Keys for External Repositories:** Do we require paid API access for AGRIS/PubMed, or are we strictly using public free tiers?
- **Vector DB Hosting:** Will ChromaDB be hosted via a managed service or self-hosted on a persistent Render disk?
