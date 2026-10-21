# Section IV Compact Publication Metric Table

This table aggregates the primary publication-facing empirical findings for Section IV across architectural groups, fully reconciled against canonical E03.3 live candidate retrieval.

| Architectural Group | Evaluated Condition | Primary Metric | Value | Latency (p50 / Mean) | Statistical Significance | Source Artifact |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **A. Benchmark** | `ds_nexus_v11` ($N=100$) | Queries (DEV / VAL / TEST) | 70 / 15 / 15 | — | Frozen Benchmark | `ds_nexus_v11.json` |
| **B. First-Stage Retrieval** | BM25 Lexical | MRR / Hit@5 (TEST) | 0.0759 / 0.0000 | 0.69 ms (p50) | Baseline | `table_e01_test_results.csv` |
| | Dense Chroma | MRR / Hit@5 (TEST) | 0.0000 / 0.0000 | 13.51 ms (p50) | Baseline | `table_e01_test_results.csv` |
| | Hybrid RRF (Canonical) | Recall@5 / Recall@10 (ALL) | 0.2700 / 0.5700 | 6.56 ms (p50) | Canonical Live E03.3 | `e03_3_canonical_results_live.json` |
| | Hybrid RRF (Canonical) | Recall@20 / Hit@20 (ALL) | 0.9500 / 1.0000 | 7.83 ms (p50) | Canonical Live E03.3 | `e03_3_canonical_results_live.json` |
| | Hybrid RRF (Canonical) | Recall@20 / Hit@20 (TEST) | 1.0000 / 1.0000 | 8.11 ms (p50) | Canonical Live E03.3 | `e03_3_canonical_results_live.json` |
| **C. Reranking** | Genuine BGE Cross-Encoder | Invocations / Bypass Count | 100 / 0 | 531.41 ms (p50) | 100% Genuine Execution | `table_latency.csv` |
| | Hybrid + BGE | Hit@5 (TEST) | 0.0000 | 535.06 ms (p50 stage) | Context-bounded | `table_e02_test_results.csv` |
| **D. Generation Grounding** | Naive RAG | CSR / UCR (ALL) | 0.0533 / 0.9467 | 4,659 ms (p50) | McNemar $p = 0.6831$ | `e04_1_aggregate_metrics.json` |
| | Verified RAG | CSR / UCR (ALL) | 0.0350 / 0.9650 | 4,899 ms (p50) | (Not Significant) | `e04_1_aggregate_metrics.json` |
| **E. Claim Verification** | Human-Grounded Evaluation | Accuracy / F1 | *NOT MEASURED* | — | Blocked (E05 human GT) | `e05_status` |
| **F. Citation Repair** | CitationRepair Loop | Attempts / Success Rate | 191 / 0.0% | 0.16 ms (p50 loop) | Conservative matching | `e06_1_summary_report.md` |
| **G. Iterative Refinement** | Iterative Loop (1–2 passes) | Degraded / Unchanged / Improved | 1 / 98 / 1 | 11,065 ms (p50, 2.2x) | Permutation $p = 1.000$ | `e07_statistics.json` |
| **H. Provenance (XAI)** | Full Trace Chain Audit | Complete / Valid Links | 100% (202/202) | — | Automated Protocol Audit | `e08_metrics.json` |
| **I. Component Ablations** | A0 Full Pipeline | CSR / Mean Latency | 0.0333 / 12,656 ms | Direct Live Execution | Authoritative E07-B | `e10_aggregate_metrics.json` |
| | A1 Minus Iteration | CSR / Mean Latency | 0.0350 / 5,691 ms | Direct Live Execution | Authoritative E04.1 | `e10_aggregate_metrics.json` |
| | A3 Naive RAG Baseline | CSR / Mean Latency | 0.0533 / 5,767 ms | Direct Live Execution | Verification & Repair OFF | `e10_aggregate_metrics.json` |
| **J. Error Taxonomy** | TEST Failure Breakdown ($N=15$) | Candidate Pool Miss / Retrieval Miss | 0 (0.0%) / 0 (0.0%) | — | Multi-Label (98 events) | `e11_summary_report.md` |
| | | Unsupported / Missing Citation | 28 (100%) / 28 (100%) | — | Context Distraction | `e11_summary_report.md` |
