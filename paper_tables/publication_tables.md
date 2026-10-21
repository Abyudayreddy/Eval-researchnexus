# Authoritative Publication Tables: ResearchNexus Conference Paper

**Paper Title**: *ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis*

**Target Venue**: IEEE Conference Proceedings

**Frozen Benchmark**: `ds_nexus_v11` ($N=100$: DEV=70, VAL=15, TEST=15)

---

## TABLE I: DATASET SPECIFICATION AND EVALUATION PROTOCOL

| Characteristic | Value / Distribution | Description |
| :--- | :--- | :--- |
| **Benchmark Dataset** | `ds_nexus_v11` | Standardized multi-domain scientific benchmark |
| **Corpus Size** | 40 papers / 80 chunks | Target literature documents across AI, NLP, CV, and IR |
| **Query Splits** | Total $N=100$ | DEV = 70, VAL = 15, TEST = 15 |
| **Query Categorization** | 8 categories ($N=100$) | Factual: 20, Methodological: 20, Numerical: 15, Causal: 15, Comparative: 10, Synthesis: 10, Adversarial: 5, Unanswerable: 5 |
| **Retrieval Evaluation** | E03.3 Candidate Recall | Lexical (BM25), Dense (Chroma), and Hybrid RRF ($k=60$) |
| **Generation Grounding** | E04.1 Grounding Analysis | Naive RAG vs. Verified RAG ($N=100$) with McNemar paired test |
| **Human Verification** | E05 Ground Truth | **NOT MEASURED** (Human expert ground-truth annotations unavailable) |
| **Citation Repair** | E06.1 CitationRepair | Deterministic substring context matching (191 opportunities) |
| **Iterative Refinement** | E07.1 Multi-Pass Refinement | Paired permutation test on query-level quality shifts |
| **Provenance Audit** | E08 Automated XAI Layer | Automated verification of bidirectional link and text offset integrity |
| **System Latencies** | E09 Stage Decomposition | Granular profiling ($p50$, $p95$) of retrieval and cross-encoder inference |
| **Component Ablations** | E10 Controlled Ablations | Single-factor architectural deletions ($A0$–$A6$) |
| **Error Taxonomy** | E11 Failure Classification | 14-category multi-label failure categorization on TEST split ($N=15$) |

## TABLE II: CANDIDATE CONTEXT RETRIEVAL PERFORMANCE

*Hybrid RRF candidate-context retrieval on ALL N=100 queries.*

| Candidate Pool Size ($k$) | Recall@k | Hit@k |
| :---: | :---: | :---: |
| 5 | 0.2700 | 0.3000 |
| 10 | 0.5700 | 0.6200 |
| 20 | 0.9500 | 1.0000 |
| 50 | 1.0000 | 1.0000 |

> **Note**: TEST ($N=15$): all 10 answerable targets are present within the canonical $k=20$ pool; 5 additional TEST queries are unanswerable probes.

## TABLE III: GENERATION GROUNDING: NAIVE VS. VERIFIED RAG

| Metric | Description | Naive RAG | Verified RAG | Desired Direction |
| :--- | :--- | :---: | :---: | :---: |
| **CSR** | Claim Support Ratio | 0.0533 | 0.0350 | ↑ better |
| **UCR** | Unsupported Claim Ratio | 0.9467 | 0.9650 | ↓ better |
| **CP** | Citation Precision | 0.0600 | 0.0400 | ↑ better |
| **COV** | Citation Coverage | 0.0617 | 0.0433 | ↑ better |

> **Statistical Test**: McNemar paired statistic = 0.1667, $p = 0.6831$.
> **Conclusion**: No statistically significant grounding improvement was observed.

## TABLE IV: SYSTEM LATENCY AND ITERATIVE REFINEMENT

### Part A: Disaggregated Pre-Generation Latency (E09, $N=100$)

| Processing Stage | $p50$ (ms) | $p95$ (ms) |
| :--- | :---: | :---: |
| Hybrid Retrieval | 6.56 | 19.12 |
| Pure BGE Inference | 531.41 | 4246.05 |
| Hybrid + BGE Combined | 535.06 | 4251.51 |

### Part B: Iterative Refinement Quality & Runtime Tradeoff (E07.1, $N=100$)

| Configuration | Mean Latency (ms) | Improved Queries | Unchanged Queries | Degraded Queries |
| :--- | :---: | :---: | :---: | :---: |
| Iteration OFF | 5691.35 | — | — | — |
| Iteration ON | 12655.70 | 1 | 98 | 1 |

> **Quality Impact**: $\Delta\text{CSR} = -0.0017$; Exact paired permutation $p = 1.0000$. Overhead multiplier = 2.22x.

### Part C: Automated XAI Provenance Layer Integrity (E08, $N=202$ Claims)

| Provenance Metric | Audit Value |
| :--- | :---: |
| Trace Completeness | 1.0000 (100.0%) |
| Claim-to-Evidence Accuracy | 1.0000 (100.0%) |
| Citation-to-Evidence Accuracy | 1.0000 (100.0%) |
| Offset Resolution Accuracy | 1.0000 (100.0%) |

> **Note**: N = 202 automated claim traces. These are automated provenance-audit metrics, not human explainability measures.

## TABLE V: ARCHITECTURAL COMPONENT ABLATION STUDY (E10, $N=100$)

| Configuration | Description | CSR | Mean Latency (ms) | Latency Status |
| :---: | :--- | :---: | :---: | :---: |
| **A0** | Full Pipeline | 0.0333 | 12655.70 | Direct |
| **A1** | Minus Iteration | 0.0350 | 5691.35 | Direct |
| **A2** | Minus Citation Repair | 0.0533 | 12610.70 | DERIVED |
| **A3** | Naive RAG Baseline | 0.0533 | 5767.46 | Direct |
| **A4** | Minus BGE Reranker | 0.0333 | 12124.29 | DERIVED |
| **A5** | Dense Only Baseline | 0.0000 | 8.46 | Direct |
| **A6** | BM25 Only Baseline | 0.0333 | 0.98 | Direct |

> *Footnote*: A2 and A4 latency values are mathematically derived component decompositions rather than independent end-to-end wall-clock runs.

## TABLE VI: ERROR TAXONOMY ANALYSIS (E11, TEST SPLIT $N=15$, 28 CLAIMS)

| Category | Event Count | Failure Level | Measurement Status / Interpretation |
| :--- | :---: | :---: | :--- |
| **1. Measured Failure Categories** | | | |
| `UNSUPPORTED_CLAIM` | **28** | Claim | measured (Concentrated failure mode) |
| `MISSING_CITATION` | **28** | Claim | measured (Concentrated failure mode) |
| `CITATION_REPAIR_FAILURE` | **27** | Citation | measured (Concentrated failure mode) |
| `ITERATION_FAILURE` | **15** | Query | measured (Concentrated failure mode) |
| **2. Zero Measured Categories** | | | |
| `RETRIEVAL_MISS` | 0 | Query | measured (0 events at canonical $k=20$) |
| `CANDIDATE_POOL_MISS` | 0 | Query | measured (0 events at canonical $k=20$) |
| `RERANKING_ERROR` | 0 | Query | measured (0 events at canonical $k=20$) |
| `EVIDENCE_SELECTION_ERROR` | 0 | Query | measured (0 events at canonical $k=20$) |
| `CONTRADICTED_CLAIM` | 0 | Claim | measured (0 events at canonical $k=20$) |
| `WRONG_CITATION` | 0 | Claim | measured (0 events at canonical $k=20$) |
| `ONLINE_RETRIEVAL_FAILURE` | 0 | Query | measured (0 events at canonical $k=20$) |
| `XAI_PROVENANCE_FAILURE` | 0 | Claim | measured (0 events at canonical $k=20$) |
| **3. Unmeasured Categories** | | | |
| `VERIFICATION_FALSE_POSITIVE` | *NOT MEASURED* | Claim | unmeasured (E05 human GT unavailable) |
| `VERIFICATION_FALSE_NEGATIVE` | *NOT MEASURED* | Claim | unmeasured (E05 human GT unavailable) |

> **Total Categorized Events**: 98 multi-label failure events across 15 TEST queries.
