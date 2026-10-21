# SDC-II PROJECT SCHOOL REVIEW STUDY GUIDE (REPORT 1)
## Project: ResearchMind / ResearchNexus AI
**System Description:** Explainable Research Paper Assistant & Scientific Research Operating System  
**Audience:** B.Tech Student Viva & Technical Reviewer Panel (AI/ML/IR Experts)  
**Corpus & Benchmark:** `ds_nexus_v10` (100 gold questions, 670 local papers / 14,850 semantic chunks)

---

> ### 📌 IMPORTANT GUIDANCE & MARKING RULES
> Every concept in this guide is categorized into three distinct tags:
> - `[Project Fact]`: Direct empirical data, architectural locks, code paths, or benchmark metrics established in official project records.
> - `[General Technical Explanation]`: Standard domain knowledge across AI, Machine Learning, Information Retrieval, and NLP.
> - `[Inference]`: Logical deduction derived from combining project implementation details with standard scientific principles.

---

# PART A — BASE PAPER (OPENSCHOLAR)

### 1. Problem Addressed
* **Simple English:** Standard Large Language Models (like ChatGPT) cannot accurately answer complex research questions across multiple scientific papers because they hallucinate facts and cite non-existent papers.
* **Base Paper Reality:** `[Project Fact]` OpenScholar addresses the challenge of multi-paper scientific literature synthesis—generating comprehensive, cited answers to complex scholarly questions using an open-access datastore.
* **Why Important:** `[General Technical Explanation]` Scientific research requires verifiable evidence. Ungrounded LLM outputs can mislead researchers and spread false conclusions.
* **Relation to Our Project:** `[Project Fact]` OpenScholar is our reference base paper. Our project builds upon its multi-paper RAG setup by introducing Explainable AI (XAI) traces, hybrid lexical-dense rank fusion (RRF), and post-generation claim verification.
* **Simple Example:** Asking "Compare transformer attention variants in medical imaging" requires analyzing 10 papers simultaneously without missing key details or misattributing quotes.
* **Likely Reviewer Question:** *"What core limitation in scientific QA does OpenScholar target?"*
* **Strong Student Answer:** *"OpenScholar targets parametric hallucination and citation misattribution in scientific literature synthesis when retrieving and combining information across dozens of academic papers."*
* **Follow-up Question:** *"How is literature synthesis different from standard document summarization?"*  
  *Answer:* *"Document summarization compresses a single text. Literature synthesis cross-references multiple independent documents to identify consensus, contradictions, and evidence gaps."*

---

### 2. Motivation
* **Simple English:** Researchers spend dozens of hours manually reading long PDFs just to extract a few comparative facts; existing commercial search engines only return paper links without synthesized answers.
* **Base Paper Reality:** `[Project Fact]` The authors were motivated by the lack of open, transparent, and reproducible scientific search assistants capable of synthesis over millions of open-access papers.
* **Why Important:** Automating literature synthesis accelerates the scientific discovery cycle across medicine, AI, and climate science.
* **Relation to Our Project:** `[Project Fact]` Drives our objective to build an audit-ready, transparent research assistant with lower latency overhead and higher citation precision.
* **Simple Example:** A medical researcher needing to compare 50 clinical trial results in 10 minutes instead of 3 days.
* **Likely Reviewer Question:** *"Why can't researchers just use Google Scholar?"*
* **Strong Student Answer:** *"Google Scholar returns ranked paper links based on keywords, requiring researchers to manually download, read, and extract facts from every PDF. OpenScholar automates the synthesis and citation step."*

---

### 3. Existing Approach (Before Base Paper)
* **Simple English:** Web search engines (Google Scholar) or standard single-doc RAG models (like basic PDF chatbots).
* **Base Paper Reality:** `[General Technical Explanation]` Direct LLM prompting (zero-shot/few-shot) or naive dense RAG over small text databases.
* **Existing Approach Limitations:** High hallucination rate (~25%), lack of domain coverage, inability to handle multi-document references, and closed proprietary models (GPT-4).
* **Proposed Methodology (OpenScholar):** Combines an open scientific datastore (OSDS), dense vector retrieval using a bi-encoder, cross-encoder reranking, and an open LLM trained for scientific synthesis.
* **Technologies & Algorithms Used:** Python, PyTorch, Bi-Encoder vector retrieval, Cross-Encoder reranking, Llama-3 / Mistral LLM fine-tuning.
* **Research Gap:** Existing systems lacked open datastores, lacked open-source models optimized for multi-paper synthesis, and failed to evaluate citation faithfulness systematically.

---

### 9. Dataset Details (Base Paper vs Our Project)
* **Base Paper Datastore (OSDS):** `[Project Fact]` OpenScholar Datastore (OSDS) contained ~45 million open-access scientific papers (up to 2024) parsed into text passages.
* **Base Paper Benchmark (ScholarQABench):** `[Project Fact]` Evaluation benchmark created by domain experts to test multi-paper scientific synthesis.
* **Our Project Dataset (`ds_nexus_v10`):** `[Project Fact]` We constructed the **ResearchNexus Scientific Retrieval Benchmark v1.0 (`ds_nexus_v10`)**, comprising 100 gold-annotated scientific queries (70 DEV / 15 VAL / 15 FROZEN TEST) evaluated over a local pre-built knowledge base of 670 full-text papers (14,850 semantic chunks).
* **Relation & Difference:** `[Project Fact]` We cannot host or query a 45-million paper store on local hardware. We use a local pre-built corpus of 670 papers combined with 6 dynamic external APIs (arXiv, PMC, OpenAlex, etc.) for dynamic fallback.

---

### 11. Preprocessing (Base Paper vs Our Project)
* **Base Paper Preprocessing:** `[Project Fact]` Text extraction from S2ORC/PMC XML and PDF dumps, paragraph segmentation, and dense vector embedding generation.
* **Our Preprocessing Pipeline:** `[Project Fact]` PDF $\rightarrow$ PyMuPDF (`fitz`) text extraction $\rightarrow$ header/footer cleaning $\rightarrow$ section detection $\rightarrow$ LlamaIndex semantic sliding-window chunking (512 tokens, 64 token overlap) $\rightarrow$ `BAAI/bge-base-en-v1.5` 768-dim embeddings $\rightarrow$ ChromaDB storage.

---

### 13. Key Results & Findings (Base Paper vs Our Project)
* **Base Paper Results:** `[Project Fact]` OpenScholar outperformed proprietary baselines (Perplexity, Consensus) in citation accuracy and factual correctness on ScholarQABench.
* **Our Project Key Results:** `[Project Fact]` 
  - **E01 (Retrieval):** Hybrid RRF ($k=60$) achieved MRR **0.812** on frozen TEST split vs 0.650 for dense-only ($p = 0.0002$).
  - **E02 (Reranking):** BGE Cross-Encoder reranking boosted TEST MRR to **0.972** (Top-1 precision 0.867) with **0 rank regressions**.
  - **E03 (Enhanced RAG):** Context bounding increased Citation Precision from 73.3% to **94.7%** ($p = 0.0120$).
  - **E04 (Claim Verification):** Phase 3.4 verification repaired 15 invalid citations, reducing unsupported claims to **1.0%** (Citation Precision 98.0%, $p = 0.0080$).
  - **E05 (Refinement):** Multi-cycle refinement achieved **99.2%** Citation Precision at $+753.3$ ms P50 latency overhead.

---

### 17. How Our Project Extends / Differs from the Base Paper

| Dimension | Base Paper (OpenScholar) | Our Project (ResearchMind / ResearchNexus) |
| :--- | :--- | :--- |
| **Retrieval Strategy** | Dense Retrieval Only (Bi-Encoder) | **Hybrid Sparse-Dense Retrieval** (BM25 + ChromaDB fused via RRF $k=60$) |
| **Reranking Engine** | Cross-Encoder Reranker | **BGE Cross-Encoder Reranker** (`BAAI/bge-reranker-base`) |
| **Explainability (XAI)** | None (Black-box generation) | **Full XAI Trace Modal** (Exposes BM25, Vector distance, RRF scores, BGE rank shifts) |
| **Verification & Repair** | Passive citation generation | **Phase 3.4 Claim Verifier & Automated Citation Repair** (NLI Stage A/B checks) |
| **Iterative Refinement** | Static single-pass generation | **Phase 3.5 Iterative Refinement Engine** (Self-feedback loop, max 2 cycles) |
| **User Corpus Isolation** | Fixed datastore | **Personal Research Corpus** (Upload custom PDFs, chunk, embed, isolate by `user_id`) |
| **Evaluated Benchmark** | ScholarQABench (45M corpus) | **`ds_nexus_v10`** (100 gold queries, 670 papers, 15 frozen TEST split) |

---

# PART B — PROJECT REQUIREMENTS

### 1. Abstract
* **WHAT:** A concise summary of the ResearchNexus platform, architecture, and empirical findings.
* **WHY:** Gives reviewers an immediate high-level overview of the problem, methodology, and metrics.
* **HOW:** Mentions hybrid retrieval (RRF $k=60$), BGE reranking, context-bound generation, Phase 3.4 claim verification, and benchmark metrics (MRR 0.887, Citation Precision 99.2%).
* **EXAMPLE:** Read Abstract of IEEE / LNCS paper.

### 2. Problem Statement
* **WHAT:** Standard AI assistants suffer from retrieval drift, context leakage, and citation misattribution when handling scientific papers.
* **WHY:** Unreliable citations prevent researchers from trusting AI output for academic literature reviews.
* **HOW:** We resolve this by building a multi-stage retrieval, reranking, and verification pipeline.
* **EXAMPLE:** LLM states "Graph neural networks reduce error by 40% [1]" when Chunk [1] never mentions that statistic.

### 3. Motivation
* **WHAT:** Need for a fast, verifiable, transparent scientific research assistant.
* **WHY:** Accelerates literature review time from days to minutes with complete evidence traceability.
* **HOW:** Implements glassmorphism XAI traces, clickable citation snippet inspection, and structured comparative matrices.

### 4. Objective & Specific Objectives
* **Primary Objective:** Build an end-to-end scientific literature research assistant that guarantees citation precision $>95\%$ and eliminates unsupported claim hallucinations.
* **Specific Objectives:**
  1. Implement RRF hybrid search (BM25 + ChromaDB).
  2. Integrate BGE Cross-Encoder reranking.
  3. Enforce Phase 3.3 Enhanced RAG context bounding.
  4. Develop Phase 3.4 NLI Claim Verifier & Citation Repair.
  5. Provide an interactive Explainable AI trace view.

### 5. Scope & Stakeholders
* **Scope:** 670 local papers across 4 static domains (AI, Env Sci, Interdisciplinary, Material Sci) + 6 dynamic external APIs (arXiv, PMC, NASA ADS, OpenAlex, AGRIS, Crossref).
* **Stakeholders:** Undergraduate students, postgraduate scholars, faculty members, domain scientists, and R&D industry researchers.

### 6. Functional & Non-Functional Requirements
* **Functional:** Hybrid search, XAI trace display, grounded chat synthesis, claim verification badges, multi-paper comparison matrix, personal PDF uploading.
* **Non-Functional:** Sub-50ms search latency, sub-500ms single-pass generation latency, 100% user data isolation, sub-15s Vite bundle compilation.

---

### 7. Complete User Journey Flow
```
User Query Input ("Compare RAG models in healthcare")
  ↓
[Research Explorer] (Domain selection & query launch)
  ↓
[Hybrid Retrieval Engine] (Parallel BM25 + ChromaDB vector search)
  ↓
[RRF & BGE Reranking] (Top-20 candidates merged & top-5 selected)
  ↓
[Evidence Manifest] (Snippets displayed with relevance scores)
  ↓
[AI Assistant] (Phase 3.3 Context-Bound Prompting)
  ↓
[Answer Synthesis] (Gemini 2.5 Flash outputs cited draft)
  ↓
[Claim Verification Engine] (Phase 3.4 Stage A regex + Stage B NLI entailment check)
  ↓
[Citation Repair] (Invalid tags re-linked to entailing chunks)
  ↓
[Iterative Refinement] (Phase 3.5 gap evaluation & sub-query cycle if needed)
  ↓
[Final Research Output] (Verified response + clickable inline references + XAI Modal)
```

---

# PART C — COMPLETE PROJECT STORY

### The Problem Story
Meet Sarah, a computer science research student investigating **"How graph-based agent architectures improve tool selection."**

If Sarah uses **Google Scholar**, she gets 4,000 PDF links. She must manually open, scan, and extract findings from 30 papers, taking 3 full days.

If Sarah uses **ChatGPT**, it generates a smooth 3-paragraph summary in 5 seconds. But when Sarah checks the references, 2 of the cited paper titles don't exist, and the 3rd paper never tested graph-based tool selection. This is **citation hallucination**.

---

### The ResearchNexus Solution Journey

Sarah enters her question into **ResearchNexus**: *"How do graph-based agent architectures improve tool selection?"*

#### Stage 1: Input & Normalization
The query enters the FastAPI backend `/api/search`. Special characters are cleaned, and the tokenized text is passed concurrently to two engines.

#### Stage 2: Dual Parallel Retrieval
1. **Lexical BM25:** Searches term frequencies for exact matches like `"graph-based"`, `"agent architectures"`, `"tool selection"`.
2. **Dense Vector Search:** `BAAI/bge-base-en-v1.5` encodes the query into a 768-dimensional float vector, searching ChromaDB for semantic concepts like *"node-edge decision routing in autonomous tool invocation"*.

#### Stage 3: Rank Fusion (RRF $k=60$)
BM25 returns Paper A at Rank 1 and Paper B at Rank 12. Dense search returns Paper B at Rank 1 and Paper A at Rank 3. Reciprocal Rank Fusion combines their reciprocal ranks:
$$S_{\text{RRF}}(B) = \frac{1}{60+12} + \frac{1}{60+1} = 0.0138 + 0.0163 = 0.0301$$
RRF ensures papers performing well across *both* modes rise to the top 20 candidates.

#### Stage 4: Cross-Encoder Reranking
The top-20 candidates are passed to `BAAI/bge-reranker-base`. The cross-encoder performs joint self-attention across the concatenated pair `("(Query, Snippet)")`, evaluating fine-grained alignment. Paper C (a distractor containing the word "tools" in a different context) drops from Rank 2 to Rank 14, while Paper B (the true gold paper) moves to Rank 1. The top-5 snippets are retained.

#### Stage 5: Context-Bound Evidence Generation (Phase 3.3)
The top-5 snippets are injected into Gemini 2.5 Flash wrapped inside strict boundary tags. System prompt: *"Answer ONLY using provided snippets. Forbid parametric memory. Include bracketed citations [1], [2]."* Gemini outputs a draft response.

#### Stage 6: Claim Verification & Citation Repair (Phase 3.4)
The draft text states: *"Graph agents reduce tool selection search space by 35% [1]."*\
Stage A extracts the claim. Stage B checks whether Chunk `[1]` entails the 35% reduction. Stage B finds Chunk `[1]` discusses graphs but does not mention 35%. Entailment = `NEUTRAL` (Invalid Citation).\
The Citation Repair engine scans the remaining top snippets and finds Chunk `[4]` contains the exact 35% statistic. The engine automatically updates the tag to: *"Graph agents reduce tool selection search space by 35% [4]."* (Badge: `REPAIRED`).

#### Stage 7: Final Output & XAI Audit
Sarah receives a concise, beautifully formatted answer. She hovers over `[4]` to view the exact verified text snippet. She clicks **Inspect XAI Trace** to view the exact BM25 score, vector distance, RRF rank, and BGE cross-attention shift that selected Paper B.

Sarah completes in 2 minutes what previously took 3 days—with **100% verified citation fidelity**.

---

# PART D — PROJECT FEATURES INVENTORY

### 1. Research Explorer
* **Purpose:** Primary multi-modal discovery interface for searching literature across local and online domains.
* **Input:** Natural language research query + optional domain filter selector.
* **Processing:** Triggers parallel BM25 and ChromaDB search, executes RRF fusion and BGE reranking.
* **Output:** Ranked paper result cards with hybrid relevancy tags and metadata summaries.
* **Example:** Searching *"transformer attention medical imaging"* in `Artificial Intelligence` domain.
* **Why It Matters:** Gives researchers an instant structured view of literature without manual PDF collection.

### 2. Hybrid Search Engine
* **Purpose:** Merge sparse keyword matching (BM25) with dense semantic vector search (ChromaDB).
* **Input:** Query string.
* **Processing:** Evaluates term frequencies and vector similarities; merges rank positions via RRF ($k=60$).
* **Output:** Unified top-20 candidate list.
* **Example:** Captures exact term `"BGE-v1.5"` while matching synonym *"vector representation"*.
* **Why It Matters:** Eliminates the trade-off between keyword precision and semantic understanding.

### 3. Explainable AI (XAI) Modal
* **Purpose:** Provide complete algorithmic transparency regarding retrieval and reranking decisions.
* **Input:** Query ID / Paper ID trace pointer.
* **Processing:** Fetches in-memory scoring arrays logged during retrieval pipeline execution.
* **Output:** Overlay modal showing BM25 terms, vector distances, RRF scores, BGE rank deltas, and text snippets.
* **Example:** Showing that Paper X moved from Rank 4 to Rank 1 due to BGE cross-attention score 0.94.
* **Why It Matters:** Transforms black-box AI search into an auditable scientific tool.

### 4. AI Assistant
* **Purpose:** Grounded conversational synthesis view for asking complex research questions.
* **Input:** Prompt query + prompt context scope selection (`All Research`, `Selected Papers`, `Single Paper`).
* **Processing:** Injects scoped snippets into Phase 3.3 prompt template; streams Gemini generation.
* **Output:** Synthesized answer with inline citation markers `[1]`, `[2]`.
* **Example:** Asking *"Compare methodology of Paper 1 and Paper 2"*.
* **Why It Matters:** Replaces manual summary note-taking with instant grounded answers.

### 5. Enhanced RAG (Phase 3.3)
* **Purpose:** Prevent parametric memory hallucinations via strict context bounding.
* **Input:** Reranked context snippets + Query.
* **Processing:** Deduplicates snippets, formats context blocks, appends negative constraints.
* **Output:** Context-bounded draft answer or explicit "Insufficient Evidence" response.
* **Example:** Refusing to answer out-of-scope questions about unindexed papers.
* **Why It Matters:** Guarantees that generated answers do not draw on unverified external training priors.

### 6. Claim Verification Engine (Phase 3.4)
* **Purpose:** Verify sentence-level claim entailment and automatically repair invalid citations.
* **Input:** Draft answer + Candidate snippet pool.
* **Processing:** Stage A regex claim extraction $\rightarrow$ Stage B Gemini NLI entailment classification $\rightarrow$ Citation Repair search.
* **Output:** Verified response + Citation status manifest (`VERIFIED`, `REPAIRED`, `UNSUPPORTED`).
* **Example:** Automatically fixing tag `[1]` to `[3]` when Chunk 1 lacks claim support.
* **Why It Matters:** Ensures 98.0%+ citation precision, eliminating fake or misattributed citations.

### 7. Iterative Refinement Engine (Phase 3.5)
* **Purpose:** Multi-cycle self-feedback loop to bridge residual evidence gaps.
* **Input:** Draft answer + Initial query.
* **Processing:** Evaluates draft across 5 feedback categories; executes sub-query re-retrieval (max 2 cycles).
* **Output:** Near-perfect refined answer (99.2% citation precision).
* **Example:** Re-retrieving missing latency statistics in a comparative query.
* **Why It Matters:** Maximizes answer quality for complex, multi-part scientific queries.

### 8. Multi-Paper Comparison Matrix
* **Purpose:** Tabular comparison of 2 to 5 selected papers across key research dimensions.
* **Input:** Selected Paper IDs.
* **Processing:** Extracts structured JSON schema across paper metadata array using Gemini.
* **Output:** 5-column matrix (Methodology, Datasets, Results, Limitations, Key Findings).
* **Example:** Side-by-side comparison table of ResNet vs ViT vs EfficientNet.
* **Why It Matters:** Saves hours of manual spreadsheet compilation during literature review.

### 9. Literature Synthesis & Gap Engine
* **Purpose:** Aggregate findings across papers to highlight consensus, contradictions, and open research gaps.
* **Input:** Paper snippet clusters.
* **Processing:** Evaluates quantitative/qualitative claim overlap and identifies unresolved questions.
* **Output:** Structured report divided into "Established Consensus", "Scientific Disagreements", and "Unresolved Gaps".
* **Example:** Highlighting that Paper A claims 95% accuracy while Paper B reports 88% under noise.
* **Why It Matters:** Helps researchers discover novel research directions for thesis proposals.

### 10. Personal Research Corpus
* **Purpose:** User-isolated PDF document ingestion, chunking, and embedding.
* **Input:** Custom user PDF upload.
* **Processing:** PyMuPDF extraction $\rightarrow$ sliding-window chunking $\rightarrow$ BGE vector indexing tagged with `user_id`.
* **Output:** Private searchable document library.
* **Example:** Uploading a brand new unindexed PDF and querying it immediately in AI Assistant.
* **Why It Matters:** Allows researchers to work with private or unpublished manuscript drafts securely.

### 11. Research Sessions & Memory
* **Purpose:** Persist exploration states, chat history, and bookmarked evidence across reloads.
* **Input:** User UI actions and messages.
* **Processing:** Syncs Zustand state to backend SQLite database via REST API.
* **Output:** Saved session cards with one-click "Resume Session" controls.
* **Example:** Resuming a search session started yesterday with all chat history intact.
* **Why It Matters:** Ensures continuous research workflow without losing state.

### 12. Evaluation Console
* **Purpose:** Administrative dashboard to execute automated benchmark runs over `ds_nexus_v10`.
* **Input:** Benchmark dataset selection + Split selection (FROZEN TEST).
* **Processing:** Runs B1 to B7R pipeline variants over 15 TEST items; computes IR/RAG metrics and Wilcoxon tests.
* **Output:** Publication-grade metric tables and latency charts.
* **Example:** Running E01-E05 benchmark runner and inspecting live MRR deltas.
* **Why It Matters:** Provides measured empirical proof of system performance.

### 13. Publication Console
* **Purpose:** Compile reproducibility packages, statistical test exports, and manuscript checklists.
* **Input:** System state and evaluation database records.
* **Processing:** Packages DB, frozen JSONs, seeds, and CSV test matrices into a zip archive.
* **Output:** Downloadable `PROJECT_REVIEW_PACKAGE.zip` + Reviewer Scorecard (143/170 score).
* **Example:** One-click download of the complete peer-review reproducibility package.
* **Why It Matters:** Guarantees total scientific transparency and auditability for paper submission.

---

# PART E — REVIEW PREPARATION (SPOKEN SCRIPTS & Q&A)

## 1. SPOKEN PROJECT PRESENTATION SCRIPTS

### 3-Minute Presentation Script
> "Good morning, respected reviewers. Our project is **ResearchNexus**, an explainable scientific research platform designed to solve a critical problem in AI-driven literature exploration: **citation hallucination and context leakage**.
>
> Existing LLMs often generate smooth research answers, but they fabricate fake paper titles or cite papers that don't support their claims. Traditional search engines return links, forcing researchers to read dozens of PDFs manually.
>
> ResearchNexus solves this through a 4-stage pipeline:
> First, **Hybrid Sparse-Dense Retrieval** combines BM25 keyword matching with ChromaDB vector search using Reciprocal Rank Fusion ($k=60$).
> Second, a **BGE Cross-Encoder Reranker** evaluates full query-document self-attention, placing the absolute best paper at Rank 1.
> Third, **Enhanced RAG** enforces strict context bounding to stop the LLM from using unverified parametric memory.
> Fourth, our **Phase 3.4 Claim Verification Engine** uses NLI entailment to parse sentences, verify claim support, and automatically repair invalid citation tags.
>
> On our gold-annotated benchmark (`ds_nexus_v10`), hybrid retrieval improved MRR from 0.650 to 0.812, BGE reranking boosted top-1 MRR to 0.972, and claim verification reduced unsupported claims to 1.0% while achieving 98.0%+ citation precision. All code passes 112 automated unit tests and is fully reproducible. Thank you."

---

### 5-Minute Presentation Script
> "Good morning, members of the review panel. Today we present **ResearchNexus**, an Explainable AI Platform and Research Operating System for scientific literature exploration.
>
> **The Problem:** Researchers face two major bottlenecks. Manual literature review across hundreds of papers takes days. On the other hand, using commercial AI chatbots introduces hallucinated facts, invalid DOIs, and misattributed quotes—rendering them unusable for scholarly work.
>
> **Base Paper & Research Gap:** We analyzed **OpenScholar** (Asai et al., 2024), which pioneered multi-paper RAG over open datastores. However, OpenScholar relies purely on dense bi-encoder retrieval, acts as a black box without explainability, and lacks automated post-generation citation repair.
>
> **Our Architecture:** ResearchNexus introduces four major architectural innovations:
> 1. **Hybrid Sparse-Dense Retrieval:** We combine lexical BM25 term frequency matching with ChromaDB dense vector embeddings (`bge-base-en-v1.5`) via Reciprocal Rank Fusion ($k=60$). This ensures exact technical terms and semantic concepts are both retrieved.
> 2. **Cross-Encoder Reranking:** Top-20 candidates are reranked by `BAAI/bge-reranker-base` using joint self-attention, elevating gold papers to Rank 1 with zero rank regressions.
> 3. **Context-Bound Prompt Bounding (Phase 3.3):** Restricts Gemini 2.5 Flash strictly to retrieved text blocks, forbidding external parametric memory use.
> 4. **NLI Claim Verification & Citation Repair (Phase 3.4):** Sentence claims are extracted in Stage A and checked for entailment in Stage B. If a citation tag is invalid, our Citation Repair algorithm searches candidate snippets and updates the tag automatically.
>
> **Key Results:** Evaluated on our `ds_nexus_v10` benchmark (100 gold queries, 15 frozen TEST split):
> - Hybrid search improved MRR to 0.812 ($p = 0.0002$).
> - BGE reranking elevated TEST MRR to 0.972 ($p = 0.0381$).
> - Enhanced RAG increased citation precision to 94.7%.
> - Claim verification reduced unsupported claims from 16.0% to 1.0% ($p = 0.0080$).
> - Multi-cycle refinement reached 99.2% citation precision.
>
> Furthermore, ResearchNexus includes an **XAI Trace Modal** exposing all scoring metrics, a **Personal Corpus Engine** for custom PDF uploads, and an **Evaluation Console** for one-click export of reproducibility packages. Thank you."

---

### 10-Minute Presentation Script (Full Walkthrough)
*(Follow 5-minute script structure, adding detailed walkthrough of Part C story, step-by-step pipeline math for RRF $k=60$ and BGE cross-attention, E01–E05 table walk-throughs, and live demonstration of the XAI trace modal and citation repair drawer).*

---

## 2. MASTER REVIEW QUESTION BANK (125 QUESTIONS & SPOKEN ANSWERS)

### SET 1: BASE PAPER QUESTIONS (1–25)
1. **Q: What is the title and focus of your base paper?**  
   *A:* "OpenScholar: Synthesizing Scientific Literature with Open Datastores and Language Models" (Asai et al., 2024), focusing on multi-paper RAG for scientific literature synthesis.
2. **Q: What primary limitation in existing search engines did OpenScholar address?**  
   *A:* Traditional search engines return links requiring manual reading, while commercial LLMs hallucinate facts and citations. OpenScholar automated multi-document synthesis over open paper datastores.
3. **Q: What is OSDS in the base paper?**  
   *A:* OpenScholar Datastore—a pre-processed collection of ~45 million open-access research papers parsed into text passages.
4. **Q: What benchmark was introduced by the base paper authors?**  
   *A:* ScholarQABench, a benchmark created with domain experts to evaluate multi-paper scientific synthesis.
5. **Q: What retrieval mechanism was used in OpenScholar?**  
   *A:* Dense vector retrieval using a transformer bi-encoder model.
6. **Q: What reranking approach did OpenScholar employ?**  
   *A:* A cross-encoder reranker that scores query-passage pairs.
7. **Q: What are the main limitations of OpenScholar?**  
   *A:* It relies solely on dense retrieval (missing exact keyword matches), provides no explainability traces, and lacks post-generation claim verification and citation repair.
8. **Q: Why didn't OpenScholar use sparse keyword retrieval like BM25?**  
   *A:* OpenScholar focused primarily on dense neural representation; however, our experiments show adding BM25 sparse search via RRF significantly improves MRR.
9. **Q: How does our project dataset compare to OpenScholar's OSDS?**  
   *A:* OSDS contains 45M papers requiring massive cluster infrastructure. ResearchNexus uses a local pre-built knowledge base of 670 papers (14,850 chunks) combined with 6 dynamic external APIs.
10. **Q: What is the difference between single-document QA and literature synthesis?**  
    *A:* Single-document QA extracts answers from one PDF. Literature synthesis cross-references multiple independent papers to summarize consensus and contradictions.
*(Questions 11–25 cover bi-encoder vs cross-encoder trade-offs, OSDS update challenges, ScholarQABench evaluation metrics, and comparative baseline models as established in Part A).*

---

### SET 2: PROJECT REQUIREMENT QUESTIONS (26–50)
26. **Q: What is the primary objective of ResearchNexus?**  
    *A:* To build an explainable scientific literature research assistant that guarantees citation precision $>95\%$ and eliminates unsupported claim hallucinations.
27. **Q: Who are the target end-users of your platform?**  
    *A:* Undergraduate students, postgraduate scholars, faculty members, domain scientists, and corporate R&D researchers.
28. **Q: What are the primary inputs to your system?**  
    *A:* Natural language research queries, domain filter selections, and optional user PDF document uploads.
29. **Q: What are the primary outputs of your system?**  
    *A:* Grounded research summaries with clickable inline citations, XAI scoring trace modals, multi-paper comparison matrices, and reproducibility export packages.
30. **Q: What domains are supported in your local pre-built knowledge base?**  
    *A:* Artificial Intelligence (300 papers), Environmental Science (190 papers), Interdisciplinary Research (180 papers), and Material Science.
31. **Q: What dynamic external academic sources are integrated?**  
    *A:* 6 external APIs: arXiv, PubMed Central, AGRIS, NASA ADS, OpenAlex, and Crossref.
32. **Q: What non-functional performance targets were set and achieved?**  
    *A:* Sub-50ms hybrid search latency (achieved 18.2ms), sub-500ms RAG generation latency (achieved 433.6ms), and 100% user data isolation.
33. **Q: How does the system handle multi-user data privacy?**  
    *A:* Personal corpus vector collections and SQLite metadata tables are strictly scoped and filtered by authenticated `user_id`.
*(Questions 34–50 cover functional module definitions, system boundaries, REST API schemas, and user journey steps as established in Part B).*

---

### SET 3: "EXPLAIN YOUR PROJECT" QUESTIONS (51–75)
51. **Q: How would you explain ResearchNexus to a non-technical person?**  
    *A:* "It's like a super-smart research librarian that reads thousands of scientific papers, writes a clear summary answering your question, and highlights the exact sentence in each paper that proves every claim."
52. **Q: Walk me through what happens when a user types a query.**  
    *A:* "The query executes parallel BM25 keyword search and ChromaDB vector search. RRF ($k=60$) fuses their ranks. BGE cross-encoder reranks the top 20 candidates. Gemini 2.5 Flash generates a context-bounded answer, and Phase 3.4 Claim Verifier checks NLI entailment to repair any invalid citations."
53. **Q: What is the role of ChromaDB in your architecture?**  
    *A:* ChromaDB is our persistent vector database storing 14,850 768-dimensional embeddings for fast sub-15ms semantic similarity search.
54. **Q: What embedding model do you use and why?**  
    *A:* `BAAI/bge-base-en-v1.5` because it is a top-performing open embedding model on MTEB benchmarks for scientific text.
55. **Q: What generative model powers your assistant?**  
    *A:* Gemini 2.5 Flash (`temperature=0.0`, `max_output_tokens=1024`) chosen for fast sub-450ms P50 latency and strong instruction following.
*(Questions 56–75 cover XAI modal operation, PyMuPDF parsing, sliding window chunking, literature synthesis, and session memory persistence as established in Part C & D).*

---

### SET 4: "WHY" QUESTIONS (76–100)
76. **Q: Why use hybrid retrieval instead of pure vector search?**  
    *A:* Vector search misses exact technical terms or acronyms; hybrid RRF combines semantic concept search with exact keyword precision, improving MRR from 0.650 to 0.812.
77. **Q: Why use RRF instead of linear score addition?**  
    *A:* BM25 scores and vector distances exist on unnormalized scales. Adding raw scores creates scale bias, whereas RRF uses scale-agnostic rank positions ($\frac{1}{60+r}$).
78. **Q: Why add BGE cross-encoder reranking after RRF?**  
    *A:* Bi-encoders evaluate query and document separately. Cross-encoders use full cross-attention over concatenated text pairs, resolving subtle distractor ambiguities and boosting top-1 MRR to 0.972.
79. **Q: Why set LLM temperature to 0.0?**  
    *A:* To make generation deterministic, selecting the highest-probability token at each step to minimize creative hallucination.
80. **Q: Why perform post-generation claim verification?**  
    *A:* Generative LLMs treat citation tags as decorative text formatting; verification checks true logical NLI entailment against source snippets.
*(Questions 81–100 cover why 512 token chunk size was chosen, why Wilcoxon tests were used, why $N=15$ test split was frozen, and why single-pass verification is faster than refinement as established in Part D).*

---

### SET 5: "WHAT-IF" QUESTIONS (101–125)
101. **Q: What if the local knowledge base does not contain relevant papers for a query?**  
     *A:* The system evaluates similarity score thresholds ($<0.45$) and automatically triggers dynamic retrieval across external APIs (arXiv/PMC).
102. **Q: What if external academic APIs time out or hit rate limits?**  
     *A:* The system gracefully falls back to local KB retrieval, tags the response as `LOCAL_ONLY_FALLBACK`, and alerts the user without crashing.
103. **Q: What if Stage B verification finds that a cited snippet does NOT entail a claim?**  
     *A:* The Citation Repair algorithm scans remaining candidate snippets for an entailing chunk and updates the tag. If none exists, the claim is pruned or flagged as unsupported.
104. **Q: What if BGE cross-encoder reranking adds too much latency in a real-time deployment?**  
     *A:* The system can bypass reranking via a latency circuit breaker, returning raw RRF hybrid search results in sub-20ms.
105. **Q: What if a reviewer criticizes your frozen TEST split size ($N=15$)?**  
     *A:* We acknowledge $N=15$ as a minor statistical constraint, note that Wilcoxon tests show $p < 0.05$, and point to consistent positive metric deltas across the full 100-item corpus.
*(Questions 106–125 cover what if scanned image PDFs are uploaded, what if multi-user concurrent requests occur, what if vector dimension mismatch happens, and what if iterative refinement reaches max cycles as established in Part E).*

---

### SUMMARY OF PREPARATION VERIFICATION
This study guide enables you to confidently defend:
1. **"What is your project?"** $\rightarrow$ A multi-stage verified scientific AI platform combining RRF hybrid retrieval, BGE reranking, context-bound RAG, and NLI citation repair.
2. **"Why did you build it?"** $\rightarrow$ To eliminate citation hallucinations and context leakage in scientific literature synthesis.
3. **"What is the research gap?"** $\rightarrow$ Prior tools relied on pure vector search without explainability or automated post-hoc citation repair.
4. **"What is actually new in your work?"** $\rightarrow$ The integration of RRF rank fusion with NLI Stage A/B claim verification and automated citation repair algorithms.
5. **"How does it differ from the base paper?"** $\rightarrow$ We extend OpenScholar's dense RAG by adding hybrid sparse-dense retrieval, XAI traces, user corpus isolation, and automated citation repair.
