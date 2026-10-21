# Publication Tables Package: ResearchNexus Conference Paper

**Paper Title**: *ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis*  
**Format Standard**: IEEE Conference Guidelines (Markdown, CSV, LaTeX, and Word-compatible HTML)  
**Dataset**: `ds_nexus_v11` ($N=100$: DEV=70, VAL=15, TEST=15)  
**Package Status**: RESULTS FREEZE (100% Reconciled Master Data)

---

## 1. Directory Structure

```
paper_tables/
├── publication_tables.md         # Full Markdown tables for GitHub / documentation
├── publication_tables.csv        # Master machine-readable CSV for all table series
├── publication_tables.tex        # IEEEtran-compliant LaTeX tables (booktabs/tabularx)
├── publication_tables_doc.html   # HTML document for direct copy-paste into Microsoft Word (.docx)
├── table_provenance_manifest.csv # Full traceability and audit log for each table
└── README_tables.md              # This documentation
```

---

## 2. Table Summary & Empirical Provenance

| Table | Title | Paper Section | Primary Source | Validation Status |
| :--- | :--- | :---: | :--- | :---: |
| **Table I** | Dataset Specification and Evaluation Protocol | Section IV-A | `ds_nexus_v11.json` | **VALID** |
| **Table II** | Candidate Context Retrieval Performance | Section IV-B | `e03_3_canonical_results_live.json` | **VALID** |
| **Table III** | Generation Grounding Comparison (Naive vs. Verified) | Section IV-D | `e04_1_aggregate_metrics.json` | **VALID** |
| **Table IV** | System Latency, Refinement Tradeoff, and Provenance | Section IV-C / IV-G / IV-H | `table_latency.csv` / `e07_statistics.json` / `e08_metrics.json` | **VALID** |
| **Table V** | Architectural Component Ablation Study | Section IV-I | `e10_aggregate_metrics.json` | **VALID** |
| **Table VI** | Error Taxonomy Analysis (TEST Split) | Section IV-J | `e11_summary_report.md` | **VALID** |

---

## 3. Strict Compliance Checks

- **Zero Experiment Reruns**: Built directly from frozen Results Freeze master records.
- **Canonical E03.3 Reconciled**: Recall@20 = 0.9500, Hit@20 = 1.0000; all 10 answerable TEST targets retrieved at $k=20$.
- **Grounding Significance**: McNemar test ($p=0.6831$) correctly documents no statistically significant improvement over Naive RAG.
- **Derived Timing Transparency**: A2 and A4 latencies are explicitly marked as **DERIVED** component decompositions.
- **Human Verification Ground Truth**: E05 is explicitly recorded as *NOT MEASURED* due to unavailable expert annotations.
