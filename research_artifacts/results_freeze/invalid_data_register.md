# Invalid Data & Superseded Results Register

This register explicitly catalogues superseded, invalid, or legacy data that must **NEVER** be cited in the conference paper.

| Invalid Metric / Finding | Legacy Source | Reason for Invalidation | Authoritative Replacement |
| :--- | :--- | :--- | :--- |
| **Synthetic / v10 Retrieval Metrics** (e.g., 91% Hit@5, 0.860 MRR) | Benchmark v10 / synthetic scripts | Hardcoded, synthetic or ungrounded evaluations | Authoritative E01 & Canonical E03.3 on `ds_nexus_v11` |
| **Stale e03_aggregate_results.json** (Hit@20 = 0.05 on ALL) | Stale early aggregate run | Flattened/truncated candidate pool evaluation | Canonical Live E03.3: Recall@20 = 0.9500, Hit@20 = 1.0000 (ALL) |
| **Top-10 Forensic Deficit in E11** (Candidate Pool Miss = 10/15) | Stale top-10 slice in `independent_test_forensics.csv` | Measured top-10 slice instead of canonical k=20 candidate pool | Reconciled E11: Candidate Pool Miss = 0 at k=20 (Hit@20 = 1.0000) |
| **BGE Bypass Latency** (~0.004 ms) | Early uninstrumented mock runs | BGE model was bypassed or cached; failed to execute neural inference | Genuine BGE wall-clock: p50 = 531.41 ms, p95 = 4,246.05 ms (E09) |
| **"77 Quality Regressions"** in Iterative Refinement | Legacy E07 heuristic | Conflated text modification with factual regression | Corrected E07.1: 1 improved, 98 unchanged, 1 degraded |
| **A5 / A6 Latencies ≈ 12,650 ms** in Ablation | Early E10 runner timing inheritance | Copied full pipeline generation timer into retrieval-only baselines | Corrected E10: A5 = 8.46 ms, A6 = 0.98 ms |
| **"100% Human Explainability"** | Early E08 draft phrasing | Conflated automated graph traversal verification with human user trust | Corrected E08: "100% provenance mapping correctness under automated audit" |
| **"Verification-Only" Ablation for A3** | Early E10 label | A3 ablated both verification AND citation repair simultaneously | Corrected E10: "Combined verification-and-repair pipeline removal" |
