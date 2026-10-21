# IEEE Paper-Readiness Gate (V4 Canonical Assessment)

## 1. Readiness Determination: READY_WITH_EXPLICIT_LIMITATIONS

The experimental package for **ResearchNexusAI** has undergone forensic cross-validation. All hard-coded numbers and conflated denominators have been corrected. 

The paper may proceed to manuscript preparation provided that all negative findings, architectural trade-offs, and human-validation blockers are presented transparently.

---

## 2. Canonical Publication Claim Classification Matrix

| Claim ID | Paper Section / Topic | Canonical Metric / Finding | Gate Status | Authoritative Justification |
| :--- | :--- | :--- | :---: | :--- |
| **CLM-RET-01** | First-Stage Lexical Retrieval | BM25 Hit@20 = 0.6667 (10/15); Rec@20 = 1.0000 (10/10 answerable); MRR = 0.0759 | **APPROVED_FOR_PAPER** | Traced directly to `e01_raw_per_query.json`. Gold items placed at ranks 8-9. |
| **CLM-RET-02** | First-Stage Hybrid Retrieval | Hybrid RRF Hit@20 = 0.6667 (10/15); Rec@20 = 1.0000 (10/10 answerable); MRR = 0.0431 | **APPROVED_FOR_PAPER** | Traced to Module 01 canonical records. Supersedes invalid 11/15 claim. |
| **CLM-RET-03** | Neural Cross-Encoder Reranker | BGE Reranker MRR = 0.0480; Hit@20 = 0.6667 | **APPROVED_WITH_LIMITATION** | Modest rank promotion from 0.0431 to 0.0480. Synthetic 0.5444 / +47.7% claim is WITHDRAWN. |
| **CLM-RET-04** | Withdrawn Reranker Claim | Hybrid MRR = 0.3685, BGE MRR = 0.5444 (+47.7% relative gain) | **WITHDRAWN** | Synthetic constant with no lineage in raw files. Permanently blocked from paper. |
| **CLM-GRN-01** | Epistemic Abstention Behavior | Unanswerable Query Abstention = 5/5 (100.0%) | **APPROVED_FOR_PAPER** | Decoupled taxonomy confirms model reliably refused queries lacking evidence. |
| **CLM-GRN-02** | Factual Claim Entailment | Automated NLI Precision = 100.0% (4/4 naive, 3/3 verified) | **APPROVED_WITH_LIMITATION** | Valid under automated NLI model; small factual sample size (N=7 claims across test split). |
| **CLM-GRN-03** | Human Ground-Truth Grounding | Claim Verifier F1 / Human Inter-Annotator Kappa | **NOT_MEASURED / BLOCKED** | No genuine external human labels exist. Must be stated explicitly as future work. |
| **CLM-REP-01** | Citation Repair Efficacy | Citation Improvement = NOT OBSERVED; Applied Repairs = 0 | **APPROVED_FOR_PAPER** | 4 candidate repairs rejected due to 10-chunk ambiguity. Conservative safety preserved. |
| **CLM-REP-02** | Successful-Repair Safety | Post-repair factual accuracy of repaired citations | **NOT_MEASURED** | Denominator is 0 (0 applied repairs). Safety is mathematically NOT ESTIMABLE. |
| **CLM-REF-01** | Iterative Synthesis Refinement | Net Grounding Gain = 0.0% (1 improved, 98 unchanged, 1 degraded; p=1.000) | **APPROVED_FOR_PAPER** | E07.1 confirms iterative refinement introduces +106% latency penalty with no gain. |
| **CLM-XAI-01** | Local Provenance Tracking | Claim-to-Evidence & Citation-to-Evidence Completeness = 100% | **APPROVED_WITH_LIMITATION** | Valid under automated audit protocol verification; does not establish human readability. |
| **CLM-LAT-01** | Component vs E2E Latency | Hybrid p50 = 6.56 ms; BGE p50 = 531.41 ms; Request Mean = 12.12 s | **APPROVED_FOR_PAPER** | Component latencies clearly separated from complete request end-to-end latency. |
| **CLM-MOD-01** | Generator Model Version | E04 (gemini-2.5-flash) vs E04.1 (gemini-3.5-flash-lite) | **APPROVED_WITH_LIMITATION** | Model evolution documented as an internal-validity threat. |
