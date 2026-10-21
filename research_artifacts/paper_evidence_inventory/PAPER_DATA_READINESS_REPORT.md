# ResearchNexus Paper Data Readiness Report (Master Evidence Inventory)

## 1. Executive Summary

This report completes **Phase A: Master Paper Evidence Inventory** for the research project *“ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis”*.

Every dataset, experimental log, metric output, figure data CSV, and table data CSV across the repository has been audited, categorized, and assigned a strict verification status.

---

## 2. Key Synthesis Findings (A through J)

### A. What Data We Already Have
1. **Benchmark Data**: Frozen, independent benchmark dataset `ds_nexus_v11` (100 items: 70 DEV, 15 VAL, 15 TEST) created from 40 real scientific ArXiv papers.
2. **Retrieval Baseline Data (E01)**: Raw per-query evaluation logs across BM25, Dense Chroma, and Hybrid RRF ($k=60$) over all 100 benchmark items.
3. **Reranking Data (E02)**: Raw per-query evaluation logs for genuine BAE/bge-reranker-base Cross-Encoder reranking (100% invocation rate, 0% bypass rate).
4. **Latency Benchmark Data**: Disaggregated timing logs for Hybrid retrieval (p50 = 6.56 ms) and Pure BGE model inference (p50 = 531.41 ms, p95 = 4,246.05 ms).
5. **Statistical & Forensics Data**: Paired t-test/Wilcoxon tests on DEVELOPMENT split ($p = 3.61 \times 10^{-7}$ for NDCG@5) and item-level rank movement traces.

---

### B. Which Results Can Directly Enter a Paper
1. **Table 1: Benchmark Dataset Characteristics (`ds_nexus_v11`)**: 100 queries, split distributions, SHA256 test set integrity hash.
2. **Table 2: Baseline Retrieval Performance (E01 vs E02 on DEV & ALL splits)**: BM25, Dense, Hybrid RRF, and Hybrid + BGE metrics.
3. **Table 3: Latency & Computational Overhead Breakdown**: Hybrid retrieval latency vs. Pure BGE Cross-Encoder inference latency.
4. **Figure 1 & Figure 2**: Retrieval metric comparison charts (`figure_1_e01_retrieval.csv`, `figure_2_e02_reranking.csv`).
5. **Figure 4**: Latency cumulative distribution chart (`figure_4_latency.csv`).

---

### C. Which Metrics Must Be Recomputed
- **Zero Metrics Required for Module 1**: All Module 1 metrics (E01 and E02) were independently re-derived and verified in Module 1.9.1 (**0 mismatches / 400 records**). No retrieval metrics need recomputation.

---

### D. Which Experiments Are Missing
1. **Module 2 RAG Generation Baselines**: Standard LLM literature synthesis runs without verification.
2. **Module 2 Claim Extraction & NLI Verification**: Empirical evaluation of claim verification precision and hallucination reduction.
3. **Module 2 Citation Repair**: Empirical evaluation of iterative retrieval repair on unsupported claims.

---

### E. Which Implementation Modules Need Testing
- **Backend RAG Services (`backend/app/services/rag_service.py`)**: The multi-stage prompt generation, hallucination verification, and citation repair code modules exist in the codebase but have **0 empirical evaluation logs**.

---

### F. Which Figures Can Already Be Produced
- **Figure 1**: Baseline Retrieval Comparison (`figure_1_e01_retrieval.csv`)
- **Figure 2**: BGE Cross-Encoder Reranking Gains (`figure_2_e02_reranking.csv`)
- **Figure 3**: Gold Document Rank Movement Distribution (`figure_3_rank_movement.csv`)
- **Figure 4**: Latency Distribution (Hybrid vs. Pure BGE vs. Total Stage) (`figure_4_latency.csv`)

---

### G. Which Tables Can Already Be Produced
- **Table 1**: Benchmark Dataset Metadata (`ds_nexus_v11_manifest.json`)
- **Table 2**: E01 Baseline Retrieval Results on TEST Split (`table_e01_test_results.csv`)
- **Table 3**: E02 BGE Reranking Results on TEST Split (`table_e02_test_results.csv`)
- **Table 4**: Rank Movement Category Breakdown (`table_e02_rank_movement.csv`)
- **Table 5**: Pipeline Latency Breakdown (`table_latency.csv`)

---

### H. Which Research Questions Currently Have Evidence
- **RQ1 (Retrieval Effectiveness)**: *"Does hybrid fusion (BM25 + Dense) outperform individual retrieval modalities on scientific literature synthesis queries?"* — **ANSWERED WITH EVIDENCE** (BM25 Hit@5=0.57, Dense Hit@5=0.0).
- **RQ2 (Cross-Encoder Reranking)**: *"Does BGE Cross-Encoder reranking significantly improve hybrid retrieval precision and ranking quality?"* — **ANSWERED WITH EVIDENCE** (DEV NDCG@5 gain $+0.2697$, $p=3.61 \times 10^{-7}$).
- **RQ3 (Reranking Latency Overhead)**: *"What is the exact inference latency overhead of applying BGE Cross-Encoder reranking?"* — **ANSWERED WITH EVIDENCE** (p50 = 531.41 ms).

---

### I. Which Research Questions Currently Lack Evidence
- **RQ4 (RAG Synthesis Quality)**: *"Does multi-stage context management improve LLM literature synthesis faithfulness compared to naive RAG?"* — **LACKS EVIDENCE** (Module 2 required).
- **RQ5 (Hallucination Verification)**: *"How effectively does claim extraction and NLI verification detect ungrounded statements in generated scientific text?"* — **LACKS EVIDENCE** (Module 2 required).
- **RQ6 (Citation Repair)**: *"Does iterative citation repair eliminate unsupported claims in synthetic literature reviews?"* — **LACKS EVIDENCE** (Module 2 required).

---

### J. Minimum Experiment Set Required to Complete a Defensible Conference Paper

To publish a defensible paper at a top-tier conference (e.g., SIGIR, EMNLP, ACL, NeurIPS RAG Workshop), the system requires the following **minimum experiment set**:

1. **Module 1 Retrieval Section (COMPLETE)**: Use existing verified E01/E02 baseline results on `ds_nexus_v11` (Figures 1–4, Tables 1–5).
2. **Module 2 Generation Section (REQUIRED)**:
   - Execute **Naive RAG Baseline** (LLM synthesis using top-5 B4 retrieved chunks).
   - Execute **ResearchNexus Verified RAG** (LLM synthesis + NLI claim verification + citation repair).
   - Evaluate on `ds_nexus_v11` ($N=100$) using **Faithfulness %, Unsupported Claim %, Citation Precision/Recall %, and End-to-End Latency**.

---

## 3. Inventory Status & Stop

All Phase A inventory artifacts have been created in `research_artifacts/paper_evidence_inventory/`:
- [MASTER_EVIDENCE_MATRIX.csv](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/paper_evidence_inventory/MASTER_EVIDENCE_MATRIX.csv) & [MASTER_EVIDENCE_MATRIX.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/paper_evidence_inventory/MASTER_EVIDENCE_MATRIX.md)
- [EXPERIMENT_INVENTORY.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/paper_evidence_inventory/EXPERIMENT_INVENTORY.md)
- [METRIC_INVENTORY.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/paper_evidence_inventory/METRIC_INVENTORY.md)
- [CLAIM_EVIDENCE_MAP.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/paper_evidence_inventory/CLAIM_EVIDENCE_MAP.md)
- [MISSING_EXPERIMENTS.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/paper_evidence_inventory/MISSING_EXPERIMENTS.md)
- [INVALID_OR_DO_NOT_USE.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/paper_evidence_inventory/INVALID_OR_DO_NOT_USE.md)
- [PAPER_DATA_READINESS_REPORT.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/paper_evidence_inventory/PAPER_DATA_READINESS_REPORT.md)

**Phase A inventory is complete. Execution has stopped.**
