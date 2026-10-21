# SDC-II REVIEW PPT CONTENT (SLIDES 1 TO 6)
## Project: ResearchMind / ResearchNexus AI
**System Description:** Explainable AI-Powered Scientific Research Assistant & Research OS  
**Evaluation Target:** Official 6-Slide SDC-II Project Presentation  
**Corpus & Benchmark Base:** `ds_nexus_v10` (100 gold questions, 670 local papers / 14,850 semantic chunks)  
**Associated Presentation File:** `SDC Review 1/SDC_II_Review_Presentation.pptx`

---

## SLIDE 1: BASE PAPER & RESEARCH GAP

### Slide Title: Base Paper Analysis & Research Gap
**Header Subtitle:** Reference Literature: OpenScholar (Asai et al., 2024) vs. Proposed ResearchNexus Architecture

#### 1. Base Paper Summary
* **Title:** *"OpenScholar: Synthesizing Scientific Literature with Open Datastores and Language Models"* (Asai et al., 2024).
* **Core Problem Addressed:** Automated multi-paper scientific literature synthesis over an open-access paper datastore (OSDS: ~45 million open papers).
* **Base Paper Architecture:** Dense vector retrieval (Bi-Encoder) $\rightarrow$ Cross-Encoder Reranker $\rightarrow$ Fine-tuned open LLM generation (Llama-3/Mistral).
* **Key Findings:** Demonstrated that RAG over an open academic datastore outperforms general commercial LLMs in factual grounding.

#### 2. Limitations of Existing System & Base Paper
* **Dense Retrieval Misses Keywords:** Relying purely on vector similarity misses exact technical acronyms, model names (e.g., `"ds_nexus_v10"`), DOIs, or quantitative formulas.
* **Black-Box Blackhole:** Provides no explainability trace into why specific papers were selected or how reranking modified search order.
* **Passive Citation Hallucination:** Standard RAG outputs citations as decorative formatting; LLMs continue to blend parametric memory, causing a 15–25% unsupported claim rate.
* **No Post-Generation Repair:** Lacks automated NLI verification to detect and repair incorrect inline citation tags.

#### 3. Research Gap & Proposed Extension
* **The Gap:** Lack of an open, explainable RAG architecture combining hybrid keyword-semantic search with post-hoc NLI claim verification and automated citation repair without requiring model fine-tuning.
* **Our Extension:**
  1. **Hybrid Retrieval:** Fuses sparse BM25 keyword matching with ChromaDB vector search (`bge-base-en-v1.5`) via Reciprocal Rank Fusion ($RRF_k = 60$).
  2. **BGE Cross-Encoder Reranking:** Evaluates joint query-snippet cross-attention using `bge-reranker-base`.
  3. **Explainable AI (XAI) Trace Modal:** Exposes exact BM25 scores, vector distances, RRF ranks, and BGE rank shifts ($\Delta r$).
  4. **Phase 3.4 Claim Verification & Citation Repair:** Sentence-level NLI entailment classification that dynamically re-links invalid citations to verified source chunks.

---

## SLIDE 2: REQUIREMENTS

### Slide Title: Project Objectives & System Requirements
**Header Subtitle:** Problem Formalization, Stakeholders, Use Cases, and Functional Scope

#### 1. Problem Statement & Motivation
* **Problem:** Manual literature review across hundreds of PDFs takes days; general AI chatbots generate smooth answers but introduce fake citations and misattributed quotes.
* **Motivation:** Build a fast, transparent, and audit-ready scientific assistant that guarantees citation precision $>95\%$ and eliminates unsupported claim hallucinations.

#### 2. System Objectives
* **Primary Objective:** Deliver an end-to-end scientific research OS with verifiable evidence attribution and sub-second retrieval performance.
* **Specific Objectives:**
  - Implement RRF hybrid search ($k=60$) combining BM25 and ChromaDB.
  - Enforce Phase 3.3 Enhanced RAG context bounding on Gemini 2.5 Flash (`temp=0.0`).
  - Develop Phase 3.4 NLI Claim Verifier & Citation Repair engine.
  - Provide glassmorphism XAI traces for full algorithmic transparency.

#### 3. Stakeholders & Target Audience
* **Undergraduate Students:** Finding core literature, understanding domain basics, and generating initial summaries.
* **Postgraduate Scholars & Faculty:** Conducting multi-paper comparative literature reviews and identifying open research gaps.
* **Domain Scientists & Corporate R&D:** Extracting specific quantitative findings with 100% evidence traceability.

#### 4. Key Functional Features & Use Cases
* **Research Explorer:** Multi-modal discovery engine across local domains and 6 external academic APIs.
* **AI Assistant:** Grounded synthesis with context scope controls (`All Research`, `Selected Papers`, `Single Paper`).
* **Multi-Paper Comparison Matrix:** Side-by-side comparative analysis of 2 to 5 papers across 10 dimensions.
* **Personal Research Corpus:** User-isolated custom PDF uploads with PyMuPDF parsing and sliding-window chunking.
* **Research Sessions & Memory:** SQLite state persistence saving queries, chats, and evidence across reloads.

---

## SLIDE 3: DESIGN AND ARCHITECTURE

### Slide Title: System Architecture & Workflow Design
**Header Subtitle:** Technology Stack, Dual-Database Model, and End-to-End Execution Flow

#### 1. Complete Technology Stack
* **Frontend:** React 18, TypeScript 5, Vite 5 (SPA compiled in 13.04s), Tailwind CSS, Zustand state management.
* **Backend:** FastAPI (Python 3.13) async ASGI framework with Pydantic schema validation & SQLAlchemy ORM.
* **Dual Database Architecture:**
  - **SQLite / PostgreSQL:** Structured metadata (paper titles, authors, DOIs, user accounts, sessions, test run logs).
  - **ChromaDB Vector Store:** 14,850 768-dimensional float vectors indexed using HNSW Approximate Nearest Neighbor search.
* **AI Models & Frameworks:** PyMuPDF (`fitz`), LlamaIndex (512/64 sliding window), `bge-base-en-v1.5` (Embedding), `bge-reranker-base` (Cross-Encoder), Gemini 2.5 Flash (Generative LLM).

#### 2. System Architecture Diagram (Text Representation)
```
                    USER
                      │
                      ▼
              REACT FRONTEND UI (Vite 5 SPA)
                      │
                      ▼
             FASTAPI REST BACKEND (Python 3.13)
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
   PostgreSQL / SQLite           ChromaDB
(Paper Metadata & Sessions)  (14,850 768-dim Vectors)
        │                           │
        └─────────────┬─────────────┘
                      ▼
               RETRIEVAL LAYER
              ┌───────┴───────┐
              ▼               ▼
         BM25 Sparse     Dense Vector
         (rank_bm25)     (BGE-v1.5)
              └───────┬───────┘
                      ▼
            Reciprocal Rank Fusion
                   (RRF k=60)
                      │
                      ▼
            BGE Cross-Encoder Reranker
               (bge-reranker-base)
                      │
                      ▼
             Gemini 2.5 Flash LLM
             (Phase 3.3 Enhanced RAG)
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      XAI Trace   Claim Verifier Refinement Loop
     (Exposes Math) (Stage A/B NLI)  (Max 2 Cycles)
          │           │           │
          └───────────┼───────────┘
                      ▼
            FINAL RESEARCH OUTPUT
```

#### 3. Core Component Workflows
* **Hybrid Retrieval Workflow:** Parallel BM25 + ChromaDB $\rightarrow$ RRF score fusion ($S_{\text{RRF}} = \sum \frac{1}{60 + r}$) $\rightarrow$ Top 20 candidates $\rightarrow$ BGE Cross-Encoder reranking $\rightarrow$ Top 5 context snippets.
* **Claim Verification Workflow:** Draft Answer $\rightarrow$ Stage A regex claim extraction $\rightarrow$ Stage B Gemini NLI entailment check (`ENTAILES`, `NEUTRAL`, `CONTRADICTS`) $\rightarrow$ Citation Repair (re-linking invalid tags to entailing chunks) $\rightarrow$ Verified Output.

---

## SLIDE 4: DATASET AND IMPLEMENTATION

### Slide Title: Implementation Progress & Dataset Pipeline
**Header Subtitle:** Implementation Status (100% Core System Verified), Dataset Splits, and Preprocessing Flow

#### 1. Implementation Progress Summary
* **Core System Status:** **100% Implemented, Tested & Verified** (112/112 backend pytests passing).
* **Overall Platform Roadmap Completion:** Estimated at **92%**.
* **Publication Audit Score:** **143 / 170 Points (84.1% — SUBMISSION READY)**.

#### 2. Dataset Breakdown (`ds_nexus_v10` & Local Knowledge Base)
* **Local Pre-Built Corpus:** 670 full-text research papers parsed into 14,850 semantic chunks.
* **Local Production Domains:** Artificial Intelligence (300), Environmental Science (190), Interdisciplinary Research (180), **Material Science** (Active domain).
* **External Dynamic APIs (6 Sources):** arXiv, PubMed Central (PMC), AGRIS, NASA ADS, OpenAlex, Crossref.
* **Benchmark Suite (`ds_nexus_v10`):** 100 gold-annotated scientific queries split into 70 DEVELOPMENT, 15 VALIDATION, and **15 FROZEN TEST** items.

#### 3. Document Preprocessing Pipeline
```
PDF File ──► PyMuPDF Extraction ──► Regex Cleaning ──► Section Detection ──► Sliding Window (512/64) ──► BGE Vector ──► Storage
```
1. **Layout Extraction:** PyMuPDF (`fitz`) parses text blocks sorted by vertical/horizontal coordinates.
2. **Cleaning:** Regex strips running headers, footers, and fixes broken hyphens (`trans- \n former` $\rightarrow$ `transformer`).
3. **Section Detection:** Tagging structural sections (`Abstract`, `Methodology`, `Results`, `Conclusion`).
4. **Semantic Chunking:** LlamaIndex sliding-window split into 512-token chunks with 64-token overlap.
5. **Embedding & Storage:** `bge-base-en-v1.5` generates 768-dim vectors stored in ChromaDB; metadata saved in SQLite/PostgreSQL.

#### 4. Demonstration Script Sequence
* **Step 1:** Open Explorer, select domain `Material Science`, type query, view live execution stepper.
* **Step 2:** Click "Inspect XAI Trace" on result card to expose BM25 terms, vector distance, RRF rank, and BGE score shift.
* **Step 3:** Synthesize answer in AI Assistant using Phase 3.3 Enhanced RAG context bounding.
* **Step 4:** Open Claim Verification drawer to demonstrate Stage A/B NLI entailment badges (`VERIFIED`, `REPAIRED`).

---

## SLIDE 5: RESULTS, CHALLENGES AND NEXT STEPS

### Slide Title: Empirical Benchmark Results, Challenges & Roadmap
**Header Subtitle:** Controlled Experiments (E01–E05), Statistical Tests, Engineering Fixes, and Next Steps

#### 1. Empirical Benchmark Results (`ds_nexus_v10` Frozen TEST Split $N=15$)

| Stage | Experiment ID & Pipeline Variant | Primary Metric | Baseline | Experimental | Delta ($\Delta$) | Statistical Significance | Latency (P50) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **E01** | **Retrieval Baseline** (B1 Dense vs B3 Hybrid) | MRR | 0.650 | **0.812** | **$+0.162$** | Wilcoxon $p = 0.0002$ | 18.2 ms |
| **E02** | **BGE Reranking** (B3 Hybrid vs B4 BGE) | MRR (TEST)<br>Hit@1 | 0.900<br>0.800 | **0.972**<br>**0.933** | **$+0.072$**<br>**$+0.133$** | Wilcoxon $p = 0.0381$<br>0 rank regressions | 60.9 ms<br>($+42.5$ms) |
| **E03** | **Enhanced RAG** (B5R Conv vs B5E Enhanced) | Citation Prec. | 0.733 | **0.947** | **$+0.214$** | Wilcoxon $p = 0.0120$ | 433.6 ms |
| **E04** | **Claim Verification** (B6A Unverified vs B6V Verified) | Citation Prec.<br>Unsupp. Rate | 0.750<br>0.160 | **0.980**<br>**0.010** | **$+0.230$**<br>**$-0.150$** | Wilcoxon $p = 0.0080$<br>15 Citations Repaired | $+340.0$ ms overhead |
| **E05** | **Iterative Refinement** (B7A Single vs B7R Refined) | Citation Prec.<br>Unsupp. Rate | 0.965<br>0.030 | **0.992**<br>**0.010** | **$+0.027$**<br>**$-0.020$** | Wilcoxon $p = 0.0035$<br>Max 2 Cycle Cap | 1253.3 ms<br>($+753$ms) |

#### 2. Engineering Challenges & Resolutions
* **Bi-Encoder Keyword Misses:** Vector search missed exact acronyms $\rightarrow$ Solved via RRF ($k=60$) sparse-dense fusion and BGE reranking (MRR 0.887 / 0.972).
* **Parametric Memory Context Leakage:** LLM inserted unverified outside facts $\rightarrow$ Solved via Phase 3.3 Enhanced RAG context bounding (Citation Precision 94.7%).
* **Invalid Citation Tag Association:** LLM attached decorative citation tags $\rightarrow$ Solved via Phase 3.4 NLI Claim Verification & Citation Repair (Unsupported Rate 1.0%).

#### 3. Future Roadmap & Next Steps
* **Immediate Fixes:** Integrate OCR layer (Tesseract/Surya) for scanned PDFs; add local API caching.
* **Short-Term Engineering:** Scale local corpus to 5,000+ papers; implement adaptive RRF $k$ parameter tuning.
* **Research Extensions:** Expand frozen TEST split to $N=100$ items; conduct double-blind human evaluation trial.

---

## SLIDE 6: RESEARCH & PAPER PUBLICATION PROGRESS

### Slide Title: Manuscript Progress & Research Contribution
**Header Subtitle:** Publication Checklist, Target Venues, Manuscript Status, and Defending Research Novelty

#### 1. Honest Publication Readiness Parameters

| Parameter | Current Honest Status Claim | Supporting Evidence Base |
| :--- | :--- | :--- |
| **Target Venues** | ACL/EMNLP System Demos, CIKM Applied Track, IEEE Access | Section 35 of audit report |
| **Final Paper Title** | Title Under Finalization (*"ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis"*) | Manuscript candidate list |
| **Literature Survey** | **COMPLETED** (28 formal academic references analyzed) | Literature review draft section |
| **Research Gap** | **COMPLETED** (Identified lack of verified RAG with post-hoc citation repair) | Section 21 of audit report |
| **Research Contribution** | **COMPLETED** (RRF + BGE + NLI Stage A/B Citation Repair Architecture) | Section 4 of audit report |
| **Methodology & Architecture**| **COMPLETED** (5-stage isolated pipeline) | System block diagrams & code |
| **Results & Analysis** | **COMPLETED** (E01-E05 empirical benchmark tables & Wilcoxon tests) | Benchmark E01–E04 reports |
| **Paper Writing Status** | **NEAR COMPLETE** (Full IEEEtran & Springer LNCS drafts compiled) | Audit Score: 143/170 (84.1%) |
| **Publication Status** | **READY FOR INTERNAL REVIEW** (Not yet formally submitted) | Publication readiness checklist |

#### 2. Defending Research Contribution vs. Software Engineering
* **What is NOT the contribution:** Using pre-trained APIs like Gemini 2.5 Flash or BGE embeddings is software integration, not primary research novelty.
* **What IS the Research Contribution:**
  1. **Phase 3.4 Stage A/B Claim Verification & Citation Repair Algorithm:** A novel post-generation NLI entailment workflow that detects hallucinated references and automatically re-links claims to entailing corpus chunks.
  2. **Phase 3.3 Enhanced RAG Context Bounding Framework:** Deterministic prompt boundary design eliminating parametric memory context leakage.
  3. **Empirical Benchmarking (`ds_nexus_v10`):** Statistically proving ($p < 0.05$) across 5 isolated experimental stages that unsupported claim rates can be reduced from 18.0% to 1.0% without expensive model fine-tuning.

#### 3. Summary Defense Statement for Viva Panel
> "ResearchNexus proves that combining hybrid Reciprocal Rank Fusion, cross-encoder reranking, and post-hoc NLI claim verification reduces scientific RAG citation hallucinations to 1.0% with 99.2% citation precision, offering an auditable, reproducible framework for scientific literature synthesis."
