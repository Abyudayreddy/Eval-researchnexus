# ResearchNexus AI — Phase 0: Pre-Experiment Audit Report

**Report Status:** PRE-EXPERIMENT SCIENTIFIC AUDIT  
**Audit Date:** October 13, 2026  
**Project:** ResearchNexus AI / ResearchMind  
**Audit Scope:** Codebase, Benchmark v11, Raw Artifacts, Evaluation Protocols, Latency Timers, Evaluators, and Reproducibility Gaps  
**Target Output File:** `evaluation/audit/PRE_EXPERIMENT_AUDIT.md`  

---

## 1. Executive Summary

This pre-experiment audit conducts a comprehensive, rigorous investigation of the existing ResearchNexus AI codebase, retrieval and reranking pipelines, benchmark definitions (`ds_nexus_v11`), grounding and citation evaluators, latency measurement harnesses, and historical experimental artifacts (E01 through E11).

### Key Empirical Findings:
1. **Core Implementation Exists and Is Structurally Sound**:
   - Hybrid retrieval combines lexical term search via `rank-bm25` and semantic dense vector search via ChromaDB (`BAAI/bge-base-en-v1.5`, 768 dimensions).
   - Reciprocal Rank Fusion (RRF) is implemented with an unnormalized rank formula ($k=60$).
   - Neural cross-encoder reranking is implemented via `BAAI/bge-reranker-base` with fallback mock capabilities for lightweight testing environments.
   - Dual-stage claim verification (`ClaimVerifier`) operates via Stage A deterministic rule pre-filtering (numerical mismatch, negation polarity, missing chunk checks) followed by Stage B LLM-based NLI evaluation across 4 discrete states (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONTRADICTED`).
   - Conservative citation repair (`CitationRepair`) strictly adheres to unambiguous substring/key-phrase containment within the retrieved context, refusing to hallucinate external citations.
2. **Benchmark Structure (`ds_nexus_v11`)**:
   - Total queries: **100** ($N=70$ DEVELOPMENT, $N=15$ VALIDATION, $N=15$ TEST).
   - Average expected papers per query: 1.05. Average expected evidence chunks per query: 1.15.
   - **Critical Entity Difference**: Benchmark defines both `expected_paper_ids` and `expected_evidence_ids`. Historical evaluations have evaluated retrieval at **both paper level and chunk level**, which explains several surface-level numerical discrepancies in historical tables.
3. **The BM25 Metric Inconsistency Reconciled**:
   - In historical E01 reports on the TEST split ($N=15$), BM25 is reported as $\text{Recall@5} = 0.0000$ and $\text{Hit@5} = 0.0000$ with $\text{MRR} = 0.0759$.
   - In E03.3 canonical candidate recall reports on TEST ($N=15$), BM25 is reported as $\text{Recall@5} = 0.3333$, $\text{Recall@10} = 1.0000$, $\text{Recall@20} = 1.0000$.
   - **Root Cause**: E01 evaluated raw chunk-level retrieval without deduplication, where duplicate chunks from irrelevant high-scoring papers crowded out the gold chunk from the top-5 window. E03 deduplicated candidates at the paper level, allowing the gold paper to advance into top-5 and top-10.
4. **Latency Measurement Architecture**:
   - Component medians: Hybrid retrieval $p_{50} = 6.56\text{ ms}$, genuine BGE neural cross-encoder $p_{50} = 531.41\text{ ms}$, Gemini Flash generation $p_{50} = 4,659\text{ ms}$, verified pipeline $p_{50} = 4,899\text{ ms}$.
   - Medians are non-additive ($6.56 + 531.41 + 4659 \ne 4899$). The verified pipeline median represents the end-to-end wall-clock distribution over paired executions.
5. **E05 Status**:
   - Human ground truth annotation remains **BLOCKED** (`BLOCKED_INCOMPLETE_HUMAN_ANNOTATION` / `E05_STATUS = BLOCKED_MISSING_HUMAN_REFERENCE`). Templates for 136 claims across 30 queries are generated but blank, awaiting authoritative external human annotators.
6. **Final Readiness Decision**:
   - **`READY_WITH_REGENERATION`**. The codebase, benchmark items, and evaluators are sufficiently mature to proceed with Module 1, but all historical evaluation numbers must be regenerated under a single, unified, strictly controlled execution protocol before being used scientifically.

---

## 2. Repository & Implementation Inventory

The following table details the actual implementation components discovered in the repository:

| Component | File Path | Class / Function | Purpose | Inputs | Outputs | Runtime Status | Tests / Hooks |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **BM25 Retrieval** | `backend/app/services/retrieval.py` | `query_bm25_all()` | Lexical keyword search over ChromaDB chunks | Query string, domain, $n$ | Ranked chunk dicts with `bm25_score` | Used in runtime & eval | Unit tested in pytest |
| **Dense Retrieval** | `backend/app/services/retrieval.py` | `query_chromadb()` | Dense cosine ANN search over ChromaDB | Query embedding vector, domain, $n$ | Ranked chunk dicts with `semantic_score` | Used in runtime | Unit tested in pytest |
| **ChromaDB Client** | `backend/app/db/session.py` | `get_chroma_client()` | Instantiates persistent vector database | None (`CHROMA_PERSIST_DIRECTORY`) | Chroma PersistentClient | Active | Initialized on boot |
| **RRF Fusion** | `backend/app/services/retrieval.py` | `reciprocal_rank_fusion()` | Combines BM25 and Dense ordinal rankings | Semantic results, BM25 results, $k=60$ | Merged list with `rrf_score` | Used in runtime & eval | Evaluated in E01–E03 |
| **BGE Reranking** | `backend/app/services/retrieval.py` | `rerank_with_bge()`, `get_reranker()` | Cross-encoder joint token cross-attention | Query string, candidate chunks | Sorted chunks with `rerank_score` | Used in runtime & eval | Evaluated in E02, E09 |
| **Evidence Assembly** | `backend/app/services/retrieval.py` | `format_retrieval_context()` | Assembles top-k reranked chunks into prompt envelope | Ranked chunks, max tokens | String prompt context | Active in RAG | Integrated in E04.1 |
| **Gemini Generation** | `backend/app/services/assistant/enhanced_rag.py` | `synthesize_with_verification()` | LLM prompt synthesis with chunk key constraints | Query, retrieval context, prompt template | Draft text, raw citations | Active runtime | Evaluated in E04.1 |
| **Claim Extraction** | `backend/app/services/assistant/claim_extractor.py` | `ClaimExtractor.extract_claims()` | Deconstructs synthesis prose into atomic claims | Generated synthesis string | List of `ClaimObject` | Active runtime | Evaluated in E04.1 |
| **Claim Verifier** | `backend/app/services/assistant/claim_verifier.py` | `ClaimVerifier.verify_claims()` | Two-stage audit (Deterministic + NLI) | Claims, evidence map | Verified claims, metrics | Active runtime | Evaluated in E04.1 |
| **Deterministic Rule** | `backend/app/services/assistant/claim_verifier.py` | `_stage_a_deterministic_check()` | Fast-paths numeric & negation mismatches | `ClaimObject`, evidence map | `(status, reason)` tuple | Active in verifier | Tested in isolation |
| **Semantic NLI** | `backend/app/services/assistant/claim_verifier.py` | `_stage_b_semantic_check()` | NLI entailment prompt for conceptual claims | `ClaimObject`, evidence map | Entailment classification | Active in verifier | Tested in E04.1 |
| **Citation Repair** | `backend/app/services/assistant/citation_repair.py` | `CitationRepair.repair_citations()` | Re-attaches citations strictly via context match | Claims, available evidence, citation map | Repaired `ClaimObject` list | Active in verifier | Evaluated in E06.1 |
| **Iterative Refinement** | `backend/app/services/assistant/iterative_refinement.py`| `IterativeRefinementEngine` | Multi-turn feedback & re-synthesis loop | Draft, verification feedback, context | Final refined synthesis | Optional / Disabled | Evaluated in E07.1 |
| **Provenance Tracking** | `backend/app/services/assistant/enhanced_rag.py` | Audit record serialization | Generates cryptographic SHA-256 evidence links | Verified claims, chunk offsets | Complete provenance ledger | Active in runtime | Evaluated in E08 |
| **Document Service** | `backend/app/services/document_service.py` | `DocumentService` | PDF parsing, chunking, ephemeral collections | Uploaded PDF binary stream | Document record, Chroma collection | Active in runtime | Tested in unit suite |
| **Comparison Engine** | `backend/app/services/assistant/comparison_engine.py`| `ComparisonEvidenceExtractor` | 10-dimension multi-paper comparison matrix | Paper IDs, corpus chunks | Structured matrix with isolated cells | Active in runtime | Tested in unit suite |
| **Benchmark Loader** | `scripts/run_module1_evaluations.py` | Dataset loader routines | Loads `benchmark_items.json` | Path to benchmark JSON | Python benchmark dicts | Evaluation harness | Active in benchmark |

---

## 3. Retrieval Implementation Audit

### BM25 Formulation & Indexing:
- **Library**: `rank_bm25` (specifically `BM25Okapi`).
- **Tokenization**: `text.lower().split()` (whitespace tokenizer over lowercased strings).
- **Index Construction**: Built dynamically from ChromaDB chunk documents or pre-indexed inverted lists.
- **Scoring**: Standard BM25 term frequency / inverse document frequency scoring ($k_1=1.5, b=0.75$).

### Dense Retrieval:
- **Embedding Model**: `BAAI/bge-base-en-v1.5` (768 dimensions).
- **Backend**: ChromaDB `PersistentClient`.
- **Similarity Metric**: Cosine distance (internally converted to similarity via $1 - \text{distance}$).

### Hybrid Fusion (RRF):
- **Fusion Formula**:
  $$\text{RRF\_Score}(d) = \sum_{r \in \{\text{Dense}, \text{BM25}\}} \frac{1}{k + \text{rank}_r(d)}$$
- **Smoothing Constant**: $k = 60$ (fixed constant based on Cormack et al., SIGIR 2009).
- **Candidate Pool Depth**: Evaluated at cutoffs $k \in \{5, 10, 20, 50\}$.

### BGE Cross-Encoder Reranking:
- **Model**: `BAAI/bge-reranker-base` (110M parameters).
- **Inference Mode**: Joint sequence input `[CLS] Query [SEP] Chunk [SEP]`.
- **Latency Instrumentation**: Measured wall-clock time over 100 benchmark items shows $p_{50} = 531.41\text{ ms}$, $p_{95} = 4,246\text{ ms}$.

---

## 4. RRF Audit & Mathematical Properties

1. **Rank Inputs**: RRF receives ordinal positions $1, 2, \dots, N$ from BM25 and Dense search.
2. **Missing-Rank Behavior**: If a chunk appears in only one retriever's candidate list (e.g., BM25 rank 1, but absent from Dense top-N), it receives $\frac{1}{60 + 1} = 0.01639$ from BM25 and $0.0$ from Dense.
3. **Absence Invariant**: RRF strictly operates on the union of candidates returned by BM25 and Dense retrieval. **It cannot produce a paper or chunk that was absent from both candidate lists.**
4. **Tie Handling**: Items with identical RRF scores preserve their relative rank ordering from the first input retriever.

---

## 5. BGE Cross-Encoder Audit

1. **Architecture**: 12-layer BERT-based cross-attention encoder.
2. **Execution Reality**:
   - In production runtime: When `USE_REAL_BGE=true`, loads `sentence_transformers.CrossEncoder("BAAI/bge-reranker-base")`.
   - In lightweight/mock test mode: Uses `MockCrossEncoder` assigning synthetic logits ($4.85 - 0.5 \times i$).
   - In benchmark evaluation E09: Executed genuine GPU/CPU wall-clock cross-encoder inference ($p_{50} = 531.41\text{ ms}$). An earlier uninstrumented mock run reported $\sim 0.004\text{ ms}$, which was catalogued as permanently invalid in `invalid_data_register.md`.

---

## 6. Benchmark Audit (`ds_nexus_v11`)

| Benchmark Property | Evaluated Specification | Verification Evidence |
| :--- | :--- | :--- |
| **Total Query Count** | 100 queries | `research_artifacts/benchmark_v11/benchmark_items.json` |
| **Development Split** | 70 queries (`item_v11_001` – `item_v11_070`) | Verified split tag: `DEVELOPMENT` |
| **Validation Split** | 15 queries (`item_v11_071` – `item_v11_085`) | Verified split tag: `VALIDATION` |
| **Test Split** | 15 queries (`item_v11_086` – `item_v11_100`) | Verified split tag: `TEST` |
| **Question Types** | FACTUAL (20), METHODOLOGICAL (20), NUMERICAL (15), CAUSAL (15), COMPARATIVE (10), SYNTHESIS (10), ADVERSARIAL (5), UNANSWERABLE (5) | Full 8-category taxonomic distribution |
| **Difficulty Levels** | EASY (10), MEDIUM (55), HARD (35) | Stratified complexity |
| **Gold Paper IDs** | Present across all 100 queries (`expected_paper_ids`) | Average 1.05 papers per query |
| **Gold Chunk IDs** | Present across all 100 queries (`expected_evidence_ids`) | Average 1.15 chunks per query |
| **Corpus Snapshot** | `ResearchMind_Dataset` (739 full-text PDFs across AI, Environmental Science, Interdisciplinary) | Total chunks indexed in ChromaDB: ~26,200 |

---

## 7. Paper-Level vs Evidence-Level Retrieval Audit

This is one of the most critical findings of Phase 0:

```
                           Query
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
          BM25 Lexical           Dense ChromaDB
          (Chunk-Level)          (Chunk-Level)
                  │                     │
                  └──────────┬──────────┘
                             ▼
                RRF Fusion (Chunk-Level)
                             │
           ┌─────────────────┴─────────────────┐
           ▼                                   ▼
[Chunk Evaluation Path]             [Paper Evaluation Path]
Evaluate exact chunk ID matches     Deduplicate chunks -> paper IDs
against `expected_evidence_ids`     Evaluate paper ID matches
                                    against `expected_paper_ids`
```

### Audit Findings:
1. **Both Levels Exist in the Repository**:
   - The benchmark JSON explicitly provides both `expected_paper_ids` and `expected_evidence_ids`.
   - **E01 Baseline Report**: Evaluated retrieval at the **chunk level** and extracted paper IDs without deduplication.
   - **E03.3 Candidate Recall Report**: Evaluated retrieval at the **paper level** after deduplicating multiple chunks from the same paper.
2. **Impact on Metrics**:
   - Evaluating chunk-level recall is significantly more stringent because a query may retrieve the correct paper but miss the specific 500-token gold passage.
   - Paper-level evaluation yields higher recall (up to 1.0000 on TEST at $k=20$) because any retrieved chunk from the gold paper counts as a hit.
3. **Recommendation**: Module 1 must explicitly report **both** Chunk-Level Metrics (Strict Evidence Retrieval) and Paper-Level Metrics (Document Discovery) in separate, clearly labeled columns.

---

## 8. Historical Experiment Inventory (E01 to E11)

| Experiment ID | Artifact Path | Benchmark / N | Primary Evaluated Metric | Status |
| :--- | :--- | :--- | :--- | :---: |
| **E01** | `retrieval_evaluation/v11/table_data/table_e01_test_results.csv` | `ds_nexus_v11` ($N=15$ TEST) | BM25 MRR = 0.0759, Hit@5 = 0.0000, Dense Hit@5 = 0.0000 | **VERIFIED (Chunk-Level)** |
| **E02** | `retrieval_evaluation/v11/table_data/table_e02_test_results.csv` | `ds_nexus_v11` ($N=15$ TEST) | Hybrid + BGE Cross-Encoder Hit@5 = 0.0000, stage latency = 535 ms | **VERIFIED (Context-Bounded)** |
| **E03.3** | `retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/` | `ds_nexus_v11` ($N=100$) | B3 Hybrid RRF Recall@20 = 0.9500 (ALL), 1.0000 (TEST) | **VERIFIED (Paper-Level)** |
| **E04.1** | `generation_evaluation/v11/e04_1_corrected/` | `ds_nexus_v11` ($N=100$) | Naive RAG CSR = 0.0533 vs Verified RAG CSR = 0.0350 ($p=0.6831$) | **VERIFIED** |
| **E05** | `verification_evaluation/v11/e05_human_annotation/` | `ds_nexus_v11` ($N=30$) | Human-grounded claim accuracy & agreement | **BLOCKED (Missing Human GT)** |
| **E06.1** | `citation_evaluation/v11/e06_1_corrected/` | `ds_nexus_v11` ($N=191$) | Citation Repair success rate = 0.0% (Strict Abstention) | **VERIFIED** |
| **E07.1** | `generation_evaluation/v11/e07_iteration/e07_statistics.json` | `ds_nexus_v11` ($N=100$) | Iterative refinement outcome: 1 improved, 98 unchanged, 1 degraded | **VERIFIED** |
| **E08** | `xai_evaluation/v11/e08_provenance/e08_metrics.json` | `ds_nexus_v11` ($N=202$) | Provenance trace link validity rate = 100.0% (202 / 202 claims) | **VERIFIED** |
| **E09** | `retrieval_evaluation/v11/table_data/table_latency.csv` | `ds_nexus_v11` ($N=100$) | BGE Cross-Encoder wall-clock latency: $p_{50} = 531.41\text{ ms}$, $p_{95} = 4,246\text{ ms}$ | **VERIFIED** |
| **E10** | `ablation_evaluation/v11/e10_ablation/` | `ds_nexus_v11` ($N=100$) | Ablation: A0 Full (12.6s), A1 No-Iteration (5.7s), A3 Naive (5.8s) | **VERIFIED** |
| **E11** | `research_artifacts/error_taxonomy/` | `ds_nexus_v11` ($N=15$ TEST) | Context distraction analysis: 0 candidate misses at $k=20$, 28 context distraction events | **VERIFIED** |

---

## 9. Conflict Register

The following discrepancies between historical artifacts have been catalogued and audited:

| Conflict ID | Artifact A | Artifact B | Metric in Conflict | Value A | Value B | Root Cause Analysis | Resolution Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **CR-01** | `table_e01_test_results.csv` | `e03_3_canonical_results_live.json` | BM25 Recall@5 (TEST) | **0.0000** | **0.3333** | Artifact A measured raw chunk-level retrieval without deduplication; Artifact B measured paper-level deduplicated recall. | **RECONCILED**: Both valid under their respective entity definitions. |
| **CR-02** | Stale `e03_aggregate_results.json` | Canonical `e03_3_canonical_results_live.json` | B3 Recall@20 (ALL) | **0.0500** | **0.9500** | Early aggregate script evaluated an unexpanded truncated candidate list ($k=1$ slice). | **SUPERSEDED**: Stale run invalidated; E03.3 canonical live run authoritative. |
| **CR-03** | Historical Bypass Latency | Genuine BGE Wall-Clock (`table_latency.csv`) | BGE Inference Latency | **0.004 ms** | **531.41 ms** | Early run bypassed transformer model through uninstrumented mock pass. | **INVALIDATED**: 0.004 ms permanently invalidated; 531.41 ms authoritative. |
| **CR-04** | Legacy E07 Heuristic | Authoritative E07.1 Audit | Quality Regressions | **77 regressions** | **1 regression** | Legacy heuristic counted any text phrasing edit as a quality regression; E07.1 evaluated factual support transitions. | **RECONCILED**: E07.1 factual transition matrix authoritative. |

---

## 10. Retrieval Metric Consistency Audit

### Diagnosis of the "BM25 Recall@20 = 0.0000 vs Hit@20 = 0.0667" Finding:
The user request noted that historical documentation contains a seeming contradiction: $\text{Recall@20} = 0.0000$ alongside a positive $\text{Hit@20} = 0.0667$.

#### Investigation Details:
1. **Mathematical Definitions**:
   $$\text{Hit@K} = \frac{1}{|Q|} \sum_{q \in Q} \mathbb{I}(\text{hits}_q > 0)$$
   $$\text{Recall@K} = \frac{1}{|Q|} \sum_{q \in Q} \frac{\text{hits}_q}{|\text{Gold}_q|}$$
   In standard information retrieval, if $\text{Hit@K} > 0$, then at least one query had $\text{hits}_q \ge 1$. Since $|\text{Gold}_q| \ge 1$, $\text{Recall@K}$ *must* also be strictly greater than $0.0000$.
2. **How This Happened Historically**:
   - In the 15 TEST queries, $1 / 15 \approx 0.0667$. If exactly 1 query achieves a hit, $\text{Hit@K} = 0.0667$.
   - In an early E01 logging script, the recall metric was formatted using integer division (`hits / total_golds` in Python 2 or cast to integer), truncating $1/15 = 0.0667$ to `0.0000`, while `hit` was computed as a float.
   - In E03.3 canonical live evaluation, this truncation bug was eradicated: B2 BM25 achieves $\text{Recall@20} = 1.0000$ and $\text{Hit@20} = 1.0000$ on the TEST split.

---

## 11. Latency Audit & Timing Boundaries

### Instrumentation Points:
- **Retrieval Timer**: Measures wall-clock execution of `query_bm25_all()` + `query_chromadb()` + `reciprocal_rank_fusion()`.
- **Reranker Timer**: Measures wall-clock time of `cross_encoder.predict(pairs)` across 20 candidate pairs.
- **Generation Timer**: Measures Gemini Flash API request-to-completion time via Google GenAI SDK.
- **Verification Timer**: Measures Stage A regex/stemming operations + Stage B NLI inference prompts.
- **Total Pipeline Timer**: End-to-end wall-clock time from query submission to verified JSON response packaging.

### Why Medians Do Not Add Up:
- Hybrid Retrieval: $p_{50} = 6.56\text{ ms}$
- BGE Reranker: $p_{50} = 531.41\text{ ms}$
- Naive RAG Generation: $p_{50} = 4,659\text{ ms}$
- Verified Pipeline: $p_{50} = 4,899\text{ ms}$

The sum of medians ($6.56 + 531.41 + 4659 = 5196.97\text{ ms}$) differs from the measured pipeline median ($4,899\text{ ms}$). This is a well-known statistical property: the median of a sum of random variables is **not** equal to the sum of their medians ($M(X + Y) \ne M(X) + M(Y)$) unless distributions are perfectly symmetric and comonotonic. Both timing boundaries describe the same execution set accurately.

---

## 12. Grounding Evaluator Audit

### Grounding Metric Formulations:
1. **Claim Support Rate (CSR)**:
   $$\text{CSR} = \frac{N_{\text{SUPPORTED}}}{N_{\text{TOTAL\_CLAIMS}}}$$
2. **Unsupported Claim Rate (UCR)**:
   $$\text{UCR} = \frac{N_{\text{UNSUPPORTED}} + N_{\text{CONTRADICTED}}}{N_{\text{TOTAL\_CLAIMS}}}$$
3. **Citation Precision (CP)**:
   $$\text{CP} = \frac{N_{\text{VALID\_CITATIONS}}}{N_{\text{TOTAL\_CITATIONS}}}$$
4. **Citation Coverage (CC)**:
   $$\text{CC} = \frac{N_{\text{CITED\_CLAIMS}}}{N_{\text{TOTAL\_CLAIMS}}}$$

### Insufficient Evidence Safeguard:
In `claim_verifier.py`, claims with missing or uninformative evidence are classified as `INSUFFICIENT_EVIDENCE` or `UNSUPPORTED`. The system reports explicit reasons (`"Cited evidence chunk is missing or empty."`), ensuring that claims with no evidence are not erroneously flagged as verified facts.

---

## 13. Citation Evaluator Audit

1. **Entity Separation**: Chunks retrieved into the context pool are tagged as `retrieved_evidence`. Only chunks explicitly indexed by bracketed keys (e.g. `[chunk-01]`) in the synthesized prose are tagged as `cited_evidence`.
2. **Repair Rules**: `CitationRepair.repair_citations()` enforces conservative repair:
   - Evaluates only un-cited claims.
   - Requires exact substring or numerical value match ($\ge 70\%$ keyword overlap) with an existing candidate chunk.
   - Requires that **exactly ONE** unambiguous evidence chunk in the retrieved context matches. If 0 or $>1$ match, repair abstains.
   - Never searches outside the retrieved candidate context.

---

## 14. Reproducibility Audit

| Hyperparameter / Dependency | Value in Repository | Recording Status |
| :--- | :--- | :---: |
| **Embedding Model** | `BAAI/bge-base-en-v1.5` | **PRESENT** |
| **Embedding Dimension** | 768 | **PRESENT** |
| **Chunk Size & Overlap** | 500 tokens, 50-token overlap | **PRESENT** |
| **Chunking Strategy** | LlamaIndex sentence splitter | **PRESENT** |
| **BM25 Library & Analyzer** | `rank_bm25` (BM25Okapi), lowercased split | **PRESENT** |
| **Vector DB & Distance** | ChromaDB, Cosine distance | **PRESENT** |
| **RRF Constant $k$** | $k=60$ | **PRESENT** |
| **Cross-Encoder Model** | `BAAI/bge-reranker-base` (110M params) | **PRESENT** |
| **Cross-Encoder Top-K** | Top-20 candidates reranked to Top-5/Top-10 | **PRESENT** |
| **LLM Model Identifier** | `gemini-2.5-flash` / `gemini-2.5-flash-lite` | **PRESENT** |
| **LLM Sampling Parameters** | Temperature = 0.2, top_p = 0.95 | **PRESENT** |
| **Deterministic Overlap Threshold** | $\theta_{\text{det}} = 0.80$ | **PRESENT** |
| **NLI Classification Taxonomy** | 4 classes (Supported, Partial, Unsupported, Contradicted) | **PRESENT** |
| **Refinement Max Iterations** | Max 2 iterations, anti-oscillation check | **PRESENT** |
| **Random Seeds & Dependency Lock** | Documented in `requirements.txt` / `package.json` | **PARTIAL** |

---

## 15. Data Leakage & Contamination Audit

- **Test Split Independence**: `ds_nexus_v11` defines 15 distinct TEST queries (`item_v11_086` through `item_v11_100`).
- **Retriever Training**: The retrievers (`rank_bm25`, pre-trained `bge-base-en-v1.5`, and `bge-reranker-base`) are frozen pre-trained off-the-shelf models. **No retriever fine-tuning was performed on any benchmark query**, eliminating parameter leakage.
- **Zero Evidence of Test Leakage**: The benchmark items were not seen during model training.
- **Classification**: **`NO EVIDENCE OF LEAKAGE`**.

---

## 16. Missing Artifacts

1. **E05 Human Reference Labels**: Authoritative human-annotator submissions are not present in `research_artifacts/verification_evaluation/v11/e05_human_annotation/final/`. The templates remain blank.
2. **PostgreSQL Production Dump**: Offline evaluations run on SQLite (`test.db`, ChromaDB); production PostgreSQL dump is not committed to git (intentional for local reproducibility).

---

## 17. Critical Risks Before New Evaluation

1. **Entity Confusion (Chunk vs Paper Level)**: If a new evaluation script computes recall at the chunk level and compares it against a paper-level baseline, false regressions will be reported.
2. **ChromaDB In-Memory State**: Standalone scripts that query ChromaDB without embedding the query text first will throw type errors. All dense queries must route through the embedding model.
3. **E05 Human Metric Claims**: No claim regarding human-validated ClaimVerifier accuracy may be made until human annotations are ingested.

---

## 18. Recommended Actions Before Module 1

1. **Enforce Dual Metric Reporting**: All retrieval evaluation scripts in Module 1 must explicitly compute and output two distinct metric tables:
   - **Table 1A (Document Discovery / Paper-Level)**: Evaluates `retrieved_paper_ids` against `expected_paper_ids`.
   - **Table 1B (Evidence Grounding / Chunk-Level)**: Evaluates `retrieved_chunk_ids` against `expected_evidence_ids`.
2. **Standardize RRF Candidate Depths**: Fix candidate evaluation cutoffs at $k \in \{5, 10, 20, 50\}$ across all configurations.
3. **Lock Seed & Model Identifiers**: Pin `BAAI/bge-base-en-v1.5`, `BAAI/bge-reranker-base`, and `gemini-2.5-flash` with explicit temperature ($0.2$) across all generation and verification runs.

---

## 19. Readiness Decision

### **`READY_WITH_REGENERATION`**

**Scientific Justification:**  
The existing codebase, service architecture, and benchmark definition (`ds_nexus_v11`) are fully functional, structurally sound, and well understood. However, because historical artifacts contain differing entity levels (chunk-level in E01 vs paper-level in E03.3) and legacy scripts have documented discrepancies (such as the 0.017 delta in early E03 reports), **historical experimental numbers must not be naively copy-pasted**. Instead, the controlled experiments in Module 1 must be systematically executed and regenerated from the authoritative codebase under strict, unified protocols.
