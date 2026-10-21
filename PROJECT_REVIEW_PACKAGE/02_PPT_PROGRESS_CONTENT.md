# ResearchNexus AI - 5-6 Week Progress Presentation Content

## Slide 1: Title
**Title:** ResearchNexus AI: An Explainable Research Assistant Using Hybrid Retrieval, XAI and Enhanced RAG
**Content:**
*   **Project:** ResearchNexus AI
*   **Focus:** Explainable Research Assistant & Evaluation Console
*   **Core Technologies:** Hybrid Retrieval, eXplainable AI (XAI), Enhanced RAG, Baseline Locking, Ablation Engine
*   **Date:** September 2026
*   **Team/Presenter:** ResearchNexus AI Development Team

**Visual/Diagram Recommendation:** Clean, professional title layout with the project logo and simple abstract tech background.
**Speaker Notes:** Welcome everyone. Today, I'll be sharing our progress on ResearchNexus AI over the past 5 to 6 weeks. Our goal is to present an explainable research assistant that leverages hybrid retrieval, XAI, enhanced RAG, and a publication-ready evaluation console.

---

## Slide 2: Problem & Motivation
**Title:** The Research Challenge
**Content:**
*   Information overload in academic literature
*   Limitations of traditional search (e.g., Google Scholar): lack of transparency and deep synthesis
*   Shortcomings of standard RAG: hallucinations, unverified claims, opaque retrieval
*   The Scientific Credibility Gap: unvalidated AI tools reporting fabricated precision numbers
*   Need for verifiable, transparent, grounded research assistance with strict evaluation standards

**Visual/Diagram Recommendation:** Split graphic contrasting a frustrated researcher overwhelmed by papers vs. a structured, transparent AI pipeline with an evaluation console.
**Speaker Notes:** Researchers today face massive information overload. Traditional tools like Google Scholar lack deep synthesis, while standard RAG systems suffer from hallucinations. Furthermore, many AI systems publish unverified metrics. ResearchNexus AI addresses these challenges by providing transparency, verifiable grounded evidence, and strict publication-grade evaluation controls.

---

## Slide 3: System Architecture
**Title:** System Architecture
**Content:**
*   **Frontend:** React 19, Vite, Tailwind, Evaluation Console UI
*   **Backend API:** FastAPI with Evaluation Router
*   **Storage & DB:** PostgreSQL (Relational + Evaluation DB), ChromaDB (Isolated User Collections)
*   **AI/LLM:** Gemini Flash, BAAI/bge-base-en-v1.5 (768d), BAAI/bge-reranker-base
*   **Core Flow:** Frontend → API → Retrieval Engine → Enhanced RAG → XAI → Evaluation Console → LLM → Storage

**Visual/Diagram Recommendation:** Layered architecture diagram showing the flow from the React Frontend through the FastAPI backend to the DBs, LLM integration, and Evaluation Service.
**Speaker Notes:** Our tech stack is built for speed, transparency, and scientific defensibility. We use React 19 and FastAPI, backed by PostgreSQL and ChromaDB for high-performance vector storage with user-isolated collections. The architecture now incorporates a dedicated Evaluation Console service.

---

## Slide 4: Research Explorer
**Title:** Research Explorer
**Content:**
*   Unified interface for deep literature search
*   Real-time polling for asynchronous search task completion
*   Simultaneous local and online result aggregation
*   Integrated search history tracking with soft-delete semantics

**Visual/Diagram Recommendation:** Screenshot or mockup of the Research Explorer UI highlighting the search bar, real-time polling indicator, and mixed local/online results.
**Speaker Notes:** The Research Explorer acts as the central hub for literature search. We've implemented real-time polling for smooth asynchronous tasks. It seamlessly aggregates results from both our local datasets and 5 online connectors, maintaining full search history with soft-delete tracking.

---

## Slide 5: Local Retrieval Pipeline
**Title:** Local Retrieval Pipeline
**Content:**
*   **Dataset:** 706 verified papers across 3 domains
*   **Vector DB:** ChromaDB backfilled with 26,179 verified embeddings
*   **Pipeline Stages:**
    *   PostgreSQL metadata filtering
    *   BM25 keyword search
    *   Dense vector search
    *   Reciprocal Rank Fusion (RRF, k=60)
    *   Filtering & Diversification
    *   BGE Cross-Encoder Reranking

**Visual/Diagram Recommendation:** Flowchart detailing the stages of the local retrieval pipeline, incorporating the 706 papers and 26K embeddings statistics.
**Speaker Notes:** Our local pipeline is highly optimized, operating on a dataset of 706 papers and over 26,000 verified embeddings. It uses a robust multi-stage approach, combining PostgreSQL metadata filtering, BM25, dense search, and BGE reranking to surface the most relevant documents.

---

## Slide 6: Hybrid Retrieval + RRF
**Title:** Hybrid Retrieval & Reciprocal Rank Fusion
**Content:**
*   **Fusion Strategy:** BM25 (keyword) + Dense (semantic) fused via RRF (k=60)
*   Addresses vocabulary mismatch and semantic gaps
*   **5 Live Online Connectors:**
    *   arXiv
    *   OpenAlex
    *   PMC (PubMed Central)
    *   AGRIS
    *   NASA ADS

**Visual/Diagram Recommendation:** Diagram showing two streams (BM25 and Dense) merging into an RRF block, alongside the 5 online API connector logos/names feeding into a unified results list.
**Speaker Notes:** To maximize retrieval quality, we fuse keyword-based BM25 and semantic dense search using Reciprocal Rank Fusion with a k-value of 60. Additionally, we integrate live data from five major academic connectors, including arXiv, OpenAlex, and PubMed Central.

---

## Slide 7: XAI Implementation
**Title:** Explainable AI (XAI) Implementation
**Content:**
*   10-stage local pipeline timeline
*   8-stage online pipeline timeline
*   Complete XAI trace visibility
*   "Why This Paper?" feature with provenance cells
*   Independent BGE rank display & search_id validation
*   37 rigorous XAI tests passed

**Visual/Diagram Recommendation:** UI snapshot of the 10-stage timeline UI showing the execution trace and the "Why This Paper?" popover.
**Speaker Notes:** Transparency is critical in research. Our XAI implementation exposes a 10-stage local timeline and an 8-stage online timeline. We ensure complete trace visibility, independent rank tracking, provenance cell verification, and 37 dedicated XAI validation tests passed.

---

## Slide 8: AI Assistant Workspace
**Title:** AI Assistant Workspace
**Content:**
*   5 distinct interaction modes (Research, Paper, Compare, Evidence, Upload)
*   Context Inspector for full transparency
*   Scope Engine for bounding queries
*   Context Snapshots (Immutable, SHA-256 hashed)
*   Isolated Chroma vector collections for uploaded document privacy (Phase 3.8)

**Visual/Diagram Recommendation:** Mockup of the workspace highlighting the context inspector, scope engine toggles, and snapshot hashing.
**Speaker Notes:** The AI Assistant Workspace gives users complete control over the AI's context. It features 5 interaction modes, a scope engine, and immutable context snapshots secured with SHA-256 hashing to ensure reproducibility and privacy.

---

## Slide 9: Enhanced RAG Pipeline
**Title:** Enhanced RAG Pipeline
**Content:**
*   **Eligibility Check:** Determine if query requires RAG
*   **Retrieval:** Fetch grounded context
*   **Deduplication:** Remove redundant evidence
*   **Context Assembly:** Build structured prompt
*   **Generation:** Initial LLM response
*   **Verification:** Automatic claim checking & citation repair

**Visual/Diagram Recommendation:** A linear block diagram or chevron list showing the 6 steps from Eligibility to Verification.
**Speaker Notes:** Our Enhanced RAG pipeline is far more rigorous than standard approaches. It moves from strict eligibility checks and deduplication to context assembly, followed by generation, automatic claim verification, and citation repair.

---

## Slide 10: Claim Verification & Citation Repair
**Title:** Automated Claim Verification
**Content:**
*   Extracts 6 different types of claims
*   Applies Stage A deterministic checks (metadata, dates)
*   Utilizes Stage B semantic LLM verification for complex claims
*   Outputs 5 distinct verification statuses
*   Features automatic conservative citation repair

**Visual/Diagram Recommendation:** Visual grid or table showing claim types on one side and the verification workflow (extraction, check, status, repair) on the other.
**Speaker Notes:** We automatically verify generated content by extracting six types of claims. We use deterministic checks for metadata and LLM-based semantic verification for complex statements. If citations are misaligned, the system executes conservative citation repair.

---

## Slide 11: Iterative Refinement
**Title:** Bounded Iterative Refinement
**Content:**
*   Generates initial answer & runs verification
*   Evaluates self-feedback on failures
*   Executes targeted secondary retrieval
*   Refines output and re-verifies
*   Maximum 2 cycles to prevent infinite loops
*   Anti-oscillation safeguards using feedback signatures

**Visual/Diagram Recommendation:** A cyclical loop diagram showing Answer → Verify → Feedback → Refine, with a prominent "Max 2 Cycles" stop condition.
**Speaker Notes:** When verification fails, the system enters an iterative refinement loop. It generates self-feedback and performs targeted retrieval to fix errors. To maintain efficiency and prevent infinite loops, we cap this process at two cycles with anti-oscillation safeguards.

---

## Slide 12: Phase 3.10 Evaluation & Publication Console
**Title:** Evaluation & Publication Console (Phase 3.10)
**Content:**
*   **Baseline Locking:** 8 locked baselines (`B0_LLM_ONLY` to `B7_ITERATIVE_RAG`)
*   **RRF Sensitivity:** Parameter sweeps over `k = [20, 40, 60, 100]`
*   **Ablation Study Matrix:** System minus individual components
*   **Blinded Human Evaluation:** Panel evaluating 7 rating dimensions
*   **Claim Audit System:** Full claim support audit
*   **One-Click Export:** Reproducibility package for journal submission
*   **Strict Policy:** Displays **NOT MEASURED** until benchmark execution

**Visual/Diagram Recommendation:** UI screenshot or diagram of the Evaluation Console showing baseline configurations, ablation matrix, and human eval panel.
**Speaker Notes:** Phase 3.10 introduces a full evaluation and publication console. It locks baseline definitions B0-B7, runs RRF sensitivity sweeps, generates ablation matrices, supports blinded human evaluation, and exports a complete reproducibility package. Unmeasured metrics strictly display as NOT MEASURED.

---

## Slide 13: Testing & Build Verification
**Title:** Testing & Build Verification
**Content:**
*   Clean backend & frontend builds (`npm run build` passes with 0 TS errors)
*   30 backend evaluation console unit tests passed (`test_evaluation_console.py`)
*   37 complete XAI tests passed
*   Validation of search_id continuity & BGE reranking correctness
*   Frontend validation scripts enforcing NOT MEASURED policy

**Visual/Diagram Recommendation:** A stylized dashboard or checklist showing green checkmarks for test suites, build status, and test passes.
**Speaker Notes:** Quality assurance has been a major focus. We have a clean build, 30 passed backend evaluation unit tests, 37 passed XAI tests, and automated frontend validation enforcing our publication rules.

---

## Slide 14: Current Completion %
**Title:** Project Status & Completion
**Content:**
*   **Overall Project Completion:** **82.5%**
*   **Data & Embedding:** 100%
*   **Retrieval & XAI Pipelines:** 95%
*   **Enhanced RAG & Claim Verification:** 90%
*   **Evaluation Console & Baselines:** 85%
*   **Testing Suite:** 75%
*   **Documentation & Reports:** 50%

**Visual/Diagram Recommendation:** A simplified weighted completion table or progress bar chart reflecting the 82.5% overall completion and individual module progress.
**Speaker Notes:** We are currently at 82.5% overall completion. The implementation of code, pipelines, XAI, and evaluation infrastructure is complete. Our next step is executing benchmark experiments on the evaluation console.

---

## Slide 15: Key Research Contributions
**Title:** Key Research Contributions
**Content:**
1.  Hybrid Local+Online research retrieval with RRF (k=60) & BGE reranking
2.  Retrieval-level XAI (10-stage local + 8-stage online transparency)
3.  Context-bound evidence-grounded Enhanced RAG with scope engine
4.  Deterministic & semantic claim verification with citation repair
5.  Bounded iterative refinement (max 2 cycles) with anti-oscillation
6.  Publication-ready Evaluation Console with baseline locking and **NOT MEASURED** enforcement

**Visual/Diagram Recommendation:** A numbered list with distinct icons for each contribution highlighting novelty compared to standard tools.
**Speaker Notes:** Our system introduces key contributions to explainable research tools: transparent 10-stage retrieval XAI, automated claim verification with repair, bounded iterative refinement, and a scientifically defensible evaluation console.

---

## Slide 16: Next Steps
**Title:** Next Steps & Future Work
**Content:**
*   Execute benchmark evaluation runs across multi-domain datasets
*   Populate evaluation metrics (Recall, Precision, Claim Support Rate)
*   Conduct blinded human evaluation studies
*   Finalize IEEE research paper manuscript
*   Backend deployment to Render

**Visual/Diagram Recommendation:** A timeline or roadmap graphic outlining the next steps to final review and paper submission.
**Speaker Notes:** Looking ahead, our immediate focus is executing benchmark runs on our new evaluation console to replace NOT MEASURED placeholders with empirical data, conducting human eval studies, and finalizing our IEEE manuscript.
