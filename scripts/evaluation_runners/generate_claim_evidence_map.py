import os, sys, csv

TARGET_DIR = 'evaluation/publication_audit_v2/final_manuscript'
os.makedirs(TARGET_DIR, exist_ok=True)

claim_map_rows = [
    {
        "paper_section": "Abstract & Section IV-B",
        "claim_text_in_paper": "On answerable test queries, hybrid retrieval achieves 10/10 Recall@20 (Hit@20 = 0.6667 across all 15 test items).",
        "canonical_metric_value": "Recall@20 = 1.0000 (10/10 answerable); Hit@20 = 0.6667 (10/15 all)",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/canonical_retrieval_metrics.csv",
        "raw_source_file": "evaluation/module_01/metrics/paper_level_metrics.json",
        "audit_verification_status": "APPROVED_FOR_PAPER"
    },
    {
        "paper_section": "Abstract & Section IV-B",
        "claim_text_in_paper": "Neural cross-encoder reranking produces a modest improvement, increasing MRR from 0.0431 to 0.0480.",
        "canonical_metric_value": "MRR_all: B3=0.0431, B4=0.0480; MRR_ans: B3=0.0647, B4=0.0720",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/canonical_retrieval_metrics.csv",
        "raw_source_file": "evaluation/module_01/metrics/paper_level_metrics.json",
        "audit_verification_status": "APPROVED_WITH_LIMITATION"
    },
    {
        "paper_section": "Abstract & Section IV-B",
        "claim_text_in_paper": "BM25 all 10 answerable test items hit gold paper at rank 8 or 9; Hit@5 = 0.0, Hit@10 = 0.6667, MRR = 0.0759 (all 15) / 0.1139 (10 answerable).",
        "canonical_metric_value": "Hit@5 = 0.0; Hit@10 = 0.6667; MRR_all = 0.0759; MRR_ans = 0.1139",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/canonical_retrieval_metrics.csv",
        "raw_source_file": "research_artifacts/retrieval_evaluation/v11/e01/raw/e01_raw_per_query.json",
        "audit_verification_status": "APPROVED_FOR_PAPER"
    },
    {
        "paper_section": "Abstract & Section IV-C",
        "claim_text_in_paper": "Automated NLI achieves 100% precision across evaluated positive factual assertions (4/4 naive, 3/3 verified).",
        "canonical_metric_value": "Precision = 1.0000 (4/4 naive, 3/3 verified factual claims)",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/canonical_grounding_metrics.json",
        "raw_source_file": "evaluation/module_02/revision_01/reclassified_claims.json",
        "audit_verification_status": "APPROVED_WITH_LIMITATION"
    },
    {
        "paper_section": "Abstract & Section IV-C",
        "claim_text_in_paper": "The system correctly refuses 100% (5/5) of unanswerable queries under decoupled epistemic taxonomy.",
        "canonical_metric_value": "Abstention Accuracy = 1.0000 (5/5 unanswerable items refused)",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/canonical_grounding_metrics.json",
        "raw_source_file": "evaluation/module_02/revision_01/corrected_metrics.json",
        "audit_verification_status": "APPROVED_FOR_PAPER"
    },
    {
        "paper_section": "Section IV-C & Section V",
        "claim_text_in_paper": "Human ground-truth validation is formally blocked and not measured; no human agreement metrics exist.",
        "canonical_metric_value": "HUMAN_VALIDATION_BLOCKED / NOT_MEASURED",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/paper_readiness_gate.md",
        "raw_source_file": "research_artifacts/results_freeze/publication_claim_register.json (CLM-006)",
        "audit_verification_status": "NOT_MEASURED"
    },
    {
        "paper_section": "Abstract & Section IV-D",
        "claim_text_in_paper": "Citation repair achieved 0 applied repairs (20.0% coverage pre- and post-repair) due to 10-chunk candidate ambiguity; safety not estimable.",
        "canonical_metric_value": "Coverage = 20.0%; Applied = 0; Rejected = 4; Safety = NOT_ESTIMABLE",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/paper_readiness_gate.md",
        "raw_source_file": "evaluation/module_03/analysis/repair_metrics.json",
        "audit_verification_status": "APPROVED_FOR_PAPER"
    },
    {
        "paper_section": "Abstract & Section IV-D",
        "claim_text_in_paper": "Iterative refinement yielded 1 improved, 98 unchanged, 1 degraded query (net gain 0.0%, p=1.000).",
        "canonical_metric_value": "1 improved, 98 unchanged, 1 degraded; permutation p=1.000",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/paper_readiness_gate.md",
        "raw_source_file": "research_artifacts/generation_evaluation/v11/e07_iteration/e07_1_audit/e07_1_corrected_summary_report.md",
        "audit_verification_status": "APPROVED_FOR_PAPER"
    },
    {
        "paper_section": "Section IV-E",
        "claim_text_in_paper": "Stage latency breakdown: BM25 p50=0.69ms, Dense p50=13.51ms, Hybrid p50=6.56ms, BGE p50=531.41ms, Combined stage p50=535.06ms.",
        "canonical_metric_value": "BM25 p50=0.69ms, Dense p50=13.51ms, Hybrid p50=6.56ms, BGE p50=531.41ms, Stage p50=535.06ms",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/canonical_latency_results.csv",
        "raw_source_file": "research_artifacts/retrieval_evaluation/v11/final_latency_analysis.json",
        "audit_verification_status": "APPROVED_FOR_PAPER"
    },
    {
        "paper_section": "Section IV-E",
        "claim_text_in_paper": "Complete request latency mean without iteration is 5,691.35ms (p50=4,899.07ms); with iteration mean is 12,655.70ms (p50=11,064.67ms).",
        "canonical_metric_value": "No iter mean=5.69s (p50=4.90s); With iter mean=12.66s (p50=11.06s)",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/canonical_latency_results.csv",
        "raw_source_file": "research_artifacts/generation_evaluation/v11/e07_iteration/e07_summary_report.md",
        "audit_verification_status": "APPROVED_FOR_PAPER"
    },
    {
        "paper_section": "Section III & Section V",
        "claim_text_in_paper": "Historical E04 evaluated gemini-2.5-flash, E04.1 evaluated gemini-3.5-flash-lite, and production backend defaults to gemini-2.5-flash.",
        "canonical_metric_value": "E04: gemini-2.5-flash; E04.1: gemini-3.5-flash-lite; Backend: gemini-2.5-flash",
        "source_v4_artifact": "evaluation/publication_audit_v2/v4_reconciliation/canonical_experiment_configurations.csv",
        "raw_source_file": "research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_config.json",
        "audit_verification_status": "APPROVED_WITH_LIMITATION"
    }
]

out_csv = os.path.join(TARGET_DIR, 'manuscript_claim_evidence_map.csv')
with open(out_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(claim_map_rows[0].keys()))
    writer.writeheader()
    writer.writerows(claim_map_rows)

print(f"Generated {out_csv} with {len(claim_map_rows)} mapped quantitative statements.")
