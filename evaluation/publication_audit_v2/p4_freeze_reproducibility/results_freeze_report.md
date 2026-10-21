# Master Results Freeze & Publication Evidence Report

## 1. Executive Summary
This document establishes the final, authoritative, reconciled experimental results for ResearchNexusAI across all research phases P0 through P4.
All historical discrepancies (e.g., BM25 Hit@20 vs Recall@20, Gemini version labeling, latency boundaries, and refusal penalties) are resolved with mathematical and empirical precision.

## 2. Reconciled Publication Results Table
| Evaluation Dimension | Metric | Baseline / Naive | Verified Pipeline | Scientific Verdict |
| :--- | :--- | :---: | :---: | :--- |
| **First-Stage Lexical** | Paper Hit@20 (TEST) | 0.6667 | 0.6667 | High candidate recall (10/10 answerable) |
| **First-Stage Dense** | Paper MRR (TEST) | 0.3111 | 0.3111 | Semantic synonym capture |
| **Hybrid RRF (k=60)** | Paper Hit@20 / MRR | 0.7333 / 0.3685 | 0.7333 / 0.3685 | Maximizes pool coverage |
| **Cross-Encoder Rerank** | Paper MRR@10 | 0.3685 | **0.5444** | +47.7% relative rank promotion |
| **Factual Claim Grounding**| Entailment Precision | 1.0000 | 1.0000 | 100% precision on true factual claims |
| **Epistemic Abstention** | Refusal on Unanswerable | 1.0000 | 1.0000 | 5/5 unanswerable queries correctly refused |
| **Citation Coverage** | Valid Citation Rate | 20.0% | 20.0% | Repair improvement NOT OBSERVED |
| **Citation Repair** | Applied Safe Repairs | 0 | 0 | Repair effectiveness NOT DEMONSTRATED |
| **Refinement Loop** | Grounding Net Gain | 0.0% | 0.0% | Negligible gain; +106% latency penalty |
| **Human Validation** | Inter-Annotator Kappa | N/A | N/A | HUMAN_VALIDATION_BLOCKED |
