import json
import os
import csv
import hashlib

def rebuild_results_freeze_canonical():
    print("Rebuilding Results Freeze Package with Canonical E03.3 & Reconciled E11...")
    freeze_dir = "research_artifacts/results_freeze"
    os.makedirs(freeze_dir, exist_ok=True)
    
    records = []
    
    def add_rec(exp_id, exp_name, status, split, n, config, metric, val, unit,
                stat_test="N/A", p_val="N/A", ci_l="N/A", ci_u="N/A",
                source="", pub_status="VALID", limits="", section="Section IV"):
        records.append({
            "experiment_id": exp_id,
            "experiment_name": exp_name,
            "status": status,
            "dataset": "ds_nexus_v11",
            "split": split,
            "N": n,
            "configuration": config,
            "metric": metric,
            "value": val,
            "unit": unit,
            "statistical_test": stat_test,
            "p_value": p_val,
            "ci_lower": ci_l,
            "ci_upper": ci_u,
            "source_artifact": source,
            "artifact_hash": "RECORDED_IN_MANIFEST",
            "publication_status": pub_status,
            "limitations": limits,
            "paper_section": section
        })

    # 1. DATASET
    add_rec("DATASET", "Dataset Specification", "VALID", "ALL", 100, "Frozen ds_nexus_v11", "Total Queries", 100, "count", pub_status="FROZEN", section="Section IV-A")
    add_rec("DATASET", "Dataset Specification", "VALID", "DEV", 70, "Frozen ds_nexus_v11", "Development Queries", 70, "count", pub_status="FROZEN", section="Section IV-A")
    add_rec("DATASET", "Dataset Specification", "VALID", "VAL", 15, "Frozen ds_nexus_v11", "Validation Queries", 15, "count", pub_status="FROZEN", section="Section IV-A")
    add_rec("DATASET", "Dataset Specification", "VALID", "TEST", 15, "Frozen ds_nexus_v11", "Test Queries", 15, "count", pub_status="FROZEN", limits="TEST N=15 limits high statistical power; descriptive analysis primary.", section="Section IV-A")

    # 2. E01 RETRIEVAL BASELINES (TEST N=15)
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B1_Dense", "MRR", 0.0, "score", source="table_e01_test_results.csv", section="Section IV-B")
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B1_Dense", "Hit@5", 0.0, "rate", source="table_e01_test_results.csv", section="Section IV-B")
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B1_Dense", "Latency_p50", 13.51, "ms", source="table_e01_test_results.csv", section="Section IV-B")
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B2_BM25", "MRR", 0.0759, "score", source="table_e01_test_results.csv", section="Section IV-B")
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B2_BM25", "Hit@5", 0.0, "rate", source="table_e01_test_results.csv", section="Section IV-B")
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B2_BM25", "Latency_p50", 0.69, "ms", source="table_e01_test_results.csv", section="Section IV-B")
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B3_Hybrid_RRF", "MRR", 0.0, "score", source="table_e01_test_results.csv", section="Section IV-B")
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B3_Hybrid_RRF", "Hit@5", 0.0, "rate", source="table_e01_test_results.csv", section="Section IV-B")
    add_rec("E01", "Retrieval Baselines", "VALID", "TEST", 15, "B3_Hybrid_RRF", "Latency_p50", 7.76, "ms", source="table_e01_test_results.csv", section="Section IV-B")

    # 3. E02 BGE RERANKING
    add_rec("E02", "BGE Cross-Encoder Reranking", "VALID", "TEST", 15, "B4_Hybrid_BGE", "MRR", 0.0, "score", source="table_e02_test_results.csv", section="Section IV-C")
    add_rec("E02", "BGE Cross-Encoder Reranking", "VALID", "TEST", 15, "B4_Hybrid_BGE", "Hit@5", 0.0, "rate", source="table_e02_test_results.csv", section="Section IV-C")
    add_rec("E02", "BGE Cross-Encoder Reranking", "VALID", "ALL", 100, "B4_Hybrid_BGE", "Genuine_Invocations", 100, "count", source="table_latency.csv", limits="BGE reranker preserves top-20 context; cannot rescue items absent from pre-rerank pool.", section="Section IV-C")

    # 4. E03.3 AUTHORITATIVE CANONICAL LIVE CANDIDATE RECALL
    # Source: research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_2_canonical/e03_3_canonical_results_live.json
    # ALL:
    add_rec("E03.3", "Candidate Context Recall", "VALID", "ALL", 100, "B3_Hybrid_RRF", "Recall@5", 0.2700, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "ALL", 100, "B3_Hybrid_RRF", "Recall@10", 0.5700, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "ALL", 100, "B3_Hybrid_RRF", "Recall@20", 0.9500, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "ALL", 100, "B3_Hybrid_RRF", "Recall@50", 1.0000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "ALL", 100, "B3_Hybrid_RRF", "Hit@5", 0.3000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "ALL", 100, "B3_Hybrid_RRF", "Hit@10", 0.6200, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "ALL", 100, "B3_Hybrid_RRF", "Hit@20", 1.0000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "ALL", 100, "B3_Hybrid_RRF", "Hit@50", 1.0000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    # Splits:
    add_rec("E03.3", "Candidate Context Recall", "VALID", "DEV", 70, "B3_Hybrid_RRF", "Recall@20", 1.0000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "DEV", 70, "B3_Hybrid_RRF", "Hit@20", 1.0000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "VAL", 15, "B3_Hybrid_RRF", "Recall@20", 0.6667, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "VAL", 15, "B3_Hybrid_RRF", "Hit@20", 1.0000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "TEST", 15, "B3_Hybrid_RRF", "Recall@20", 1.0000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")
    add_rec("E03.3", "Candidate Context Recall", "VALID", "TEST", 15, "B3_Hybrid_RRF", "Hit@20", 1.0000, "rate", source="e03_3_canonical_results_live.json", section="Section IV-B")

    # 5. E04.1 NAIVE VS VERIFIED RAG GENERATION
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Naive_RAG", "CSR", 0.0533, "rate", ci_l=0.0133, ci_u=0.1000, source="e04_1_aggregate_metrics.json", section="Section IV-D")
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Verified_RAG", "CSR", 0.0350, "rate", ci_l=0.0100, ci_u=0.0750, source="e04_1_aggregate_metrics.json", section="Section IV-D")
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Naive_RAG", "UCR", 0.9467, "rate", ci_l=0.9000, ci_u=0.9867, source="e04_1_aggregate_metrics.json", section="Section IV-D")
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Verified_RAG", "UCR", 0.9650, "rate", ci_l=0.9250, ci_u=0.9900, source="e04_1_aggregate_metrics.json", section="Section IV-D")
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Naive_RAG", "CP", 0.0600, "score", source="e04_1_aggregate_metrics.json", section="Section IV-D")
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Verified_RAG", "CP", 0.0400, "score", source="e04_1_aggregate_metrics.json", section="Section IV-D")
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Naive_vs_Verified", "McNemar_Test", 0.1667, "stat", stat_test="McNemar", p_val=0.6831, source="e04_1_statistical_tests.json", limits="No statistically significant grounding improvement over Naive RAG on this benchmark.", section="Section IV-D")
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Naive_RAG", "Latency_Mean", 5767.46, "ms", source="e04_1_aggregate_metrics.json", section="Section IV-D")
    add_rec("E04.1", "Generation Evaluation", "VALID", "ALL", 100, "Verified_RAG", "Latency_Mean", 5691.35, "ms", source="e04_1_aggregate_metrics.json", section="Section IV-D")

    # 6. E05 HUMAN VERIFIER EVALUATION
    add_rec("E05", "Human Ground-Truth Evaluation", "BLOCKED", "ALL", 0, "Human_Annotation", "Precision_Recall_F1", "NOT_MEASURED", "N/A", pub_status="NOT_MEASURED", limits="Blocked due to unavailability of human ground-truth annotations.", section="Section IV-E")

    # 7. E06.1 CITATION REPAIR
    add_rec("E06.1", "Citation Repair", "VALID", "ALL", 100, "CitationRepair", "Opportunities", 191, "count", source="e06_1_summary_report.md", section="Section IV-F")
    add_rec("E06.1", "Citation Repair", "VALID", "ALL", 100, "CitationRepair", "Attempts", 191, "count", source="e06_1_summary_report.md", section="Section IV-F")
    add_rec("E06.1", "Citation Repair", "VALID", "ALL", 100, "CitationRepair", "Successful_Repairs", 0, "count", source="e06_1_summary_report.md", limits="Under evaluated context and conservative matching policy, no opportunity satisfied repair criterion.", section="Section IV-F")
    add_rec("E06.1", "Citation Repair", "VALID", "ALL", 100, "CitationRepair", "Success_Rate", 0.0, "rate", source="e06_1_summary_report.md", section="Section IV-F")
    add_rec("E06.1", "Citation Repair", "VALID", "ALL", 202, "CitationRepair", "Latency_p50", 0.16, "ms", source="e06_1_latency_results.json", section="Section IV-F")

    # 8. E07.1 ITERATIVE REFINEMENT
    add_rec("E07.1", "Iterative Refinement", "VALID", "ALL", 100, "Refinement_Quality", "Improved_Queries", 1, "count", source="e07_1_summary_report.md", section="Section IV-G")
    add_rec("E07.1", "Iterative Refinement", "VALID", "ALL", 100, "Refinement_Quality", "Unchanged_Queries", 98, "count", source="e07_1_summary_report.md", section="Section IV-G")
    add_rec("E07.1", "Iterative Refinement", "VALID", "ALL", 100, "Refinement_Quality", "Degraded_Queries", 1, "count", source="e07_1_summary_report.md", section="Section IV-G")
    add_rec("E07.1", "Iterative Refinement", "VALID", "ALL", 100, "Refinement_Quality", "Delta_CSR", -0.0017, "delta", stat_test="Exact Paired Permutation", p_val=1.0, ci_l=-0.015, ci_u=0.010, source="e07_statistics.json", limits="Substantial latency increase (2.2x) with no statistically significant grounding benefit.", section="Section IV-G")
    add_rec("E07.1", "Iterative Refinement", "VALID", "ALL", 100, "Iteration_ON", "Latency_Mean", 12655.70, "ms", source="e07_latency_results.json", section="Section IV-G")
    add_rec("E07.1", "Iterative Refinement", "VALID", "ALL", 100, "Iteration_OFF", "Latency_Mean", 5691.35, "ms", source="e07_latency_results.json", section="Section IV-G")

    # 9. E08 XAI PROVENANCE EVALUATION
    add_rec("E08", "XAI Provenance Audit", "VALID", "ALL", 202, "Automated_Audit", "Trace_Completeness", 1.0, "rate", source="e08_metrics.json", limits="Represents automated audit protocol verification; not subjective human explainability.", section="Section IV-H")
    add_rec("E08", "XAI Provenance Audit", "VALID", "ALL", 202, "Automated_Audit", "Claim_to_Evidence_Accuracy", 1.0, "rate", source="e08_metrics.json", section="Section IV-H")
    add_rec("E08", "XAI Provenance Audit", "VALID", "ALL", 202, "Automated_Audit", "Citation_to_Evidence_Accuracy", 1.0, "rate", source="e08_metrics.json", section="Section IV-H")
    add_rec("E08", "XAI Provenance Audit", "VALID", "ALL", 202, "Automated_Audit", "Offset_Resolution_Accuracy", 1.0, "rate", source="e08_metrics.json", section="Section IV-H")
    add_rec("E08", "XAI Provenance Audit", "VALID", "ALL", 202, "Automated_Audit", "Online_Provenance", "NOT_APPLICABLE", "N/A", source="e08_online_provenance_results.json", section="Section IV-H")

    # 10. E09 DISAGGREGATED LATENCY
    add_rec("E09", "Disaggregated Latency", "VALID", "ALL", 100, "Hybrid_Retrieval", "Latency_p50", 6.56, "ms", source="final_latency_analysis.json", section="Section IV-I")
    add_rec("E09", "Disaggregated Latency", "VALID", "ALL", 100, "Hybrid_Retrieval", "Latency_p95", 19.12, "ms", source="final_latency_analysis.json", section="Section IV-I")
    add_rec("E09", "Disaggregated Latency", "VALID", "ALL", 100, "Pure_BGE_Inference", "Latency_p50", 531.41, "ms", source="final_latency_analysis.json", section="Section IV-I")
    add_rec("E09", "Disaggregated Latency", "VALID", "ALL", 100, "Pure_BGE_Inference", "Latency_p95", 4246.05, "ms", source="final_latency_analysis.json", section="Section IV-I")
    add_rec("E09", "Disaggregated Latency", "VALID", "ALL", 100, "Total_Hybrid_BGE_Stage", "Latency_p50", 535.06, "ms", source="final_latency_analysis.json", section="Section IV-I")
    add_rec("E09", "Disaggregated Latency", "VALID", "ALL", 100, "Total_Hybrid_BGE_Stage", "Latency_p95", 4251.51, "ms", source="final_latency_analysis.json", section="Section IV-I")

    # 11. E10 COMPONENT ABLATION STUDY
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A0_Full", "CSR", 0.0333, "rate", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A0_Full", "Latency_Mean", 12655.70, "ms", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A1_Minus_Iteration", "CSR", 0.0350, "rate", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A1_Minus_Iteration", "Latency_Mean", 5691.35, "ms", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A2_Minus_Citation_Repair", "CSR", 0.0533, "rate", source="e10_aggregate_metrics.json", limits="Derived decomposed timing from A0 minus CitationRepair stage.", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A2_Minus_Citation_Repair", "Latency_Mean", 12610.70, "ms", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A3_Naive_RAG", "CSR", 0.0533, "rate", source="e10_aggregate_metrics.json", limits="Combined verification-and-repair pipeline removal.", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A3_Naive_RAG", "Latency_Mean", 5767.46, "ms", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A4_Minus_BGE", "CSR", 0.0333, "rate", source="e10_aggregate_metrics.json", limits="Derived decomposed timing from A0 minus BGE stage.", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A4_Minus_BGE", "Latency_Mean", 12124.29, "ms", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A5_Dense_Only", "CSR", 0.0, "rate", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A5_Dense_Only", "Latency_Mean", 8.46, "ms", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A6_BM25_Only", "CSR", 0.0333, "rate", source="e10_aggregate_metrics.json", section="Section IV-J")
    add_rec("E10", "Component Ablation", "VALID", "ALL", 100, "A6_BM25_Only", "Latency_Mean", 0.98, "ms", source="e10_aggregate_metrics.json", section="Section IV-J")

    # 12. E11 RECONCILED ERROR TAXONOMY (TEST N=15)
    # Source: e11_category_counts.json (reconciled with canonical E03.3)
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 15, "Multi_Label_Taxonomy", "RETRIEVAL_MISS", 0, "count", source="e11_category_counts.json", limits="0 at k=20; all 15 TEST queries achieve Hit@20=1.0 in canonical E03.3 candidate pool.", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 15, "Multi_Label_Taxonomy", "CANDIDATE_POOL_MISS", 0, "count", source="e11_category_counts.json", limits="0 at k=20; all gold targets present in canonical top-20 candidate pool.", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 15, "Multi_Label_Taxonomy", "RERANKING_ERROR", 0, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 15, "Multi_Label_Taxonomy", "EVIDENCE_SELECTION_ERROR", 0, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 28, "Multi_Label_Taxonomy", "UNSUPPORTED_CLAIM", 28, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 28, "Multi_Label_Taxonomy", "CONTRADICTED_CLAIM", 0, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 0, "Multi_Label_Taxonomy", "WRONG_CITATION", 0, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 28, "Multi_Label_Taxonomy", "MISSING_CITATION", 28, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "BLOCKED", "TEST", 0, "Multi_Label_Taxonomy", "VERIFICATION_FALSE_POSITIVE", "NOT_MEASURED", "N/A", pub_status="NOT_MEASURED", limits="Unmeasurable without human ground truth (E05 blocked).", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "BLOCKED", "TEST", 0, "Multi_Label_Taxonomy", "VERIFICATION_FALSE_NEGATIVE", "NOT_MEASURED", "N/A", pub_status="NOT_MEASURED", limits="Unmeasurable without human ground truth (E05 blocked).", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 27, "Multi_Label_Taxonomy", "CITATION_REPAIR_FAILURE", 27, "count", source="e11_category_counts.json", limits="27/27 attempts failed; 1 record pre-supported and unattempted.", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 15, "Multi_Label_Taxonomy", "ITERATION_FAILURE", 15, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 15, "Multi_Label_Taxonomy", "ONLINE_RETRIEVAL_FAILURE", 0, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 28, "Multi_Label_Taxonomy", "XAI_PROVENANCE_FAILURE", 0, "count", source="e11_category_counts.json", section="Section IV-K")
    add_rec("E11", "Error Taxonomy", "VALID", "TEST", 15, "Multi_Label_Taxonomy", "Total_Categorized_Events", 98, "count", source="e11_summary_report.md", section="Section IV-K")

    print(f"Total frozen master records compiled: {len(records)}")
    
    # Write master files
    with open(f"{freeze_dir}/results_freeze_master.json", "w") as f:
        json.dump(records, f, indent=2)
        
    keys = list(records[0].keys())
    with open(f"{freeze_dir}/results_freeze_master.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
        
    md_content = ["# Authoritative Results Freeze Master Table",
                  "**Dataset**: `ds_nexus_v11` (N=100: DEV=70, VAL=15, TEST=15)",
                  "**Package Status**: FROZEN (Reconciled with Canonical E03.3 Live Candidate Recall)", "",
                  "| Experiment | Name | Split | N | Configuration | Metric | Value | Unit | Stat Test (p-val) | 95% CI | Limitations |",
                  "| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |"]
    for r in records:
        stat_str = f"{r['statistical_test']} ({r['p_value']})" if r['statistical_test'] != 'N/A' else "N/A"
        ci_str = f"[{r['ci_lower']}, {r['ci_upper']}]" if r['ci_lower'] != 'N/A' else "N/A"
        md_content.append(f"| {r['experiment_id']} | {r['experiment_name']} | {r['split']} | {r['N']} | {r['configuration']} | {r['metric']} | **{r['value']}** | {r['unit']} | {stat_str} | {ci_str} | {r['limitations']} |")
        
    with open(f"{freeze_dir}/results_freeze_master.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

    # Paper Metric Table
    paper_table_md = """# Section IV Compact Publication Metric Table

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
"""
    with open(f"{freeze_dir}/paper_metric_table.md", "w", encoding="utf-8") as f:
        f.write(paper_table_md)

    # Claim Safety Register
    claim_register = [
        {
            "claim_id": "CLM-001",
            "claim": "ResearchNexus provides complete and correct local provenance tracing from generated claims back to exact source text chunks.",
            "evidence": "E08 automated provenance audit evaluated 202 claims across 100 queries, achieving 100% Trace Completeness, Claim-to-Evidence Accuracy, and Citation-to-Evidence Accuracy.",
            "status": "SUPPORTED_WITH_LIMITATION",
            "limitations": "Valid under automated audit protocol verification; does not establish subjective human interpretability."
        },
        {
            "claim_id": "CLM-002",
            "claim": "Verified RAG significantly outperforms Naive RAG in claim factual grounding and citation precision.",
            "evidence": "E04.1 measured Naive CSR=0.0533 vs Verified CSR=0.0350 (McNemar p=0.6831). Differences are not statistically significant.",
            "status": "INVALID_DO_NOT_USE",
            "limitations": "Empirically refuted on ds_nexus_v11. Paper must state that Verified RAG did not demonstrate significant grounding improvement over Naive RAG."
        },
        {
            "claim_id": "CLM-003",
            "claim": "Iterative refinement substantially improves answer factual accuracy over single-pass generation.",
            "evidence": "E07.1 evaluated 100 queries: 1 improved, 98 unchanged, 1 degraded (permutation test p=1.000).",
            "status": "INVALID_DO_NOT_USE",
            "limitations": "Empirically refuted on ds_nexus_v11. Iteration added 2.2x latency without factual quality recovery."
        },
        {
            "claim_id": "CLM-004",
            "claim": "BGE Cross-Encoder reranking executes genuinely across all queries without bypass.",
            "evidence": "E02 and E09 verified 100/100 genuine BGE cross-encoder invocations with p50 latency of 531.41 ms (p95 of 4,246.05 ms).",
            "status": "SUPPORTED",
            "limitations": "Reranking operates within candidate context pools; lower-ranked gold documents amid distractors challenge generative synthesis."
        },
        {
            "claim_id": "CLM-005",
            "claim": "Citation repair universally fails across all retrieval settings.",
            "evidence": "E06.1 observed 191 repair attempts with 0 successful repairs on ds_nexus_v11.",
            "status": "SUPPORTED_WITH_LIMITATION",
            "limitations": "Finding is specific to evaluated context pool and conservative exact matching policy; do not claim universal failure across all domains."
        },
        {
            "claim_id": "CLM-006",
            "claim": "Automated claim verifier achieves 95%+ precision against human expert annotators.",
            "evidence": "Experiment E05 is blocked due to lack of human ground-truth annotations.",
            "status": "NOT_MEASURED",
            "limitations": "Human evaluation was not conducted. No human agreement or verifier F1 metrics exist."
        },
        {
            "claim_id": "CLM-007",
            "claim": "Downstream RAG generation failures predominantly follow a context-distraction and grounding-deficit propagation pattern.",
            "evidence": "E11 multi-label error taxonomy analysis revealed that despite Hit@20=1.0 at candidate level, lower ranking placement (ranks 15-17) resulted in 28 unsupported claims, 28 missing citations, 27 repair failures, and 15 iteration exhaustions.",
            "status": "SUPPORTED",
            "limitations": "Characterizes observed empirical propagation across components; not a claim of universal deterministic causality."
        }
    ]
    with open(f"{freeze_dir}/publication_claim_register.json", "w") as f:
        json.dump(claim_register, f, indent=2)
        
    claim_md = ["# Publication Claim Safety Register",
                "| Claim ID | Proposed Paper Claim | Empirical Evidence | Claim Safety Status | Limitations & Publication Constraints |",
                "| :--- | :--- | :--- | :---: | :--- |"]
    for c in claim_register:
        claim_md.append(f"| **{c['claim_id']}** | {c['claim']} | {c['evidence']} | `{c['status']}` | {c['limitations']} |")
    with open(f"{freeze_dir}/publication_claim_register.md", "w", encoding="utf-8") as f:
        f.write("\n".join(claim_md))

    # Invalid Data Register
    invalid_data_md = """# Invalid Data & Superseded Results Register

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
"""
    with open(f"{freeze_dir}/invalid_data_register.md", "w", encoding="utf-8") as f:
        f.write(invalid_data_md)

    # Limitations Register
    limitations_md = """# Publication Limitations Register

The following limitations are grounded in verified artifacts and must be transparently acknowledged in Section V:

1. **Test Set Statistical Power ($N=15$)**:
   The test split of `ds_nexus_v11` comprises 15 items. While ideal for exhaustive forensic analysis (e.g., E11), it limits high statistical power for small effect sizes. Analysis is primarily descriptive.

2. **Absence of Human-Grounded Ground Truth (E05 Blocked)**:
   Experiment E05 remains blocked due to the unavailability of human expert annotations. Claim verification accuracy is audited deterministically and semantically against LLM-based NLI, but human-annotator agreement metrics are not reported.

3. **Automated Scope of XAI Provenance (E08)**:
   The 100% provenance chain accuracy reflects automated graph link resolution and exact text offset matching within the canonical database. It does not measure cognitive interpretability or human user trust.

4. **Policy-Specific Citation Repair Outcomes (E06.1)**:
   The 0% success rate in CitationRepair reflects a conservative exact-string/semantic matching policy in a closed retrieval corpus. It should not be generalized as a fundamental limitation of the concept.

5. **No Grounding Improvement in Verified Pipeline (E04.1 / E07.1)**:
   Neither Verified RAG over Naive RAG (McNemar $p=0.6831$) nor Iterative Refinement over Single-Pass ($p=1.000$) demonstrated statistically significant grounding gains on this benchmark, despite a 2.2x latency overhead.

6. **Context Distraction Despite High Recall (E03.3 / E11)**:
   While canonical candidate recall achieves Hit@20 = 1.0000 on TEST, gold documents are placed at lower ranks (15–17) amid distractor chunks, challenging LLM synthesis and leading to refusal/ungrounded outputs.

7. **Derived Latency Decompositions (E10)**:
   Ablation conditions A2 (No Citation Repair) and A4 (No BGE) latency values are derived mathematically via component decomposition from A0, rather than independent wall-clock runs.
"""
    with open(f"{freeze_dir}/limitations_register.md", "w", encoding="utf-8") as f:
        f.write(limitations_md)

    # Conclusions
    conclusions_md = """# Authoritative Results Freeze Conclusions

1. **High Candidate Context Recall**: Under canonical live evaluation (E03.3), hybrid RRF achieves high candidate context recall (Recall@20 = 0.9500, Hit@20 = 1.0000 on ALL; Hit@20 = 1.0000 on TEST), successfully capturing gold documents within the top-20 pool.
2. **Context Distraction & Generator Bounds**: Although gold items are retrieved in top-20, their placement at lower ranks (ranks 15–17) amid distractors prevents the generator from synthesizing grounded answers, leading to refusal statements and ungrounded assertions.
3. **Verified RAG Performance**: On the evaluated benchmark, the multi-stage verified pipeline did not demonstrate a statistically significant grounding or citation improvement over Naive RAG (McNemar $p = 0.6831$).
4. **Iterative Refinement Trade-off**: Enabling iterative refinement increased wall-clock generation latency by 2.2x (mean 12,656 ms vs 5,691 ms) with no measurable grounding recovery (98 unchanged, 1 improved, 1 degraded, $p = 1.000$).
5. **Citation Repair Constraints**: Under conservative replacement policies in closed candidate pools, citation repair resolved 0 of 191 repair opportunities because replacement evidence did not satisfy strict matching thresholds.
6. **Disaggregated Neural Latency**: Genuine cross-encoder neural reranking contributes a median of 531.41 ms (p95 of 4,246.05 ms), representing the largest pre-generation latency component.
7. **Complete Architectural Provenance**: Under automated graph verification, the ResearchNexus explanation layer achieves 100% end-to-end provenance integrity (202/202 claims) connecting claims, citations, chunks, and retrieval scores.
8. **Empirical Grounding Integrity**: Scientific literature synthesis benchmarking requires strict separation between automated provenance tracing and human evaluation, with transparent reporting of non-significant improvements.
"""
    with open(f"{freeze_dir}/results_freeze_conclusions.md", "w", encoding="utf-8") as f:
        f.write(conclusions_md)

    # Manifest
    manifest = {}
    for filename in sorted(os.listdir(freeze_dir)):
        if filename != "results_freeze_manifest.json":
            filepath = os.path.join(freeze_dir, filename)
            with open(filepath, "rb") as f:
                manifest[filename] = hashlib.sha256(f.read()).hexdigest()
                
    with open(f"{freeze_dir}/results_freeze_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Results Freeze successfully rebuilt! Compiled {len(records)} frozen records.")

if __name__ == '__main__':
    rebuild_results_freeze_canonical()
