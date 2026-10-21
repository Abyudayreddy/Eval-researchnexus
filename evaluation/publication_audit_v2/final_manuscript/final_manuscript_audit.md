# Final Manuscript Audit Report
**Manuscript**: `ResearchNexusAI: An Explainable Multi-Stage RAG Framework for Scientific Literature Synthesis`  
**Target Format**: IEEE Conference Proceedings (Maximum 6 Pages)  
**Output Directory**: `evaluation/publication_audit_v2/final_manuscript/`  
**Compiled Artifact**: `ResearchNexusAI_IEEE_Final_Max6Pages.pdf`  
**LaTeX Source**: `ResearchNexusAI_IEEE_Final.tex`  
**Date**: October 17, 2026  

---

## 1. Compliance and Page-Budget Verification

- **Target Page Limit**: Maximum 6 pages.
- **Compiled Page Count**: Exactly **3 pages** (Verified via `pypdf` and `PyMuPDF`).
- **IEEE Conference Format**: Two-column layout (column width 260 pt, gutter 20 pt), standard IEEE typography (Times-Roman, Times-Bold, Times-Italic), IEEE title/author block, bold-italic abstract, index terms, numbered roman section headings, compact formal tables (Tables I–IV), pipeline architecture box (Fig. 1), and numbered bibliography in citation order.
- **Status**: **PASS (Strictly $\le$ 6 Pages)**.

---

## 2. Experimental Result and Metric Verification

All quantitative statements in the text, abstract, and tables correspond to the V4 canonical reconciliation package (`canonical_retrieval_metrics.csv`, `canonical_claim_accounting.csv`, `canonical_grounding_metrics.json`, `canonical_latency_results.csv`, and `canonical_benchmark_manifest.json`):

1. **Retrieval Metrics (Table I)**:
   - **BM25 Lexical**: Hit@5 = 0.0000, Hit@10 = 0.6667 (10/15), Hit@20 = 0.6667 (10/15), Recall@20 (10 answerable test items) = 1.0000 (10/10). MRR (all 15 items) = 0.0759, MRR (10 answerable items) = 0.1139.
   - **Dense Chroma**: Hit@20 = 0.0000 on test split (stale claim of 0.6000 was synthetic).
   - **Hybrid RRF ($k=60$)**: Hit@20 = 0.6667 (10/15), Recall@20 (answerable) = 1.0000 (10/10), MRR (all 15) = 0.0431, MRR (answerable) = 0.0647.
   - **BGE Neural Reranker**: Hit@20 = 0.6667 (10/15), MRR (all 15) = 0.0480, MRR (answerable) = 0.0720.
   - **Withdrawn Claims Filtered**: The ungrounded claims of Hybrid Hit@20 = 11/15, Hybrid MRR = 0.3685, BGE MRR = 0.5444, and +47.7% relative gain **do not appear** anywhere in the paper.
2. **Claim Grounding & Epistemic Decoupling (Table II)**:
   - Evaluated candidate sentences: 56 total (28 naive, 28 verified).
   - Epistemic breakdown: 30 appropriate abstentions, 19 insufficient evidence findings, 7 positive factual assertions across systems.
   - Automated NLI factual precision: 100.0% (4/4 in Naive RAG, 3/3 in Verified RAG).
   - Epistemic abstention accuracy on unanswerable queries: 100.0% (5/5).
   - Disclosed limitation: 100% automated precision on 7 claims does not establish generalized factual grounding.
3. **Citation Repair and Iterative Refinement (Table III)**:
   - Eligible factual claims: 5 (baseline valid citation rate 20.0%, 1/5).
   - Candidate repairs attempted: 4 (detected in `item_v11_092`).
   - Ambiguity filter rejections: 4 / 4 (each statement matched 10 chunks simultaneously).
   - Safely applied repairs: 0 (Repair effect: NOT DEMONSTRATED; Coverage gain: NOT OBSERVED; Safety: NOT ESTIMABLE).
   - Refinement ablation ($N=100$): 1 improved, 98 unchanged, 1 degraded query ($p=1.000$, permutation test; net gain 0.0%).
4. **Latency Decomposed Profile (Table IV)**:
   - BM25 p50 = 0.69 ms, Dense p50 = 13.51 ms, Hybrid RRF p50 = 6.56 ms.
   - BGE Cross-Encoder p50 = 531.41 ms (p95 = 4,246.05 ms).
   - Combined retrieval+reranking stage p50 = 535.06 ms.
   - Generation stage: single-pass p50 = 1,420 ms; secondary refinement pass p50 = 2,930 ms (+106.3% stage latency increase).
   - Complete request end-to-end latency: without refinement mean = 5,691.35 ms (p50 = 4,899.07 ms); with refinement mean = 12,655.70 ms (p50 = 11,064.67 ms) (+122.4% complete request latency increase). Component percentiles are explicitly noted as non-additive.
5. **Human Validation Status**:
   - Formally disclosed in abstract, Table II, and Section V as **BLOCKED / NOT MEASURED** due to the absence of external double-blind human labels.

---

## 3. Bibliographic Integrity

- **Principal Base Paper**: OpenScholar [1] retained and prominently analyzed in Section II, Section III, and Section IV as the primary related-work baseline.
- **Removed References**: SciRAG [19] and PeerQA [20] are completely absent from the text and bibliography.
- **Reference Citations**: All citations ([1] through [7]) strictly map to valid entries in the bibliography in citation order.

---

## 4. File Inventory

| File Path | Description | Verification Status |
| :--- | :--- | :---: |
| `evaluation/publication_audit_v2/final_manuscript/ResearchNexusAI_IEEE_Final_Max6Pages.pdf` | Final compiled 3-page IEEE PDF manuscript | **VERIFIED ($\le$ 6 pages)** |
| `evaluation/publication_audit_v2/final_manuscript/ResearchNexusAI_IEEE_Final.tex` | IEEEtran conference LaTeX source code | **VERIFIED** |
| `evaluation/publication_audit_v2/final_manuscript/manuscript_claim_evidence_map.csv` | Full mapping of 11 quantitative statements to raw V4 artifacts | **VERIFIED** |
| `evaluation/publication_audit_v2/final_manuscript/final_manuscript_audit.md` | Audit verification report | **VERIFIED** |

---

## 5. Submission Readiness Determination

**Gate Status: READY_FOR_SUBMISSION_WITH_LIMITATIONS**  
The manuscript represents an evidence-grounded engineering and empirical evaluation study that honestly reports demonstrated benefits alongside null/negative results and research limitations.
