import os

path = r'SDC Review 1/SDC_II_COMPREHENSIVE_MASTER_PROJECT_REPORT.md'

chapters_4_to_5 = """
---

# CHAPTER 4: SYSTEM DESIGN & ARCHITECTURAL FOUNDATIONS (10 MARKS)

### 4.1 End-to-End System Architecture
ResearchMind is constructed upon a high-performance, decoupled, multi-tiered micro-service architecture that enforces complete separation of concerns between user interaction, computational orchestration, dense/sparse indexing, and persistent relational state.

```
+=======================================================================================================+
|                                  RESEARCHMIND / RESEARCHNEXUS AI                                      |
|                                    END-TO-END SYSTEM ARCHITECTURE                                     |
+=======================================================================================================+
|  [PRESENTATION LAYER - CLIENT]                                                                        |
|  * React 18 SPA + TypeScript + Vite + Tailwind CSS + Lucide Icons                                     |
|  * 14 Specialized Workspaces (Explorer, Matrix, Heatmap, Synthesizer, Vault, LaTeX Export)             |
|  * Real-Time Server-Sent Events (SSE) Streaming & Attention Heatmap Canvas Renderer                   |
+-------------------------------------------------------------------------------------------------------+
                                                   | HTTP / REST & WebSockets (Port 8000)
                                                   v
+-------------------------------------------------------------------------------------------------------+
|  [API & ORCHESTRATION LAYER - FASTAPI]                                                                |
|  * Asynchronous Request Router & Pydantic V2 Request/Response Validation Handlers                     |
|  * Pipeline Orchestrator (Phase 1 Retrieval -> Phase 2 Rerank -> Phase 3 Generation & Verify)         |
|  * Token Budget Manager & CORS / Multi-Tenant Session Security Guards                                 |
+-------------------------------------------------------------------------------------------------------+
        |                                          |                                        |
        v                                          v                                        v
+-----------------------+      +-----------------------------------+      +-----------------------------+
| [DOCUMENT PIPELINE]   |      | [HYBRID RETRIEVAL & RERANK ENGINE]|      | [EPISTEMIC STATE & STORAGE] |
| * PyMuPDF (fitz):     |      | * Sparse Engine: Okapi BM25       |      | * PostgreSQL: Sessions,     |
|   Layout extraction,  |      |   (Inverted Token Index)          |      |   Users, Claims, Traces,    |
|   header/noise strip  |      | * Dense Engine: ChromaDB          |      |   Synthesis Documents       |
| * LlamaIndex:         |      |   (BAAI/bge-base-en-v1.5)         |      | * ChromaDB: 14,850 vectors  |
|   Semantic & sliding  | ---> | * Fusion: Reciprocal Rank Fusion  | <--> |   768-dim L2 collection     |
|   window chunking     |      |   RRF(d) = sum(1 / (k + rank))    |      | * In-Memory LRU Cache:      |
|   (512 tok / 64 ovlp) |      | * Cross-Encoder: BAAI/bge-rerank  |      |   Pre-computed embeddings   |
+-----------------------+      +-----------------------------------+      +-----------------------------+
                                                   |
                                                   | Top-K Reranked Context Passages
                                                   v
+-------------------------------------------------------------------------------------------------------+
|  [COGNITIVE GENERATION & VERIFICATION SUBSYSTEM]                                                      |
|  * Generative Synthesis: Google Gemini 2.5 Flash (Strict Grounding System Prompt)                     |
|  * Syntactic Proposition Extractor: Atomic Claim Decomposition Algorithm                             |
|  * Phase 3.4 Verification Engine: Natural Language Inference (NLI) [Entailment/Neutral/Contradict]     |
|  * Autonomous Claim Repair Loop: Regenerates / excises ungrounded claims if NLI Confidence < 0.85    |
|  * Explainable AI (XAI) Engine: Computes token-level attribution weights & highlights source chunks   |
+=======================================================================================================+
```

### 4.2 Comprehensive Tech Stack Justification

| Technology / Tool | Exact Version / Spec | Role in ResearchMind | Justification over Alternatives |
| :--- | :--- | :--- | :--- |
| **React 18** | v18.3.1 | Presentation Layer SPA | Provides Concurrent Mode and efficient DOM diffing necessary for rendering live streaming LLM responses and complex interactive comparison matrices without UI stutter. |
| **TypeScript** | v5.5.3 | Static Type Safety | Eliminates runtime type errors across complex scientific JSON schemas, API contracts, and multi-document synthesis payloads. |
| **Tailwind CSS** | v3.4.1 | UI Styling & Design System | Utility-first CSS enables responsive, accessible, dark/light theme switching with zero runtime CSS bundle overhead. |
| **FastAPI** | v0.111.0 | Asynchronous REST Backend | Asynchronous ASGI framework providing native Python coroutines (`async`/`await`), automated OpenAPI documentation, and high-performance throughput matching NodeJS/Go. |
| **PyMuPDF (fitz)** | v1.24.4 | PDF Document Ingestion | 10x-20x faster extraction speed than PyPDF2 or PDFMiner; extracts bounding box coordinates, font sizes, and layout structures to reliably strip running headers/footers. |
| **LlamaIndex** | v0.10.35 | Semantic Document Chunking | Provides hierarchical and semantic sentence splitters that preserve scientific paragraph cohesion and chemical formula boundaries. |
| **ChromaDB** | v0.5.0 | Embedded Vector Database | Lightweight, persistent, zero-dependency Apache 2.0 vector store with native HNSW indexing, ideal for sub-second L2/cosine similarity queries over 14,850 vectors. |
| **Rank-BM25** | v0.2.2 | Sparse Inverted Index | Implements exact Okapi BM25 keyword matching; essential for retrieving exact chemical stoichiometric formulas (e.g., $\\text{Li}_{10}\\text{GeP}_2\\text{S}_{12}$) where dense embeddings fail. |
| **BAAI/bge-base-en-v1.5** | HuggingFace / Transformers | 768-dim Dense Bi-Encoder | Top-ranked open-weights embedding model on MTEB (Massive Text Embedding Benchmark); captures deep conceptual and semantic relationships in scientific prose. |
| **BAAI/bge-reranker-base** | HuggingFace / Cross-Encoder | Deep Cross-Attention Reranker | Full query-document cross-attention scoring that eliminates false positives from dense search by computing token-level interactions simultaneously. |
| **Google Gemini 2.5 Flash** | Google Generative AI API | Primary Generative Synthesizer | State-of-the-art reasoning-to-latency ratio, 1M+ token context window support, and high instruction-following fidelity for grounded scientific generation. |
| **PostgreSQL** | v15+ (SQLAlchemy ORM) | Relational Storage & State | ACID-compliant transactional persistence for user accounts, research sessions, atomic claim verification logs, and LaTeX export histories. |

### 4.3 Detailed Architectural Subsystems
The system consists of five decoupled operational engines:
1. **Document Ingestion Engine:** Converts raw multi-column academic PDFs into cleaned, structured text chunks enriched with document metadata (Title, Authors, DOI, Year, Section Heading).
2. **Hybrid Retrieval & RRF Fusion Engine:** Simultaneously dispatches queries to BM25 and ChromaDB, collects ranked lists, and mathematically fuses them via Reciprocal Rank Fusion.
3. **Cross-Encoder Reranking Engine:** Performs intensive cross-attention over the top-$K$ fused candidate passages to compute non-linear relevance probabilities.
4. **Contextual Synthesis & XAI Engine:** Injects top reranked chunks into Gemini 2.5 Flash with strict grounding constraints and generates token-level attribution weights for the visual heatmap.
5. **Phase 3.4 Verification & Auto-Repair Engine:** Deconstructs the generated text into atomic propositions, executes NLI evaluation against source chunks, and triggers surgical text repair for unsupported claims.

### 4.4 Data Pipeline Architecture: Ingestion, Extraction, and Chunking
The document preparation pipeline executes in four deterministic stages:
```
Raw Academic PDF (e.g., Nature Materials, Advanced Energy Materials)
    |
    v
[Stage 1: PyMuPDF Layout Analysis]
    * Extracts raw text blocks along with font size, weight, and bounding boxes.
    * Identifies and excises running headers, footers, page numbers, and copyright notices.
    * Flags section header boundaries based on font-size thresholds.
    |
    v
[Stage 2: Section-Aware Segmentation]
    * Groups extracted text under normalized section headings (Abstract, Intro, Methods, Results, Discussion).
    * Isolates non-body content such as References, Acknowledgments, and Author Affiliations.
    |
    v
[Stage 3: LlamaIndex Semantic Chunking]
    * Chunks text into sliding windows of 512 tokens with a 64-token stride.
    * Respects sentence boundaries; avoids truncating formulas or sentences mid-clause.
    * Prepends document metadata (e.g., "[Paper: Chen et al., 2023 | Section: Results]") to each chunk.
    |
    v
[Stage 4: Dual Index Population]
    * Inverted Index: Tokenizes chunk text and updates Okapi BM25 frequency statistics.
    * Vector Index: Passes chunk text through BAAI/bge-base-en-v1.5 to compute 768-dim embeddings -> ChromaDB.
```

### 4.5 Retrieval Architecture: Sparse, Dense, RRF, and Cross-Encoder
Scientific information retrieval requires balancing **lexical precision** (for exact acronyms, chemical formulas, and quantitative constants) and **semantic recall** (for synonymous terminology and abstract conceptual queries). ResearchMind implements a three-tier retrieval funnel:

```
User Query: "What is the ionic conductivity of Li10GeP2S12 solid electrolytes?"
    |
    +---------------------------------------+
    |                                       |
    v                                       v
[Sparse Branch: Okapi BM25]             [Dense Branch: BGE-base-en-v1.5]
* Analyzes exact term frequencies       * Embeds query into 768-dim space
* Matches "Li10GeP2S12" precisely       * Matches semantic context "solid electrolytes"
* Outputs Top-30 ranked chunks          * Outputs Top-30 ranked chunks
    |                                       |
    +-------------------+-------------------+
                        |
                        v
        [Stage 2: Reciprocal Rank Fusion (k=60)]
        * Fuses ranks: RRF(d) = sum(1 / (60 + rank_i(d)))
        * Produces unified Top-20 fused candidates
                        |
                        v
        [Stage 3: BGE-Reranker-Base Cross-Encoder]
        * Concatenates [CLS] + Query + [SEP] + Passage + [EOS]
        * Computes 12-layer all-to-all cross-attention
        * Selects Top-5 highest scoring passages for LLM Context
```

### 4.6 Verification & Self-Repair Architecture (Phase 3.4)
The Phase 3.4 Verification Subsystem serves as the automated scientific peer reviewer, ensuring zero ungrounded assertions reach the researcher.

```
Synthesized Output from LLM
    |
    v
[Step 1: Atomic Claim Decomposition]
    * Splits multi-sentence paragraphs into discrete factual propositions.
    * e.g., Claim C1: "Li10GeP2S12 exhibits an ionic conductivity of 1.2 x 10^-2 S/cm at 25 C."
    * e.g., Claim C2: "It degrades rapidly when exposed to dry argon atmosphere."
    |
    v
[Step 2: Citation Mapping & NLI Classification]
    * Maps Claim C1 to cited Source Passage P1.
    * Runs NLI Evaluation Prompt: P(Entailed | P1, C1).
    * C1 -> Class: ENTAILED (Confidence: 0.96) -> ACCEPTED.
    * C2 -> Class: CONTRADICTED (Source states it is stable in dry argon) -> FLAGGED.
    |
    v
[Step 3: Automated Surgical Repair Loop]
    * Passes flagged claim C2 and passage P1 to Repair Prompt.
    * Surgical instruction: "Rewrite or remove Claim C2 to strictly reflect Passage P1."
    * Repaired output: "It demonstrates superior electrochemical stability in dry argon atmosphere."
    |
    v
Final Verified, Attributed Scientific Response Output
```

### 4.7 Database Design: Relational Schema and Vector Schema

#### 4.7.1 PostgreSQL Relational Database Schema
The relational database tracks sessions, papers, claims, verification traces, and user interactions.

```sql
-- Core Papers Table
CREATE TABLE papers (
    paper_id VARCHAR(64) PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT[] NOT NULL,
    abstract TEXT,
    publication_year INT,
    doi VARCHAR(128) UNIQUE,
    journal_venue VARCHAR(255),
    total_chunks INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Passage Chunks Metadata Table
CREATE TABLE passage_chunks (
    chunk_id VARCHAR(64) PRIMARY KEY,
    paper_id VARCHAR(64) REFERENCES papers(paper_id) ON DELETE CASCADE,
    section_name VARCHAR(128) NOT NULL,
    chunk_index INT NOT NULL,
    token_count INT NOT NULL,
    raw_content TEXT NOT NULL,
    cleaned_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User Research Sessions Table
CREATE TABLE research_sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    session_title VARCHAR(255) NOT NULL,
    domain VARCHAR(64) DEFAULT 'Material Science',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Queries & Synthesis Audit Table
CREATE TABLE synthesis_traces (
    trace_id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) REFERENCES research_sessions(session_id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    retrieved_chunk_ids TEXT[] NOT NULL,
    raw_response TEXT NOT NULL,
    verified_response TEXT NOT NULL,
    citation_precision FLOAT NOT NULL,
    unsupported_rate FLOAT NOT NULL,
    execution_time_ms INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Granular Claim Verification Table
CREATE TABLE claim_verifications (
    claim_id VARCHAR(64) PRIMARY KEY,
    trace_id VARCHAR(64) REFERENCES synthesis_traces(trace_id) ON DELETE CASCADE,
    atomic_claim_text TEXT NOT NULL,
    cited_chunk_id VARCHAR(64) REFERENCES passage_chunks(chunk_id),
    nli_verdict VARCHAR(32) NOT NULL, -- 'ENTAILED', 'NEUTRAL', 'CONTRADICTED'
    nli_confidence FLOAT NOT NULL,
    repair_action VARCHAR(32),        -- 'ACCEPTED', 'REWRITTEN', 'REMOVED'
    repaired_claim_text TEXT
);
```

#### 4.7.2 ChromaDB Vector Database Schema
- **Collection Name:** `material_science_corpus_v1`
- **Embedding Dimension:** 768 dimensions (Float32 vectors generated by `bge-base-en-v1.5`)
- **Distance Metric:** Cosine Distance / L2 Euclidean Space
- **Metadata Document Payload:**
  ```json
  {
    "paper_id": "paper_matsic_2023_0412",
    "chunk_id": "paper_matsic_2023_0412_chunk_014",
    "section": "3.2 Electrochemical Characterization",
    "title": "High Ionic Conductivity in Sulfide-Based Solid Electrolytes",
    "authors": "Zhang et al.",
    "year": 2023,
    "token_length": 487
  }
  ```

### 4.8 Object-Oriented Class Design and Component Hierarchy
The backend application follows a clean domain-driven architectural pattern structured into distinct layers:

```
[API Layer: Controllers]
  -> SearchController: Handles /api/search/hybrid, /api/search/rerank
  -> SynthesisController: Handles /api/rag/synthesize, /api/rag/stream
  -> VerificationController: Handles /api/verify/claims, /api/verify/repair
  -> MatrixController: Handles /api/matrix/compare, /api/export/latex
        |
        v
[Service Layer: Business Logic Orchestrators]
  -> DocumentIngestionService (PyMuPDF parser, structural sanitizer)
  -> HybridRetrievalService (BM25 sparse indexer + ChromaDB dense search)
  -> RankFusionService (Reciprocal Rank Fusion k=60 algorithm)
  -> CrossEncoderService (bge-reranker inference manager)
  -> SynthesisService (Gemini 2.5 Flash prompt builder & response parser)
  -> ClaimVerificationService (NLI decomposition, verification, and repair)
  -> XAIExplanationService (Token alignment, attention weight matrix)
        |
        v
[Repository / Data Access Layer]
  -> PostgreSQLRepository (SQLAlchemy models for papers, sessions, claims)
  -> ChromaVectorRepository (ChromaDB collection querying and CRUD)
  -> BM25InvertedIndexRepository (In-memory token frequency lookup tables)
```

### 4.9 Sequence Diagrams and Workflow Interactions
The sequence of synchronous and asynchronous events during a complete research query execution:

```
User (Browser)       FastAPI Router       HybridService     CrossEncoder     Gemini 2.5     VerifyService
     |                     |                    |                |               |                |
     |--- 1. POST Query -->|                    |                |               |                |
     |    (JSON payload)   |--- 2. Retrieve --->|                |               |                |
     |                     |    (BM25 + Dense)  |                |               |                |
     |                     |                    |                |               |                |
     |                     |<-- 3. Top-20 RRF --|                |               |                |
     |                     |                                     |               |                |
     |                     |--- 4. POST Rerank(Top-20) --------->|               |                |
     |                     |<-- 5. Return Top-5 High Confidence -|               |                |
     |                     |                                                     |                |
     |                     |--- 6. POST Prompt + Top-5 Context ----------------->|                |
     |                     |<-- 7. Synthesized Draft + Citations ----------------|                |
     |                     |                                                                      |
     |                     |--- 8. POST Draft Response + Context Passages ----------------------->|
     |                     |       (Extract atomic propositions & run NLI checks)                 |
     |                     |<-- 9. Verification Matrix (Entailed / Repaired Claims) --------------|
     |                     |
     |<-- 10. Final Stream-|
     |    (Verified text + |
     |    XAI heatmaps +   |
     |    citation badges) |
```

---

# CHAPTER 5: MATHEMATICAL FORMULATIONS & AI/ML/NLP ALGORITHMS

### 5.1 Text Representation: Dense Semantic Embeddings ($BAAI/bge-base-en-v1.5$)
Dense bi-encoder representations map arbitrary variable-length text sequences into a continuous, dense vector space $\\mathbb{R}^d$ where semantic affinity corresponds to directional proximity.
- **Model:** `BAAI/bge-base-en-v1.5`
- **Embedding Dimension:** $d = 768$
- **Mathematical Formulation:**
  Given a passage text $T = (w_1, w_2, \\dots, w_m)$, the text is tokenized and prepended with a special classification token $[\\text{CLS}]$. The sequence is processed through 12 Transformer encoder layers:
  $$\\mathbf{H} = \\text{TransformerEncoder}([\\text{CLS}], w_1, \\dots, w_m) \\in \\mathbb{R}^{(m+1) \\times 768}$$
  The sentence representation is extracted via mean pooling over all token representations $\\mathbf{h}_i$:
  $$\\mathbf{e}_T = \\frac{1}{m} \\sum_{i=1}^m \\mathbf{h}_i$$
  The vector is then $L_2$-normalized to project onto the unit hypersphere:
  $$\\mathbf{v}_T = \\frac{\\mathbf{e}_T}{\\|\\mathbf{e}_T\\|_2}$$
- **Dense Similarity Function:**
  Given a query vector $\\mathbf{v}_Q$ and passage vector $\\mathbf{v}_P$, the semantic similarity score is the cosine angle (which equals the dot product after $L_2$ normalization):
  $$S_{\\text{dense}}(Q, P) = \\mathbf{v}_Q \\cdot \\mathbf{v}_P = \\sum_{j=1}^{768} v_{Q, j} \\cdot v_{P, j}$$

### 5.2 Sparse Lexical Retrieval: Okapi BM25 Formulation
While dense embeddings excel at semantic paraphrasing, they compress exact token information. Okapi BM25 evaluates exact term occurrences weighted by document frequencies and document length normalization.
- **BM25 Scoring Formula:**
  Given a query $Q$ consisting of terms $q_1, q_2, \\dots, q_n$ and a candidate passage $D$:
  $$\\text{Score}_{\\text{BM25}}(D, Q) = \\sum_{i=1}^n \\text{IDF}(q_i) \\cdot \\frac{f(q_i, D) \\cdot (k_1 + 1)}{f(q_i, D) + k_1 \\cdot \\left(1 - b + b \\cdot \\frac{|D|}{\\text{avgdl}}\\right)}$$
- **Parameters & Variables:**
  - $f(q_i, D)$: Raw term frequency of query token $q_i$ in passage $D$.
  - $|D|$: Token length of document chunk $D$.
  - $\\text{avgdl}$: Average token length of all passage chunks in the corpus (configured at 512 tokens).
  - $k_1$: Term frequency saturation parameter (configured to $k_1 = 1.5$). Prevents excessively repeated keywords from artificially inflating relevance.
  - $b$: Document length normalization parameter (configured to $b = 0.75$). Penalizes abnormally long chunks.
  - $\\text{IDF}(q_i)$: Inverse Document Frequency, computed as:
    $$\\text{IDF}(q_i) = \\ln \\left( \\frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1 \\right)$$
    where $N = 14,850$ is total chunks, and $n(q_i)$ is the number of chunks containing term $q_i$.

### 5.3 Hybrid Rank Fusion: Reciprocal Rank Fusion ($RRF_k$)
Because BM25 scores (unbounded positive floats) and dense cosine similarity scores (bounded between -1 and +1) exist on completely different scales with distinct probability distributions, direct linear score combination (e.g., $\\alpha S_{\\text{BM25}} + \\beta S_{\\text{dense}}$) requires sensitive hyperparameter tuning that fails across diverse query types.

ResearchMind implements **Reciprocal Rank Fusion (RRF)**, an order-based fusion algorithm that is completely scale-invariant:
$$\\text{RRF}(d) = \\sum_{m \\in M} \\frac{1}{k + r_m(d)}$$
- **Variables & Parameters:**
  - $M = \\{\\text{BM25}, \\text{Dense}\\}$: The set of retrieval models.
  - $r_m(d) \\in \\{1, 2, 3, \\dots\\}$: The ordinal rank of passage $d$ in the output of model $m$.
  - $k = 60$: The smoothing constant. The value 60 is established in information retrieval literature (Cormack et al.) to prevent high-ranking outliers from dominating the fused ranking while ensuring documents appearing in both lists receive substantial reciprocal boosts.

### 5.4 Cross-Encoder Relevance Reranking ($BAAI/bge-reranker-base$)
Bi-encoders compute query and document representations independently ($Q \\rightarrow \\mathbf{v}_Q, D \\rightarrow \\mathbf{v}_D$), meaning the query tokens cannot attend to document tokens during encoding. To capture full cross-token interactions, ResearchMind passes the top-20 RRF candidates to a **Cross-Encoder**.
- **Model:** `BAAI/bge-reranker-base` (Cross-Attention Transformer)
- **Input Representation:**
  $$\\mathbf{x} = [\\text{CLS}] \\circ Q \\circ [\\text{SEP}] \\circ D \\circ [\\text{EOS}]$$
- **Cross-Attention Mechanism:**
  At every self-attention layer $l \\in [1, 12]$, every token in $Q$ computes attention weights with every token in $D$:
  $$\\text{Attention}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{softmax}\\left(\\frac{\\mathbf{Q}\\mathbf{K}^T}{\\sqrt{d_k}}\\right)\\mathbf{V}$$
- **Relevance Probability Output:**
  The pooled $[\\text{CLS}]$ representation is passed through a classification head:
  $$S_{\\text{cross}}(Q, D) = \\sigma(\\mathbf{W}_{\\text{rerank}} \\cdot \\mathbf{h}_{[\\text{CLS}]} + b)$$
  where $\\sigma(z) = \\frac{1}{1 + e^{-z}}$ outputs a calibrated relevance score in the range $[0, 1]$.

### 5.5 Generative Synthesis: Google Gemini 2.5 Flash
The top-5 reranked chunks are formatted with strict XML delimiters and provided to Gemini 2.5 Flash.
- **System Grounding Prompt Constraint:**
  *\"You are an expert scientific research assistant. Synthesize a comprehensive, rigorous answer strictly based on the provided context passages. For every factual assertion, you MUST attach an explicit citation marker pointing to the exact Chunk ID. If the provided context is insufficient to answer any part of the query, explicitly state that the literature does not establish the claim. Do not extrapolate beyond provided experimental findings.\"*

### 5.6 Natural Language Inference (NLI) Claim Verification Formulation
In Phase 3.4, the synthesized text $Y$ is segmented into atomic propositions $\\mathcal{C} = \\{c_1, c_2, \\dots, c_p\\}$. Each claim $c_i$ is mapped to its cited context passage $P_i$.
- **NLI Formulation:**
  For each pair $(P_i, c_i)$, the NLI engine computes the conditional probability distribution over the three standard textual inference classes:
  $$\\mathcal{Y}_{\\text{NLI}} = \\{\\text{Entailment}, \\text{Neutral}, \\text{Contradiction}\\}$$
  $$\\hat{y}_i = \\arg\\max_{y \\in \\mathcal{Y}_{\\text{NLI}}} P(y \\mid P_i, c_i)$$
- **Decision Boundary & Verification Verdict:**
  - If $\\hat{y}_i = \\text{Entailment}$ and $P(\\text{Entailment}) \\ge 0.85$: **VERIFIED (Accepted)**.
  - If $\\hat{y}_i = \\text{Neutral}$ or $P(\\text{Entailment}) < 0.85$: **UNSUPPORTED (Trigger Auto-Repair)**.
  - If $\\hat{y}_i = \\text{Contradiction}$: **CONTRADICTED (Trigger Excising / Rewrite)**.

### 5.7 XAI Token-Attribution and Attention Heatmap Mechanics
To make verification visible, ResearchMind computes token-level attribution matrices between the claim tokens $c_{i, t}$ and passage tokens $p_{j, s}$.
- **Attribution Score Formulation:**
  $$A(t, s) = \\lambda \\cdot \\text{Sim}(\\mathbf{e}_{c, t}, \\mathbf{e}_{p, s}) + (1 - \\lambda) \\cdot \\mathbb{I}(c_{i, t} == p_{j, s})$$
  where $\\mathbb{I}$ is the exact token match indicator, and $\\text{Sim}$ is the cosine similarity between token embeddings. The aggregated token importance weight $w(s)$ for passage token $s$ is:
  $$w(s) = \\max_{t} A(t, s)$$
  These weights are normalized into color intensity values $[0.0, 1.0]$ displayed as real-time visual heatmaps in the user interface.

### 5.8 Iterative Query Reformulation and Convergence Criteria
When the global verification confidence across all claims in an answer falls below the acceptable threshold ($\\frac{1}{p}\\sum_{i=1}^p P(\\text{Entailment}_i) < 0.85$), the system initiates an autonomous refinement iteration:
- **Query Reformulation:**
  $$Q_{t+1} = \\text{LLM}_{\\text{refine}}\\left(Q_t, \\{c_{\\text{unsupported}}\\}, \\{P_{\\text{retrieved}}\\}\\right)$$
- **Stopping Criteria:**
  The iteration loop terminates when:
  1. $\\text{Confidence}(Y_{t+1}) \\ge 0.88$; OR
  2. Maximum iteration limit $t_{\\max} = 3$ is reached; OR
  3. Change in retrieved chunk set $\\|\\mathcal{P}_{t+1} \\cap \\mathcal{P}_t\\| / \\|\\mathcal{P}_t\\| \\ge 0.90$ (Information Saturation).
"""

with open(path, 'a', encoding='utf-8') as f:
    f.write(chapters_4_to_5)

print("Chapters 4-5 written successfully.")
