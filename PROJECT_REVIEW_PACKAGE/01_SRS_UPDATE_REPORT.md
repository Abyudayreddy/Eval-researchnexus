# Software Requirements Specification (SRS)
## ResearchNexus AI: An Explainable Research Assistant Using Hybrid Retrieval, XAI, and Enhanced RAG

---

## Table of Contents
1. [Introduction](#1-introduction)
   - 1.1 Purpose
   - 1.2 Scope
   - 1.3 Definitions, Acronyms, and Abbreviations
   - 1.4 References
   - 1.5 Document Overview
2. [Overall Description](#2-overall-description)
   - 2.1 Product Perspective
   - 2.2 Product Functions
   - 2.3 User Classes and Characteristics
   - 2.4 Operating Environment
   - 2.5 Design and Implementation Constraints
   - 2.6 User Documentation
   - 2.7 Assumptions and Dependencies
3. [External Interface Requirements](#3-external-interface-requirements)
   - 3.1 User Interface
   - 3.2 Hardware Interface
   - 3.3 Software Interface
   - 3.4 Communication Interface
4. [System Features](#4-system-features)
   - 4.1 User Authentication
   - 4.2 Dashboard
   - 4.3 Research Domain Management
   - 4.4 Hybrid Search & Retrieval
   - 4.5 Dynamic Data Ingestion
   - 4.6 AI Research Assistant
   - 4.7 Explainable AI (XAI)
   - 4.8 Research Workspace
   - 4.9 Literature Review Builder
   - 4.10 Notebook
   - 4.11 Project Management
   - 4.12 Paper Library
   - 4.13 Analytics
   - 4.14 Notifications
   - 4.15 Global Search
   - 4.16 Evaluation & Publication Console (Phase 3.10)
5. [Other Nonfunctional Requirements](#5-other-nonfunctional-requirements)
   - 5.1 Performance Requirements
   - 5.2 Safety Requirements
   - 5.3 Security Requirements
   - 5.4 Software Quality Attributes
   - 5.5 Business Rules
6. [Other Requirements](#6-other-requirements)
   - 6.1 Software Requirements
   - 6.2 Hardware Requirements
- [Appendix A: Glossary](#appendix-a-glossary)
- [Appendix B: Analysis Models](#appendix-b-analysis-models)
- [Appendix C: To Be Determined (TBD) List](#appendix-c-to-be-determined-list)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document details the complete functional, non-functional, and structural requirements for **ResearchNexus AI** (also known as ResearchMind), an explainable research assistant operating system. The document serves as the authoritative technical contract for developers, software architects, AI researchers, and academic evaluation committees (SDC-II review panel). It governs the system's design, implementation, verification, and publication-ready evaluation frameworks.

### 1.2 Scope
ResearchNexus AI is an advanced, domain-aware research assistant designed to alleviate information overload, hallucinated citations, and opaque retrieval in academic literature synthesis. 
The software provides:
1. **Hybrid Local & Multi-Repository Retrieval:** Concurrent sparse (PostgreSQL ILIKE + BM25) and dense vector (ChromaDB) search fused via Reciprocal Rank Fusion (RRF, $k=60$) and reranked using a cross-encoder model (BAAI/bge-reranker-base), coupled with 5 live online connectors (arXiv, OpenAlex, PMC, AGRIS, NASA ADS).
2. **Explainable AI (XAI) Engine:** Transparent 10-stage local execution timelines, 8-stage online timelines, search ID validation, and interactive "Why This Paper?" provenance drawers.
3. **Context-Bound Enhanced RAG Workspace:** 5 interaction modes (Research, Paper, Compare, Evidence, Upload), 5 context scopes, SHA-256 context hashing, eligibility routing, Stage A deterministic + Stage B semantic claim verification (6 claim types, 5 verification statuses), conservative citation repair, and bounded iterative refinement (max 2 passes) with anti-oscillation safeguards.
4. **Isolated Personal Corpus Management (Phase 3.8):** Dedicated Chroma vector collection namespaces isolating uploaded researcher documents from global corpora.
5. **Session Memory & Soft Delete Model (Phase 3.9):** Explicit non-destructive deletion using `deleted_at` fields and structured provenance basis tagging (`USER_RECORDED`, `EVIDENCE_DERIVED`, `AI_SUGGESTED`).
6. **Evaluation & Publication Console (Phase 3.10):** A baseline-locked evaluation framework supporting 8 predefined baselines ($B0$ to $B7$), RRF parameter sensitivity sweeps ($k \in \{20, 40, 60, 100\}$), ablation matrix generation, 7-dimension blinded human evaluation, claim audit logging, one-click reproducibility package export, and strict **NOT MEASURED** metric UI governance.

### 1.3 Definitions, Acronyms, and Abbreviations
- **API:** Application Programming Interface
- **BGE:** Beijing Academy of Artificial Intelligence (BAAI) General Embedding model family (`bge-base-en-v1.5`, `bge-reranker-base`).
- **BM25:** Best Matching 25 algorithm for sparse lexical keyword retrieval.
- **ChromaDB:** Open-source vector database utilized for storing 768-dimensional embeddings.
- **Enhanced RAG:** Advanced Retrieval-Augmented Generation featuring context scoping, claim extraction, verification, citation repair, and iterative feedback loops.
- **FastAPI:** High-performance Python web framework used for API endpoints.
- **JWT:** JSON Web Token for stateless user authentication.
- **LLM:** Large Language Model (specifically Google Gemini 3.5 Flash Lite).
- **ORM:** Object-Relational Mapping (SQLAlchemy).
- **PMC:** PubMed Central academic database connector.
- **RAG:** Retrieval-Augmented Generation.
- **RRF:** Reciprocal Rank Fusion ($RRF\_Score = \sum \frac{1}{k + r(d)}$).
- **SDC-II:** Software Development Capstone II / Final Academic Project Review.
- **SRS:** Software Requirements Specification.
- **XAI:** eXplainable Artificial Intelligence.

### 1.4 References
1. IEEE Std 830-1998: *IEEE Recommended Practice for Software Requirements Specifications*.
2. Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS.
3. Cormack, G. V., Clarke, C. L., & Buettcher, S. (2009). *Reciprocal Rank Fusion Outperforms Data Fusion Algorithms*. SIGIR.
4. BAAI Embedding Tech Report (2023). *BGE: Open-source Embeddings and Rerankers*.
5. Phase 3.1 – 3.10 Lock Reports and Codebase Architecture Specifications, ResearchNexus AI (2026).

### 1.5 Document Overview
This document follows the standard IEEE 830 structure. Section 2 outlines the general product perspective, user personas, operating context, and design constraints. Section 3 details external interface requirements (UI, Hardware, Software, Communication). Section 4 provides an exhaustive specification of all 16 system features (including user authentication, hybrid search, XAI, RAG, and evaluation console). Section 5 outlines non-functional requirements (Performance, Security, Quality Attributes, Business Rules). Section 6 details environment requirements. Appendices provide the glossary, UML analysis models, and TBD items.

---

## 2. Overall Description

### 2.1 Product Perspective
ResearchNexus AI is a self-contained, client-server web application. It operates as an explainable layer above unstructured academic paper corpora and external academic REST APIs.

```
+-------------------------------------------------------------------------+
|                          Presentation Layer                             |
|             React 19 + TypeScript + Vite + TailwindCSS 4               |
|   (Research Explorer, XAI Timelines, Assistant, Evaluation Console UI)  |
+-------------------------------------------------------------------------+
                                   | HTTP / JSON REST APIs
+-------------------------------------------------------------------------+
|                            Application Layer                            |
|                          Python FastAPI Backend                         |
|   +-------------------+ +--------------------+ +--------------------+   |
|   | Search & Retrieval| | Enhanced RAG Engine| | Evaluation Service |   |
|   | Pipeline (RRF,BGE)| | (Verify & Refine)  | | (Baseline B0-B7) |   |
|   +-------------------+ +--------------------+ +--------------------+   |
+-------------------------------------------------------------------------+
                        |                          |
                        v                          v
+-----------------------------------+  +----------------------------------+
|          Relational Data          |  |           Vector Data            |
|       PostgreSQL Database         |  |        ChromaDB Store            |
| (Users, Papers, History, Evaluation|  |  (26,179 Chunks, 768d BGE Vectors,|
|    Datasets, Experiments, Runs)   |  |   Isolated User Collections)     |
+-----------------------------------+  +----------------------------------+
```

### 2.2 Product Functions
Major functions provided by ResearchNexus AI include:
- **Lexical & Semantic Hybrid Search:** Merging sparse BM25 and dense vector results via RRF ($k=60$) followed by cross-encoder BGE reranking.
- **Online Scientific Aggregation:** Real-time polling across arXiv, OpenAlex, PMC, AGRIS, and NASA ADS.
- **Traceable XAI Visualizations:** Exposing 10-stage local execution steps and 8-stage online retrieval states.
- **Context-Scoped RAG Assistance:** Executing queries within 5 distinct interaction modes and 5 strictly enforced context scopes with SHA-256 context hashing.
- **Automated Claim Verification & Repair:** Extracting 6 claim types, evaluating Stage A deterministic and Stage B LLM semantic alignment, assigning 5 verification statuses, and performing conservative citation repair.
- **Bounded Iterative Refinement:** Executing self-feedback loops up to a maximum of 2 passes with anti-oscillation safeguards.
- **Benchmark-Locked Evaluation Console:** Supporting baseline locking ($B0$–$B7$), RRF parameter sweeps, ablation studies, blinded human eval, publication claim audits, and one-click reproducibility package exports.

### 2.3 User Classes and Characteristics
1. **Academic Researchers & Students (Primary Users):** Require fast, verifiable literature search, transparent matching criteria ("Why This Paper?"), structured note-taking, and citation verification.
2. **Peer Reviewers & Faculty Evaluators (Audit Users):** Require reproducible evaluation data, immutable baseline comparisons, blinded evaluation capabilities, and verifiable evidence provenance.
3. **System Administrators / Developers:** Require access to database migration utilities, dataset management, backend test suites, and log inspection.

### 2.4 Operating Environment
- **Client OS:** OS Independent (Modern Web Browsers: Chrome 110+, Firefox 115+, Edge 110+, Safari 16+).
- **Server OS:** Windows 10/11, Linux (Ubuntu 22.04 LTS), macOS.
- **Runtime Engines:** Node.js v18+ (Frontend), Python 3.10+ (Backend).
- **Database Servers:** PostgreSQL 14+, ChromaDB 0.4+.

### 2.5 Design and Implementation Constraints
1. **Strict Provenance Rule:** Every LLM-generated claim must be anchored to explicit evidence (`value`, `value_type`, `evidence_ids`, `support_status`).
2. **Scientific Governance ("NOT MEASURED" Policy):** The UI must never display estimated or hardcoded performance percentages. Unmeasured metrics must explicitly display as **NOT MEASURED**.
3. **Baseline Immutability:** Once an evaluation experiment is created, its baseline configuration JSON is frozen and immutable.
4. **Soft Delete Enforcement:** Deletion of sessions or records must set `deleted_at` timestamps rather than purging records from normal queries.
5. **Latency Bounds:** Total pipeline execution latency enforces a minimum realistic processing floor ($\ge 515.0$ ms) during evaluation simulations.

### 2.6 User Documentation
The system provides inline UI tooltips, context inspector sidebars, interactive timeline drawers, an exported walkthrough guide (`walkthrough.md`), and an IEEE publication preparation report (`03_IEEE_PAPER_DATA.md`).

### 2.7 Assumptions and Dependencies
- Google Gemini API key availability for LLM generation (`gemini-3.5-flash-lite`).
- Local disk storage for PostgreSQL relational data and ChromaDB vector embeddings.
- Active network connectivity for fetching live results from online repository APIs (arXiv, OpenAlex, PMC, AGRIS, NASA ADS).

---

## 3. External Interface Requirements

### 3.1 User Interface
The user interface is implemented in React 19, Vite, and TailwindCSS 4, utilizing Radix UI primitives and Lucide icons. Key screens include:
- **Hybrid Search Explorer (`/search`):** Search input, domain filters, real-time polling indicator, unified local + online results list.
- **XAI Timeline Page (`/xai`):** Interactive 10-stage local execution timeline and 8-stage online retrieval timeline.
- **AI Assistant Workspace (`/assistant`):** Multi-mode selector (Research, Paper, Compare, Evidence, Upload), Context Inspector drawer, Scope Engine toggles, Claim Proof drawers.
- **Evaluation Console (`/evaluation`):** Baseline Selector ($B0$–$B7$), Experiment Runner, Ablation Matrix View, Blinded Human Evaluation Panel (7 rating sliders), Publication Tables, One-Click Export button.
- **Paper Reader (`/reader`):** PDF iframe viewer with text selection and annotation anchors.

### 3.2 Hardware Interface
The application interfaces with server disk drives for PostgreSQL WAL storage and vector index file storage. It utilizes system RAM ($\ge 8$ GB recommended) for hosting in-memory BM25 indices and loading the BGE cross-encoder model.

### 3.3 Software Interface
- **PostgreSQL Database:** Connected via SQLAlchemy ORM using `psycopg2` / `asyncpg` drivers.
- **ChromaDB Vector Store:** Interfaced via native Python `chromadb` client API using `bge-base-en-v1.5` embeddings (768 dimensions).
- **Google Gemini API:** Accessed via official `google-generativeai` SDK using `gemini-3.5-flash-lite`.

### 3.4 Communication Interface
- **HTTP / HTTPS REST APIs:** All client-server communication uses JSON over HTTP/HTTPS REST endpoints.
- **Polling Protocol:** Asynchronous task progress (retrieval and evaluation runs) is monitored by client-side interval polling against task status endpoints.

---

## 4. System Features

### 4.1 User Authentication
- **Description:** Provides secure JWT-based registration, authentication, login state persistence, and profile management.
- **Inputs:** Email, Password, User Metadata.
- **Outputs:** JWT Bearer Token, User Profile Payload.
- **Functional Steps:** Passwords hashed with `passlib` (bcrypt); JWT issued via `python-jose`.

### 4.2 Dashboard
- **Description:** Central overview panel displaying system stats, recent searches, saved research projects, and paper activity heatmaps.
- **Inputs:** Authenticated User Session ID.
- **Outputs:** Aggregated stats JSON (paper counts, project counts, total queries).

### 4.3 Research Domain Management
- **Description:** Classifies papers and evaluation questions into 3 curated domains (Artificial Intelligence, Environmental Science, Interdisciplinary Studies).
- **Inputs:** Domain Selection Flags.
- **Outputs:** Filtered dataset subsets and search constraints.

### 4.4 Hybrid Search & Retrieval
- **Description:** Multi-stage hybrid search combining local corpus and 5 live online academic connectors.
- **Detailed Mechanics:**
  1. **Sparse Lexical Search:** PostgreSQL ILIKE + BM25 keyword scoring over paper titles and abstracts.
  2. **Dense Vector Search:** ChromaDB cosine similarity search using 768-dimensional BGE embeddings.
  3. **Reciprocal Rank Fusion (RRF):** Fuses sparse and dense ranks using $RRF(d) = \sum \frac{1}{60 + rank(d)}$.
  4. **Diversification & Relevance Filtering:** Filters low-relevance chunks and limits chunks per paper to prevent paper dominance.
  5. **BGE Cross-Encoder Reranking:** Re-scores top-K candidates using `BAAI/bge-reranker-base`.
- **Inputs:** Query String, Domain Filter, Top-K Parameters.
- **Outputs:** Merged and reranked paper evidence array with explicit pre-rerank and post-rerank ranks.

### 4.5 Dynamic Data Ingestion
- **Description:** Ingests academic PDFs, extracts raw text via PyPDF, splits documents into 512-token chunks with 50-token overlap via LlamaIndex `SentenceSplitter`, and generates BGE embeddings.
- **Inputs:** PDF Files / Document Streams.
- **Outputs:** ChromaDB vector entries and PostgreSQL metadata rows.

### 4.6 AI Research Assistant
- **Description:** Multi-mode LLM assistant providing grounded academic answers.
- **Interaction Modes:**
  - `RESEARCH_MODE`: Broad literature synthesis.
  - `PAPER_MODE`: Deep single-paper interrogation.
  - `COMPARE_MODE`: Structured multi-paper comparative analysis.
  - `EVIDENCE_MODE`: Extraction of explicit evidence tables with provenance cells.
  - `UPLOAD_MODE`: Q&A restricted to researcher-uploaded documents.
- **Inputs:** User Prompt, Selected Mode, Active Scope.
- **Outputs:** Grounded response text with inline citation tags (`[1]`, `[2]`), provenance cells, and verification badges.

### 4.7 Explainable AI (XAI)
- **Description:** Exposes complete internal retrieval and generation state to the user.
- **Components:**
  - **10-Stage Local Timeline:** Query Preprocessing, Metadata Filter, BM25 Search, Dense Vector Search, RRF Fusion, Relevance Filter, Paper Diversification, BGE Reranking, Context Assembly, LLM Generation.
  - **8-Stage Online Timeline:** Query Translation, API Dispatch (arXiv, OpenAlex, PMC, AGRIS, NASA ADS), Response Parsing, Deduplication, Metadata Normalization, Scoring, Fusion, Display.
  - **"Why This Paper?" Drawer:** Displays BM25 rank, Dense rank, RRF score, Pre-Rerank rank, BGE rank, BGE score, and filter decisions.

### 4.8 Research Workspace
- **Description:** Integrated interface managing context scopes, context inspector, and context snapshots.
- **Context Scopes:** `LOCAL_ONLY`, `ONLINE_ONLY`, `HYBRID_ALL`, `PROJECT_BOUND`, `UPLOAD_BOUND`.
- **Context Snapshots:** Generates immutable SHA-256 hashes of retrieved context to guarantee query reproducibility.

### 4.9 Literature Review Builder
- **Description:** Synthesizes literature reviews across retrieved papers, outputting structured section outlines, methodology comparisons, and evidence gaps.

### 4.10 Notebook
- **Description:** Full CRUD note-taking application allowing researchers to save markdown notes linked to specific papers and research projects.

### 4.11 Project Management
- **Description:** Allows researchers to organize literature into discrete research projects, linking papers, notes, and search histories.

### 4.12 Paper Library
- **Description:** Personal bookmarking and library system with tagging, project assignment, and PDF viewing capabilities.

### 4.13 Analytics
- **Description:** Tracks user search frequency, paper view counts, verification failure rates, and activity heatmaps over time.

### 4.14 Notifications
- **Description:** System status notifications for asynchronous search task completion, evaluation run completions, and rate limit alerts.

### 4.15 Global Search
- **Description:** Fast global navigation search bar enabling quick lookups across saved projects, bookmarks, notes, and past search histories.

### 4.16 Evaluation & Publication Console (Phase 3.10)
- **Description:** Comprehensive framework making system evaluation scientifically defensible and publication-ready.
- **Sub-Features:**
  1. **Baseline Locking ($B0$–$B7$):**
     - $B0$: Zero-shot LLM (`B0_LLM_ONLY`).
     - $B1$: Standard Dense RAG (`B1_DENSE_RAG`).
     - $B2$: Standard Sparse RAG (`B2_BM25_RAG`).
     - $B3$: Hybrid RAG without reranker (`B3_HYBRID_RAG`).
     - $B4$: Hybrid RAG + BGE Reranker (`B4_HYBRID_BGE`).
     - $B5$: Enhanced RAG Pipeline (`B5_ENHANCED_RAG`).
     - $B6$: Enhanced RAG + Claim Verification (`B6_ENHANCED_VERIFICATION`).
     - $B7$: Complete Iterative RAG (`B7_ITERATIVE_RAG`).
  2. **RRF Sensitivity Study:** Evaluates retrieval performance across $k \in \{20, 40, 60, 100\}$.
  3. **Ablation Study Matrix:** Evaluates full system versus minus-one component variants.
  4. **Blinded Human Evaluation Panel:** Collects double-blind human ratings across 7 dimensions (Relevance, Completeness, Correctness, Citation Accuracy, Clarity, Conciseness, Overall Trust).
  5. **Publication Claim Audit:** Audits all generated claims against evidence, assigning support statuses.
  6. **Reproducibility Package Export:** One-click JSON package generator bundling metric tables, claim audit logs, and experiment configurations.
  7. **Strict "NOT MEASURED" Policy:** Unrun metrics strictly render as **NOT MEASURED** in the UI.

---

## 5. Other Nonfunctional Requirements

### 5.1 Performance Requirements
- **Local Retrieval Latency:** Sparse + Dense + RRF search completed in $< 1.5$ seconds.
- **BGE Reranking Latency:** Cross-encoder reranking of top-20 candidates completed in $< 800$ ms.
- **Evaluation Simulation Latency Floor:** Enforces a minimum realistic total processing floor of $\ge 515.0$ ms.
- **UI Responsiveness:** Frontend components re-render within $< 100$ ms upon state changes.

### 5.2 Safety Requirements
- **Anti-Hallucination Safeguards:** AI assistant responses require verification against retrieved chunks; unverified claims are flagged with warning badges.
- **Loop Safeguards:** Iterative refinement is strictly bounded to a maximum of 2 cycles with anti-oscillation feedback signatures.

### 5.3 Security Requirements
- **Authentication:** JWT tokens signed with SHA-256 secret keys; passlib bcrypt password hashing.
- **Corpus Isolation (Phase 3.8):** User-uploaded documents are stored in dedicated Chroma vector collections to prevent cross-user data leakage.
- **Input Sanitization:** API parameters validated via Pydantic models to prevent injection attacks.

### 5.4 Software Quality Attributes
- **Maintainability:** Modular separation between API routers, domain services, SQLAlchemy ORM models, and Zustand frontend stores.
- **Testability:** Full unit test coverage for evaluation models, service methods, and XAI pipelines (30 backend evaluation tests + 37 XAI tests passed).
- **Reproducibility:** SHA-256 context hashing and immutable evaluation experiment configurations.

### 5.5 Business Rules
1. **Scientific Integrity:** Unrun metrics must render as **NOT MEASURED**; no fabricated or estimated percentages permitted.
2. **Provenance Mandatory:** Every cell in an evidence table must contain `value`, `value_type`, `evidence_ids`, and `support_status`.
3. **Soft Delete Mandate:** Session deletion sets `deleted_at` timestamps without purging historical evaluation data.

---

## 6. Other Requirements

### 6.1 Software Requirements
- **Python:** Version 3.10 or higher.
- **FastAPI:** Version 0.100+
- **SQLAlchemy:** Version 2.0+
- **ChromaDB:** Version 0.4+
- **Node.js:** Version 18.0 or higher.
- **React:** Version 19.0
- **TypeScript:** Version 5.0+

### 6.2 Hardware Requirements
- **Processor:** Dual-core Intel Core i5 / AMD Ryzen 5 or better (Quad-core recommended for BGE reranking).
- **RAM:** Minimum 8 GB (16 GB recommended).
- **Disk Space:** Minimum 10 GB available SSD storage for datasets, vector databases, and evaluation logs.

---

## Appendix A: Glossary

- **Claim Verification:** The process of parsing generated text into discrete claims and validating them against retrieved context chunks using Stage A deterministic logic and Stage B LLM semantic checking.
- **Citation Repair:** Automated realignment of inline citations (`[1]`, `[2]`) to point to the correct supporting evidence chunk when mismatched.
- **Provenance Cell:** Structured evidence object containing explicit text values, data types, supporting chunk IDs, and verification statuses.
- **Reciprocal Rank Fusion (RRF):** A rank aggregation algorithm combining rankings from multiple retrieval systems without needing normalized scores.

---

## Appendix B: Analysis Models

### B.1 Entity-Relationship Diagram (Evaluation Console Subsystem)

```
+-------------------+        1:N        +-------------------+
| EvaluationDataset | ----------------> |  EvaluationItem   |
+-------------------+                   +-------------------+
| dataset_id (PK)   |                   | item_id (PK)      |
| name              |                   | dataset_id (FK)   |
| version           |                   | split (DEV/VAL/TST|
| item_count        |                   | question          |
+-------------------+                   | gold_claims_json  |
          |                             +-------------------+
          | 1:N                                   |
          v                                       | 1:N
+--------------------+                            v
|EvaluationExperiment| 1:N              +-------------------+
+--------------------+ ---------------> |   EvaluationRun   |
| experiment_id (PK) |                  +-------------------+
| dataset_id (FK)    |                  | run_id (PK)       |
| baseline_id (B0-B7)|                  | experiment_id(FK) |
| config_json (FREEZE|                  | item_id (FK)      |
| status             |                  | answer_text       |
+--------------------+                  | latency_json      |
                                        | verification_json |
                                        +-------------------+
```

### B.2 Enhanced RAG State Machine

```
   +-------------+
   | Query Recv  |
   +-------------+
          |
          v
   +-------------+      NO       +------------------+
   | Eligible?   | ------------> | Direct Generation|
   +-------------+               +------------------+
          | YES
          v
   +-------------+
   | Hybrid RRF  |
   +-------------+
          |
          v
   +-------------+
   | BGE Rerank  |
   +-------------+
          |
          v
   +-------------+
   | Deduplicate |
   +-------------+
          |
          v
   +-------------+
   | LLM Generate|
   +-------------+
          |
          v
   +-------------+
   | Verify Claim|
   +-------------+
          |
   +------+------+
   |             |
 UNSUPPORTED  SUPPORTED
   |             |
   v             v
+------+   +-----------+
|Pass<2|   | Output Res|
+------+   +-----------+
   | YES
   v
+------+
|Refined| (Max 2 Passes)
+------+
```

---

## Appendix C: To Be Determined (TBD) List

1. **TBD-01:** Empirical benchmark metrics (Recall@10, Precision@5, Claim Support Rate) across evaluation datasets will be populated upon execution of experiment runs in the Evaluation Console.
2. **TBD-02:** Multi-language processing support for non-English research papers (currently standardizing on English academic literature).
3. **TBD-03:** Cloud production deployment automated CI/CD pipeline targeting Render for FastAPI backend and Vercel for React frontend.

---
*End of Software Requirements Specification*
