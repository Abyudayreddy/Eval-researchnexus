# SDC-II OFFICIAL REVIEW PARAMETERS — DEFENSE DOCUMENT
## Project: ResearchMind / ResearchNexus AI
**System Description:** Explainable AI-Powered Scientific Research Assistant & Research OS  
**Evaluation Target:** 50 Marks Total across 5 Official Review Parameters (10 Marks Each)  
**Corpus & Benchmark Base:** `ds_nexus_v10` (100 gold questions, 670 local papers / 14,850 semantic chunks)

---

# PARAMETER 1: BASE PAPER (10 MARKS)

### 1. Title & Authors
* **Base Paper Title:** *"OpenScholar: Synthesizing Scientific Literature with Open Datastores and Language Models"* (Asai et al., 2024).

### 2. Problem Addressed
* **Simple English:** General AI tools like ChatGPT invent fake paper titles or cite papers that don't support their claims.
* **Base Paper Reality:** `[Project Fact]` Addresses the challenge of multi-paper scientific literature synthesis—generating comprehensive, cited answers to complex scholarly questions using open-access academic datastores.

### 3. Existing Approach Before Base Paper
* **Simple English:** Search engines like Google Scholar or basic single-document PDF chatbots.
* **Technical Reality:** `[General Technical Explanation]` Direct LLM prompting (zero-shot/few-shot) or naive dense RAG over small text databases, yielding hallucination rates of 20–25%.

### 4. Proposed Methodology of Base Paper
* **Technical Setup:** Combines an open scientific datastore (OSDS) containing ~45 million open-access papers, dense vector retrieval using a transformer bi-encoder, cross-encoder reranking, and an open LLM (Llama-3/Mistral) fine-tuned for scientific synthesis.

### 5. Technologies & Algorithms Used in Base Paper
* **Technologies:** Python, PyTorch, LlamaIndex, Dense Vector Stores.
* **Algorithms:** Bi-Encoder Vector Retrieval, Cross-Encoder Reranking, Supervised Fine-Tuning (SFT).

### 6. Research Gap Identified
* **Gap:** Existing systems lacked open-access paper datastores, lacked open models optimized for multi-paper synthesis, and failed to systematically evaluate citation faithfulness.

### 7. Dataset Details & Input Details
* **Base Paper Datastore (OSDS):** ~45 million open-access scientific papers (up to 2024) parsed into text passages.
* **Base Paper Benchmark (ScholarQABench):** Evaluation benchmark created by domain experts to evaluate multi-paper scientific synthesis.
* **Input Details:** Natural language scientific research questions.

### 8. Key Results, Final Output & Findings
* **Results:** OpenScholar outperformed proprietary baselines (Perplexity, Consensus) in citation accuracy and factual correctness on ScholarQABench.

### 9. How ResearchNexus Extends / Differs from the Base Paper

| Parameter | Base Paper (OpenScholar) | Our Project (ResearchMind / ResearchNexus) |
| :--- | :--- | :--- |
| **Retrieval Strategy** | Dense Retrieval Only (Bi-Encoder) | **Hybrid Sparse-Dense Retrieval** (BM25 + ChromaDB fused via RRF $k=60$) |
| **Reranking Engine** | Cross-Encoder Reranker | **BGE Cross-Encoder Reranker** (`BAAI/bge-reranker-base`) |
| **Explainability (XAI)** | None (Black-box generation) | **Full XAI Trace Modal** (Exposes BM25, Vector distance, RRF scores, BGE rank shifts) |
| **Verification & Repair** | Passive citation generation | **Phase 3.4 Claim Verifier & Automated Citation Repair** (NLI Stage A/B checks) |
| **Iterative Refinement** | Static single-pass generation | **Phase 3.5 Iterative Refinement Engine** (Self-feedback loop, max 2 cycles) |
| **User Corpus Isolation** | Fixed datastore | **Personal Research Corpus** (Upload custom PDFs, chunk, embed, isolate by `user_id`) |
| **Evaluated Benchmark** | ScholarQABench (45M corpus) | **`ds_nexus_v10`** (100 gold queries, 670 papers, 15 frozen TEST split) |

---

# PARAMETER 2: PROJECT REQUIREMENTS (10 MARKS)

### 1. Abstract
ResearchNexus is an explainable, multi-stage scientific research assistant designed to eliminate citation hallucinations and context leakage. The system combines lexical BM25 search with ChromaDB dense vector embeddings (`bge-base-en-v1.5`) via Reciprocal Rank Fusion ($k=60$), refines results using `bge-reranker-base`, enforces Phase 3.3 Enhanced RAG context bounding on Gemini 2.5 Flash, and applies Phase 3.4 NLI Claim Verification to automatically repair invalid citations. Evaluated on the `ds_nexus_v10` benchmark, hybrid search achieved an MRR of 0.812 ($p=0.0002$), BGE reranking boosted MRR to 0.972 ($p=0.0381$), and claim verification reduced unsupported claims to 1.0% with 98.0%+ citation precision.

### 2. Primary Objective & Specific Objectives
* **Primary Objective:** Build an end-to-end scientific research assistant that guarantees citation precision $>95\%$ and eliminates unsupported claim hallucinations.
* **Specific Objectives:**
  1. Implement RRF hybrid search (BM25 + ChromaDB).
  2. Integrate BGE Cross-Encoder reranking.
  3. Enforce Phase 3.3 Enhanced RAG context bounding.
  4. Develop Phase 3.4 NLI Claim Verifier & Citation Repair.
  5. Provide an interactive Explainable AI trace view.

### 3. Core Features Inventory
1. **Research Explorer:** Domain-scoped multi-modal search interface.
2. **Hybrid Search Engine:** Lexical BM25 + ChromaDB vector search fused via RRF ($k=60$).
3. **XAI Trace Modal:** Exposes BM25 scores, vector distances, RRF ranks, and BGE rank deltas ($\Delta r$).
4. **AI Assistant:** Grounded chat synthesis with prompt scoping (`All Research`, `Selected Papers`, `Single Paper`).
5. **Enhanced RAG (Phase 3.3):** Context bounding prompts restricting LLMs strictly to retrieved context.
6. **Claim Verification (Phase 3.4):** Stage A regex parsing + Stage B Gemini NLI entailment checking + Citation Repair.
7. **Iterative Refinement (Phase 3.5):** Self-feedback gap evaluation loop (max 2 cycles).
8. **Multi-Paper Comparison Matrix:** 10-dimension tabular comparison of 2 to 5 papers.
9. **Literature Synthesis & Gaps:** Identifies Consensus, Contradictions (5 conflict types), and Research Gaps (10 gap classes).
10. **Personal Research Corpus:** Private user PDF uploading with PyMuPDF parsing and `user_id` context isolation.
11. **Research Sessions & Memory:** SQLite state persistence saving queries, chats, and evidence across reloads.
12. **Evaluation & Publication Consoles:** Automated benchmark execution and reproducibility package exporter.

### 4. Stakeholders
* Undergraduate students, postgraduate scholars, faculty members, domain scientists, and corporate R&D researchers.

### 5. Use Cases & User Journey
* **Use Case 1:** Rapid literature search across 670 local papers or 6 dynamic APIs.
* **Use Case 2:** Grounded research synthesis with 100% verifiable inline citations.
* **Use Case 3:** Auditing retrieval math via XAI traces.
* **Use Case 4:** Side-by-side paper comparison matrices.
* **User Journey Sequence:**
  $$\text{Query Input} \rightarrow \text{Research Explorer} \rightarrow \text{Hybrid Retrieval} \rightarrow \text{RRF \& BGE Rerank} \rightarrow \text{AI Assistant} \rightarrow \text{Claim Verification} \rightarrow \text{Citation Repair} \rightarrow \text{Final Output}$$

---

# PARAMETER 3: SYSTEM DESIGN (10 MARKS)

### 1. Technology Stack Table

| Layer | Technology | Purpose | Technical Role |
| :--- | :--- | :--- | :--- |
| **Frontend** | React 18, TypeScript 5, Vite 5, Tailwind CSS | UI Layout & State | SPA compiled in 13.04s; Zustand state management |
| **Backend** | FastAPI (Python 3.13) | REST API Framework | Asynchronous ASGI server with Pydantic validation |
| **Relational DB** | SQLite / PostgreSQL | Metadata & Sessions | Stores user accounts, paper DOIs, session logs, and test data |
| **Vector DB** | ChromaDB | Dense Vector Search | Stores 14,850 768-dim vectors using HNSW ANN indexing |
| **Parsing** | PyMuPDF (`fitz`), LlamaIndex | Document Processing | Layout-aware text extraction & 512/64 sliding window chunking |
| **Embeddings** | `BAAI/bge-base-en-v1.5` | Dense Vector Generator | 768-dimensional transformer bi-encoder embedding model |
| **Reranker** | `BAAI/bge-reranker-base` | Second-Stage Reranking | Transformer cross-encoder evaluating joint cross-attention |
| **LLM** | Gemini 2.5 Flash | Grounded RAG Synthesis | Generative LLM (`temp=0.0`) for synthesis and NLI checking |

---

### 2. Complete Architecture Diagram
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

---

### 3. Workflows

#### A. Retrieval Workflow
Query $\rightarrow$ BM25 + ChromaDB $\rightarrow$ RRF Score Aggregation ($S_{\text{RRF}} = \sum \frac{1}{60 + r}$) $\rightarrow$ Top 20 Candidates $\rightarrow$ BGE Cross-Encoder $\rightarrow$ Top 5 Snippets.

#### B. Verification Workflow
Answer Draft $\rightarrow$ Stage A Regex Claim Extraction $\rightarrow$ Stage B Gemini NLI Entailment Check (`ENTAILES`, `NEUTRAL`, `CONTRADICTS`) $\rightarrow$ Citation Repair (re-links invalid tags to entailing chunks) $\rightarrow$ Verified Output.

#### C. Domain Loading Workflow
User clicks domain (e.g., `Material Science`) $\rightarrow$ Domain shell renders immediately $\rightarrow$ Async API fetches paper metadata $\rightarrow$ Grid populates progressively.

---

### 4. Database & Class Domain Design

#### Dual Database Architecture
* **PostgreSQL / SQLite:** Relational metadata (papers, authors, DOIs, user profiles, session histories, evaluation run logs).
* **ChromaDB:** High-dimensional vector store holding 14,850 768-dim float vectors with HNSW indexing.

#### Core Entity Domain Classes
* `ResearchContext`: Active search state, domain tags, retrieved chunk IDs.
* `ResearchPaper`: Paper ID, title, authors, DOI, publication year, abstract, PDF URL.
* `EvidenceBlock`: Chunk ID, section name, page number, text content, 768-dim vector array.
* `ResearchAnswer`: Answer text, citation array, verification result, refinement cycle count.
* `Claim`: Sentence text, cited chunk IDs, NLI entailment status.
* `Citation`: Citation key (`[1]`), chunk ID, paper ID, status (`VALID`, `INVALID`, `REPAIRED`).

---

# PARAMETER 4: IMPLEMENTATION (10 MARKS)

### 1. Implemented Modules & Current Progress %
`[Project Fact]` Core system architecture and benchmark evaluation suite are **100% implemented, tested, and verified** (112/112 backend pytests passing). Overall platform roadmap completion is estimated at **92%**.

| Module | Implemented? | Backend | Frontend | Testing | Status | Known Limitation |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Research Explorer** | YES | YES | YES | YES | **100% COMPLETE** | External API rate limits during burst traffic. |
| **Hybrid Search (RRF)** | YES | YES | YES | YES | **100% COMPLETE** | Static $k=60$ parameter across all query lengths. |
| **BGE Reranker** | YES | YES | YES | YES | **100% COMPLETE** | Adds $+42.5$ ms P50 latency overhead. |
| **Explainable AI (XAI)** | YES | YES | YES | YES | **100% COMPLETE** | Trace JSON payload size (~15KB). |
| **AI Assistant (RAG)** | YES | YES | YES | YES | **100% COMPLETE** | Requires active Gemini API key. |
| **Enhanced RAG (B5E)** | YES | YES | YES | YES | **100% COMPLETE** | Context bounds return Insufficient Evidence on unindexed terms. |
| **Claim Verification** | YES | YES | YES | YES | **100% COMPLETE** | Adds $+340$ ms verification latency. |
| **Iterative Refinement** | YES | YES | YES | YES | **100% COMPLETE** | Adds $+753.3$ ms P50 overhead (+150.6%). |
| **Paper Comparison** | YES | YES | YES | YES | **100% COMPLETE** | Limited to max 5 papers for UI layout clarity. |
| **Literature Synthesis** | YES | YES | YES | YES | **100% COMPLETE** | Gap depth depends on chunk context coverage. |
| **Personal Corpus** | YES | YES | YES | YES | **100% COMPLETE** | Requires text-based PDFs (no OCR layer). |
| **Research Sessions** | YES | YES | YES | YES | **100% COMPLETE** | Dev setup stores sessions in local SQLite DB. |
| **Evaluation Console** | YES | YES | YES | YES | **100% COMPLETE** | Benchmark runner takes ~45 seconds for 15 TEST items. |
| **Publication Console** | YES | YES | YES | YES | **100% COMPLETE** | Manual blind human rating marked `NOT MEASURED`. |

---

### 2. Technologies, Frameworks, APIs & Models Used
* **Languages & Frameworks:** Python 3.13, FastAPI, React 18, TypeScript 5, Vite 5, Tailwind CSS, Zustand, Pydantic, SQLAlchemy.
* **AI Models:** `BAAI/bge-base-en-v1.5` (Embedding), `BAAI/bge-reranker-base` (Cross-Encoder), Gemini 2.5 Flash (LLM).
* **External Academic APIs:** 6 APIs: arXiv, PubMed Central (PMC), AGRIS, NASA ADS, OpenAlex, Crossref.

---

### 3. Dataset & Preprocessing Details
* **Local Pre-Built Knowledge Base:** 670 papers (14,850 semantic chunks).
* **Local Curated Domains:** Artificial Intelligence (300), Environmental Science (190), Interdisciplinary Research (180), Material Science (Active).
* **Preprocessing Pipeline:** PDF $\rightarrow$ PyMuPDF text extraction $\rightarrow$ header/footer cleaning $\rightarrow$ section splitting $\rightarrow$ LlamaIndex sliding-window chunking (512 tokens, 64 overlap) $\rightarrow$ BGE 768-dim embeddings $\rightarrow$ ChromaDB storage.

---

### 4. Working Demo Script Sequence
1. **Open Landing Page:** Show dashboard and domain stats.
2. **Launch Search in Explorer:** Select domain `Material Science`, type query: *"Compare Retrieval-Augmented Generation models in medical diagnosis"*, watch live pipeline execution stepper.
3. **Inspect XAI Trace:** Click "Inspect XAI Trace" on result card; show BM25 score, vector distance, RRF rank, and BGE rank shift ($\Delta r$).
4. **Synthesize in Assistant:** Select top 3 papers, click "Synthesize in Assistant", view grounded answer with inline citations `[1]`, `[2]`.
5. **Verify Claims:** Click "Verify Claims", view claim verification drawer showing `VERIFIED` and `REPAIRED` badges.
6. **Compare Papers:** Open Literature Review workspace, select 3 papers, generate 10-dimension comparison matrix.
7. **Resume Session:** Open Research Sessions sidebar, click previous session to demonstrate SQLite state persistence across reloads.

---

### 5. Benchmark Empirical Results (`ds_nexus_v10` Frozen TEST Split $N=15$)

`[Project Fact]` Official measured evaluation results from benchmark reports:

| Stage | Experiment ID & Configuration | Primary Metric | Baseline | Experimental | Delta ($\Delta$) | Statistical Result | Latency (P50) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **E01** | **Retrieval Baseline** (B1 Dense vs B3 Hybrid) | MRR | 0.650 | **0.812** | **$+0.162$** | Wilcoxon $p = 0.0002$ | 18.2 ms |
| **E02** | **BGE Reranking** (B3 Hybrid vs B4 BGE) | MRR (TEST)<br>Hit@1 | 0.900<br>0.800 | **0.972**<br>**0.933** | **$+0.072$**<br>**$+0.133$** | Wilcoxon $p = 0.0381$<br>0 rank regressions | 60.9 ms<br>($+42.5$ms) |
| **E03** | **Enhanced RAG** (B5R Conv vs B5E Enhanced) | Citation Prec. | 0.733 | **0.947** | **$+0.214$** | Wilcoxon $p = 0.0120$ | 433.6 ms |
| **E04** | **Claim Verification** (B6A Unverified vs B6V Verified) | Citation Prec.<br>Unsupp. Rate | 0.750<br>0.160 | **0.980**<br>**0.010** | **$+0.230$**<br>**$-0.150$** | Wilcoxon $p = 0.0080$<br>15 Citations Repaired | $+340.0$ ms overhead |
| **E05** | **Iterative Refinement** (B7A Single vs B7R Refined) | Citation Prec.<br>Unsupp. Rate | 0.965<br>0.030 | **0.992**<br>**0.010** | **$+0.027$**<br>**$-0.020$** | Wilcoxon $p = 0.0035$<br>Max 2 Cycle Cap | 1253.3 ms<br>($+753$ms) |

---

### 6. Challenges & Next Steps
* **Challenge 1:** Bi-encoder keyword distractor bias $\rightarrow$ Resolved via RRF ($k=60$) hybrid search and BGE cross-encoder reranking.
* **Challenge 2:** Parametric memory hallucination $\rightarrow$ Resolved via Phase 3.3 Enhanced RAG context bounding.
* **Challenge 3:** Invalid citation tag association $\rightarrow$ Resolved via Phase 3.4 NLI Claim Verification and Citation Repair algorithms.
* **Next Steps:** Integrate OCR parsing layer for scanned PDFs; scale local corpus to 5,000+ papers; expand benchmark TEST split to $N=100$.

---

# PARAMETER 5: PAPER PUBLICATION PROGRESS (10 MARKS)

### 1. Target Conference / Journal
* **Tier 1 System/Demo Venues:** ACL / EMNLP System Demonstrations, CIKM Applied Research Track, ECIR Industry/Demo Track, IEEE Access.

### 2. Finalized Paper Title
* **Official Working Title:** *"ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis"* (Candidate title under finalization).

### 3. Literature Survey Status
* **Status:** **COMPLETED**. 28 formal academic references analyzed across RAG (Lewis et al.), BM25 (Robertson et al.), RRF (Cormack et al.), Cross-Encoders (BAAI), and NLI Verification (Asai et al.).

### 4. Research Gap & Contribution

#### Research Gap
Existing scientific search tools rely on unverified vector search or employ generative LLMs without post-hoc claim verification, resulting in hallucinated citation rates between 15% and 25%. Current self-reflective RAG methods require expensive model fine-tuning.

#### Research Contribution
1. **Phase 3.4 Claim Verification & Citation Repair Algorithm:** Automated 2-stage verification workflow (Stage A regex + Stage B NLI entailment classification) that dynamically detects invalid citations and repairs them by re-linking claims to entailing corpus chunks.
2. **Phase 3.3 Enhanced RAG Context Bounding Framework:** Deterministic prompt boundary design eliminating parametric memory context leakage.
3. **Empirical Benchmarking (`ds_nexus_v10`):** Statistically proving ($p < 0.05$) across 5 isolated experimental stages that unsupported claim rates can be reduced from 18.0% to 1.0% without model fine-tuning.

---

### 5. Methodology & Architecture Completed
* **Status:** **COMPLETED**. End-to-end 5-stage isolated pipeline implemented, tested, and locked.

### 6. Results and Analysis Status
* **Status:** **COMPLETED**. Full empirical metric tables, Wilcoxon $p$-values ($p<0.05$), and 95% Bootstrap CIs compiled for E01 through E05.

### 7. Paper Writing Status — Sections Completed / Pending

| Section | Writing Status | Evidence / Source Material |
| :--- | :---: | :--- |
| **Abstract** | **COMPLETED** | `FINAL_PUBLICATION_READINESS_REPORT.md` |
| **Introduction** | **COMPLETED** | Manuscript draft in IEEEtran & LNCS formats |
| **Literature Review** | **COMPLETED** | 28 reference citations in IEEE/LNCS drafts |
| **Problem Statement & Gap** | **COMPLETED** | Section 21 of audit report |
| **Methodology & Equations** | **COMPLETED** | Formulas for RRF ($k=60$), BGE, Stage A/B NLI |
| **System Architecture** | **COMPLETED** | Figure 1 System Block Diagram |
| **Implementation Details** | **COMPLETED** | Lock report Section 2 |
| **Experiments & Results** | **COMPLETED** | Benchmark E01–E05 metric tables |
| **Discussion & Limitations** | **COMPLETED** | Latency trade-off analysis ($+753$ms vs 99.2% precision) |
| **Conclusion & Future Work** | **COMPLETED** | Summary & multi-document graph summarization roadmap |
| **References** | **COMPLETED** | 28 formatted academic references |

---

### 8. Publication Status
* **Honest Status Tag:** **READY FOR INTERNAL REVIEW** (Draft near complete; audit score 143/170 - 84.1% SUBMISSION READY; ready for team/advisor sign-off prior to formal submission).
* *Note:* We explicitly state **"Ready for Internal Review"** to maintain honest reporting integrity (we do NOT falsely claim "Submitted" or "Under Review").

---

### SUMMARY REVISION CHEAT SHEET FOR THE 5 PARAMETERS

```
========================================================================================
                  SDC-II REVIEW PARAMETERS — 50 MARKS VIVA CHEAT SHEET
========================================================================================
[PARAMETER 1: BASE PAPER (10 Marks)]
  • Base Paper : OpenScholar (Asai et al., 2024) [Multi-Paper Scientific RAG]
  • Extension  : Added Hybrid RRF (k=60), BGE Reranker, XAI Traces, NLI Citation Repair

[PARAMETER 2: PROJECT REQUIREMENTS (10 Marks)]
  • Objective  : Grounded scientific QA with >95% Citation Precision & <3% Unsupported Rate
  • Features   : Explorer, Hybrid Search, XAI Modal, AI Assistant, Verifier, Matrix, Personal Corpus

[PARAMETER 3: SYSTEM DESIGN (10 Marks)]
  • Tech Stack : React 18, TypeScript 5, Vite 5, FastAPI, SQLite/PostgreSQL, ChromaDB
  • Models     : BGE-v1.5 (Embedding), BGE-Reranker-Base (Cross-Encoder), Gemini 2.5 Flash (LLM)
  • Workflow   : Query -> BM25 + Vector -> RRF k=60 -> BGE Rerank -> RAG -> NLI Verifier -> Output

[PARAMETER 4: IMPLEMENTATION (10 Marks)]
  • Completion : 100% Core System Functional (112/112 Pytests Pass) | 92% Overall Platform
  • Dataset    : ds_nexus_v10 Benchmark (100 Queries) | 670 Local Papers (14,850 Chunks)
  • Metrics    : E01 MRR 0.812 | E02 MRR 0.972 | E03 Prec 94.7% | E04 Prec 98.0% | E05 Prec 99.2%

[PARAMETER 5: PAPER PUBLICATION (10 Marks)]
  • Status     : READY FOR INTERNAL REVIEW (Audit Score: 143/170 - 84.1% SUBMISSION READY)
  • Target     : ACL/EMNLP Demos, CIKM Applied Track, IEEE Access | Title Under Finalization
  • Contribution: NLI Stage A/B Citation Repair Algorithm + RRF Hybrid RAG Architecture
========================================================================================
```
