# Forensic Experimental Validation Report (V3)
**Package Under Audit**: `evaluation/publication_audit_v2/`
**Target Dataset**: `ds_nexus_v11` (N=100: DEV=70, VAL=15, TEST=15)
**Audit Mandate**: Full forensic audit separating documentation generated from constants from metrics calculated from raw experimental records.

---

## 1. Executive Summary & Audit Verdict

This forensic audit inspected the scripts that created the v2 audit package (`generate_p0_governance.py`, `generate_p0_artifacts.py`, `generate_p1_artifacts.py`, and `generate_p2_p3_p4_artifacts.py`) and traced every numerical claim back to underlying raw JSON and CSV experimental outputs.

### Critical Audit Findings:
1. **Separation of Constant Documentation from Raw Data**:
   - Several tables in `publication_audit_v2/` were written directly as hard-coded string literals inside Python generation scripts rather than calculated dynamically from raw files.
   - Specifically, the reported **Hybrid MRR of 0.3685** and **BGE Reranker MRR of 0.5444 (+47.7% relative improvement)** do not exist in any raw experimental record. In canonical Module 01 records, Hybrid RRF MRR is **0.0431** and BGE Reranker MRR is **0.0480**. The synthetic figures have been formally **WITHDRAWN** from publication approval.
2. **Resolution of the 11/15 Hybrid Hit Paradox**:
   - The reported claim of **11/15 hits** on the test set is mathematically impossible under true ground truth because `ds_nexus_v11` contains exactly **10 answerable queries** (items 86-95) and **5 unanswerable queries** (items 96-100) with empty gold paper sets.
   - Raw Module 01 records confirm that Hybrid RRF achieved **10/15 (0.6667) Hit@20**, and **10/10 (1.0000) Recall@20** on answerable queries. The 11/15 claim was an artifact and has been corrected to **10/15 (0.6667)**.
3. **BM25 Hit@20 vs Recall@20 Lineage Verified**:
   - In raw BM25 test records (`e01_raw_per_query.json`), all 10 answerable test items retrieved the gold paper at rank 8 or 9.
   - Consequently, **Hit@5 is 0.0000 (0/15)**, **Hit@10 is 0.6667 (10/15)**, and **Hit@20 is 0.6667 (10/15)**.
   - The mean MRR across all 15 test items (treating unanswerables as 0.0) is **0.075926**. Across the 10 answerable items, mean MRR is **0.113889**. Both values are mathematically proven and reconciled.
4. **Grounding Evaluation Clarified**:
   - In `reclassified_claims.json`, exactly 56 claims are evaluated. Epistemic taxonomy classifies 49 as epistemic abstentions/negative findings and 7 as positive factual assertions.
   - Automated NLI precision on positive factual claims is **100.0% (4/4 naive, 3/3 verified)**.
   - Epistemic abstention accuracy on unanswerable queries is **100.0% (5/5)**.
   - Human ground truth validation remains strictly **`HUMAN_VALIDATION_BLOCKED / NOT_MEASURED`**.
5. **Citation Repair Reality Confirmed**:
   - Raw logs in Module 03 confirm baseline citation coverage of **20.0% (1/5 factual claims)**.
   - For the 4 uncited claims in `item_v11_092`, the repair module identified matches that spanned **10 chunks simultaneously**, correctly triggering conservative ambiguity rejection.
   - **Applied repairs = 0**. **Post-repair coverage = 20.0%**. Successful-repair safety is **NOT ESTIMABLE** (0/0).

---

## 2. Forensic Investigation Summaries

### Investigation 1: Retrieval Metric Consistency
- **Test Set Composition**: Verified in `test_manifest.json` and `benchmark_items.json`.
  - Items `item_v11_086` to `item_v11_090`: SYNTHESIS (Answerable, 1 gold paper each).
  - Items `item_v11_091` to `item_v11_095`: ADVERSARIAL (Answerable, 1 gold paper each).
  - Items `item_v11_096` to `item_v11_100`: UNANSWERABLE (0 gold papers, 0 gold chunks).
- **BM25 Performance**:
  - Answerable queries: 10/10 hit gold paper at ranks 8-9. Hit@20 = 1.0 (10/10). Recall@20 = 1.0 (10/10).
  - All test queries: Hit@20 = 0.6667 (10/15). Hit@5 = 0.0000 (0/15). MRR = 0.0759 (all 15) / 0.1139 (10 answerable).
- **Hybrid Performance**:
  - Hit@20 is 10/15 (0.6667). The claim of 11/15 is withdrawn as mathematically invalid.

### Investigation 2: Reranker Ablation
- The claimed numbers (Hybrid MRR=0.3685, BGE MRR=0.5444, +47.7% gain) were produced as static string constants in `generate_p2_p3_p4_artifacts.py`.
- In canonical raw records (`evaluation/module_01/metrics/paper_level_metrics.json`), Hybrid RRF achieved MRR = 0.0431, and BGE Reranker achieved MRR = 0.0480. In early E02 runs, neither configuration promoted items into top-5 (MRR@5 = 0.0000).
- The +47.7% claim is withdrawn from the publication package.

### Investigation 3: Grounding & Abstention
- Analyzed all 56 claim entries in `reclassified_claims.json`.
- Factual claims: 7 total across systems (4 evaluated in naive RAG, 3 in verified RAG). All evaluated factual claims were supported by retrieved text under automated NLI (precision = 1.0000).
- Epistemic abstentions: 30 appropriate abstentions + 19 insufficient evidence findings.
- All 5 unanswerable queries correctly abstained from hallucinating factual answers (100% abstention rate).
- Automated only; human evaluation remains BLOCKED.

### Investigation 4: Citation Repair
- Traced across `repair_metrics.json` and `citation_metrics.json`.
- Total factual claims eligible for citation: 5. Already cited at baseline: 1 (20.0% coverage).
- Uncited factual claims: 4 (all in `item_v11_092`).
- Candidate matching: All 4 candidates matched 10 retrieved chunks equally.
- Repair action: 4 rejected due to ambiguity; 0 applied.
- Status locked: Citation improvement NOT OBSERVED; Repair effectiveness NOT DEMONSTRATED; Safety NOT ESTIMABLE.

### Investigation 5: Model & Latency Provenance
- Config inspection revealed model drift:
  - E04 used `gemini-2.5-flash` (temp=0.0).
  - E04.1 used `gemini-3.5-flash-lite` (temp=0.0).
  - Backend production code uses `gemini-2.5-flash`.
- Latency percentiles: Component p50 values must not be summed. Disaggregated measurements:
  - Hybrid retrieval p50: 6.56 ms.
  - BGE reranking p50: 531.41 ms.
  - Total hybrid+reranking p50: 535.06 ms.
  - End-to-end pipeline mean latency: 12.12 s.

---

## 3. Authoritative Validated Status Table

| Priority | Task / Claim | Forensic Status | Supporting Raw File | Verified Value | Next Required Action |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **P0** | BM25 TEST Hit@20 & Recall | **PASS** | `e01_raw_per_query.json` | Hit@20 = 0.6667 (10/15); Rec@20 = 1.0 (10/10) | Include explicit answerable denominator note |
| **P0** | BM25 TEST MRR | **PASS** | `e01_raw_per_query.json` | MRR = 0.0759 (all 15) / 0.1139 (10 answerable) | Report both denominators |
| **P0** | Hybrid Hit@20 (Claimed 11/15) | **FAIL_CORRECTED** | `paper_level_metrics.json` | Hit@20 = 0.6667 (10/15) | Withdraw 11/15; update to 10/15 |
| **P0** | Model Version Provenance | **FAIL_DOCUMENTED** | `e04_config.json`, `e04_1_config.json` | E04 (gemini-2.5-flash) vs E04.1 (gemini-3.5-flash-lite) | Document model drift in threats to validity |
| **P0** | Latency Boundary Decomposition | **PASS_CORRECTED** | `table_latency.csv`, `final_latency_analysis.json` | Component p50s non-additive; End-to-end mean = 12.12s | Report true end-to-end alongside component p50s |
| **P1** | Factual Grounding Precision | **PASS_CORRECTED** | `reclassified_claims.json`, `corrected_metrics.json` | 100% (4/4 naive, 3/3 verified) | Label strictly as automated NLI result |
| **P1** | Epistemic Abstention Accuracy | **PASS** | `corrected_metrics.json` | 100% (5/5 unanswerable refused) | Publish as verified abstention behavior |
| **P1** | Human Ground-Truth Validation | **BLOCKED** | `human_evaluation_status.md` | NOT_MEASURED (0 human labels) | Retain blinded package for future rater study |
| **P2** | Reranker MRR 0.3685 -> 0.5444 | **FAIL_WITHDRAWN** | Synthetic constant in script | CANONICAL: B3=0.0431, B4=0.0480 | Withdraw 0.3685, 0.5444, and +47.7% claims |
| **P3** | Citation Repair Safety & Counts | **PASS** | `repair_metrics.json`, `citation_metrics.json` | 0 applied; 4 rejected ambiguity; Safety NOT ESTIMABLE | Publish conservative negative result |
| **P3** | Iterative Refinement Net Gain | **PASS** | `publication_claim_register.json` (CLM-003) | 1 improved, 98 unchanged, 1 degraded (p=1.000) | State refinement added latency without gain |
| **P4** | Master Results Lineage & Hashes | **PASS** | `metric_lineage.csv` | Full SHA-256 traceable lineage | Lock verified metrics in IEEE manuscript |
