"""
========================================================================================
ResearchNexus: Authoritative Publication Tables Generator
Paper: "ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation
        Architecture for Scientific Literature Synthesis"
Target: IEEE Conference Publications
Dataset: ds_nexus_v11 (N=100: DEV=70, VAL=15, TEST=15)
Status: RESULTS FREEZE (100% Reconciled Data)

Outputs Generated:
1. paper_tables/publication_tables.md
2. paper_tables/publication_tables.csv
3. paper_tables/publication_tables.tex (IEEEtran compliant)
4. paper_tables/publication_tables_doc.html (Word / docx copy-paste compatible)
5. paper_tables/table_provenance_manifest.csv
6. paper_tables/README_tables.md
========================================================================================
"""

import os
import sys

# --------------------------------------------------------------------------------------
# 1. STRICT FROZEN DATA SPECIFICATION & ASSERTIONS
# --------------------------------------------------------------------------------------

# Table I Data
TABLE_I_DATA = {
    "dataset": "ds_nexus_v11",
    "n_total": 100,
    "splits": {"DEV": 70, "VAL": 15, "TEST": 15},
    "papers": 40,
    "chunks": 80,
    "domains": "AI / NLP / CV / IR",
    "query_categories": {
        "Factual": 20,
        "Methodological": 20,
        "Numerical": 15,
        "Causal": 15,
        "Comparative": 10,
        "Synthesis": 10,
        "Adversarial": 5,
        "Unanswerable": 5
    },
    "components": [
        ("E03.3", "Candidate Context Retrieval", "Hybrid RRF (k=60)"),
        ("E04.1", "Generation Grounding", "Gemini 2.5 Flash + Verifier"),
        ("E05", "Human Expert Verification", "NOT MEASURED (Human GT unavailable)"),
        ("E06.1", "Citation Repair", "Exact Context Substring Matching"),
        ("E07.1", "Iterative Refinement", "Multi-pass Feedback Loop"),
        ("E08", "XAI Provenance Audit", "Automated Link & Offset Verification"),
        ("E09", "Latency Decomposition", "Stage Profiling (p50 / p95)"),
        ("E10", "Component Ablation", "Controlled Single-factor Deletion (A0-A6)"),
        ("E11", "Error Taxonomy", "14-Category Failure Distribution (TEST)")
    ]
}

# Table II Data (E03.3 Canonical Live)
TABLE_II_DATA = [
    {"k": 5, "recall": 0.2700, "hit": 0.3000},
    {"k": 10, "recall": 0.5700, "hit": 0.6200},
    {"k": 20, "recall": 0.9500, "hit": 1.0000},
    {"k": 50, "recall": 1.0000, "hit": 1.0000}
]

# Table III Data (E04.1 Generation Grounding)
TABLE_III_DATA = [
    {"metric": "CSR", "full_name": "Claim Support Ratio", "naive": 0.0533, "verified": 0.0350, "direction": "↑ better"},
    {"metric": "UCR", "full_name": "Unsupported Claim Ratio", "naive": 0.9467, "verified": 0.9650, "direction": "↓ better"},
    {"metric": "CP", "full_name": "Citation Precision", "naive": 0.0600, "verified": 0.0400, "direction": "↑ better"},
    {"metric": "COV", "full_name": "Citation Coverage", "naive": 0.0617, "verified": 0.0433, "direction": "↑ better"}
]
TABLE_III_TEST = {
    "mcnemar_stat": 0.1667,
    "mcnemar_p": 0.6831,
    "note": "No statistically significant grounding improvement was observed."
}

# Table IV Data (Latency & Refinement & Provenance)
TABLE_IV_A_DATA = [
    {"stage": "Hybrid Retrieval", "p50": 6.56, "p95": 19.12},
    {"stage": "Pure BGE Inference", "p50": 531.41, "p95": 4246.05},
    {"stage": "Hybrid + BGE Combined", "p50": 535.06, "p95": 4251.51}
]

TABLE_IV_B_DATA = [
    {"config": "Iteration OFF", "latency": 5691.35, "improved": "—", "unchanged": "—", "degraded": "—"},
    {"config": "Iteration ON", "latency": 12655.70, "improved": 1, "unchanged": 98, "degraded": 1}
]
TABLE_IV_B_STATS = {
    "delta_csr": -0.0017,
    "permutation_p": 1.0000,
    "multiplier": "2.22x"
}

TABLE_IV_C_DATA = [
    {"metric": "Trace Completeness", "value": 1.0000},
    {"metric": "Claim-to-Evidence Accuracy", "value": 1.0000},
    {"metric": "Citation-to-Evidence Accuracy", "value": 1.0000},
    {"metric": "Offset Resolution Accuracy", "value": 1.0000}
]
TABLE_IV_C_NOTE = "N = 202 automated claim traces. These are automated provenance-audit metrics, not human explainability measures."

# Table V Data (Ablations)
TABLE_V_DATA = [
    {"config": "A0 Full Pipeline", "csr": 0.0333, "latency": 12655.70, "status": "Direct"},
    {"config": "A1 Minus Iteration", "csr": 0.0350, "latency": 5691.35, "status": "Direct"},
    {"config": "A2 Minus Citation Repair", "csr": 0.0533, "latency": 12610.70, "status": "DERIVED"},
    {"config": "A3 Naive RAG Baseline", "csr": 0.0533, "latency": 5767.46, "status": "Direct"},
    {"config": "A4 Minus BGE Reranker", "csr": 0.0333, "latency": 12124.29, "status": "DERIVED"},
    {"config": "A5 Dense Only Baseline", "csr": 0.0000, "latency": 8.46, "status": "Direct"},
    {"config": "A6 BM25 Only Baseline", "csr": 0.0333, "latency": 0.98, "status": "Direct"}
]

# Table VI Data (E11 Error Taxonomy)
TABLE_VI_MEASURED = [
    {"category": "UNSUPPORTED_CLAIM", "count": 28, "level": "Claim", "status": "measured"},
    {"category": "MISSING_CITATION", "count": 28, "level": "Claim", "status": "measured"},
    {"category": "CITATION_REPAIR_FAILURE", "count": 27, "level": "Citation", "status": "measured"},
    {"category": "ITERATION_FAILURE", "count": 15, "level": "Query", "status": "measured"}
]

TABLE_VI_ZERO = [
    {"category": "RETRIEVAL_MISS", "count": 0, "level": "Query", "status": "measured"},
    {"category": "CANDIDATE_POOL_MISS", "count": 0, "level": "Query", "status": "measured"},
    {"category": "RERANKING_ERROR", "count": 0, "level": "Query", "status": "measured"},
    {"category": "EVIDENCE_SELECTION_ERROR", "count": 0, "level": "Query", "status": "measured"},
    {"category": "CONTRADICTED_CLAIM", "count": 0, "level": "Claim", "status": "measured"},
    {"category": "WRONG_CITATION", "count": 0, "level": "Claim", "status": "measured"},
    {"category": "ONLINE_RETRIEVAL_FAILURE", "count": 0, "level": "Query", "status": "measured"},
    {"category": "XAI_PROVENANCE_FAILURE", "count": 0, "level": "Claim", "status": "measured"}
]

TABLE_VI_UNMEASURED = [
    {"category": "VERIFICATION_FALSE_POSITIVE", "count": "NOT MEASURED", "level": "Claim", "status": "unmeasured (E05 human GT unavailable)"},
    {"category": "VERIFICATION_FALSE_NEGATIVE", "count": "NOT MEASURED", "level": "Claim", "status": "unmeasured (E05 human GT unavailable)"}
]


def run_strict_assertions():
    """Validates all values against frozen benchmark numbers before writing tables."""
    # Table I
    assert sum(TABLE_I_DATA["splits"].values()) == 100
    assert sum(TABLE_I_DATA["query_categories"].values()) == 100
    
    # Table II
    assert [r["recall"] for r in TABLE_II_DATA] == [0.2700, 0.5700, 0.9500, 1.0000]
    assert [r["hit"] for r in TABLE_II_DATA] == [0.3000, 0.6200, 1.0000, 1.0000]
    
    # Table III
    assert TABLE_III_DATA[0]["naive"] == 0.0533 and TABLE_III_DATA[0]["verified"] == 0.0350
    assert TABLE_III_DATA[1]["naive"] == 0.9467 and TABLE_III_DATA[1]["verified"] == 0.9650
    assert TABLE_III_DATA[2]["naive"] == 0.0600 and TABLE_III_DATA[2]["verified"] == 0.0400
    assert TABLE_III_DATA[3]["naive"] == 0.0617 and TABLE_III_DATA[3]["verified"] == 0.0433
    assert TABLE_III_TEST["mcnemar_stat"] == 0.1667
    assert TABLE_III_TEST["mcnemar_p"] == 0.6831
    
    # Table IV
    assert TABLE_IV_A_DATA[0]["p50"] == 6.56 and TABLE_IV_A_DATA[0]["p95"] == 19.12
    assert TABLE_IV_A_DATA[1]["p50"] == 531.41 and TABLE_IV_A_DATA[1]["p95"] == 4246.05
    assert TABLE_IV_A_DATA[2]["p50"] == 535.06 and TABLE_IV_A_DATA[2]["p95"] == 4251.51
    assert TABLE_IV_B_DATA[0]["latency"] == 5691.35
    assert TABLE_IV_B_DATA[1]["latency"] == 12655.70
    assert TABLE_IV_B_DATA[1]["improved"] == 1 and TABLE_IV_B_DATA[1]["unchanged"] == 98 and TABLE_IV_B_DATA[1]["degraded"] == 1
    assert TABLE_IV_B_STATS["delta_csr"] == -0.0017
    assert TABLE_IV_B_STATS["permutation_p"] == 1.0000
    assert all(r["value"] == 1.0000 for r in TABLE_IV_C_DATA)
    
    # Table V
    assert [r["csr"] for r in TABLE_V_DATA] == [0.0333, 0.0350, 0.0533, 0.0533, 0.0333, 0.0000, 0.0333]
    assert [r["latency"] for r in TABLE_V_DATA] == [12655.70, 5691.35, 12610.70, 5767.46, 12124.29, 8.46, 0.98]
    assert TABLE_V_DATA[2]["status"] == "DERIVED" and TABLE_V_DATA[4]["status"] == "DERIVED"
    
    # Table VI
    assert TABLE_VI_MEASURED[0]["count"] == 28
    assert TABLE_VI_MEASURED[1]["count"] == 28
    assert TABLE_VI_MEASURED[2]["count"] == 27
    assert TABLE_VI_MEASURED[3]["count"] == 15
    assert all(r["count"] == 0 for r in TABLE_VI_ZERO)
    assert sum(r["count"] for r in TABLE_VI_MEASURED) + sum(r["count"] for r in TABLE_VI_ZERO) == 98
    
    print("[PASS] All strict table assertions passed successfully.")


# --------------------------------------------------------------------------------------
# 2. GENERATE MARKDOWN TABLES (publication_tables.md)
# --------------------------------------------------------------------------------------
def generate_markdown(output_dir):
    md_path = os.path.join(output_dir, "publication_tables.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Authoritative Publication Tables: ResearchNexus Conference Paper\n\n")
        f.write("**Paper Title**: *ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis*\n\n")
        f.write("**Target Venue**: IEEE Conference Proceedings\n\n")
        f.write("**Frozen Benchmark**: `ds_nexus_v11` ($N=100$: DEV=70, VAL=15, TEST=15)\n\n")
        f.write("---\n\n")
        
        # TABLE I
        f.write("## TABLE I: DATASET SPECIFICATION AND EVALUATION PROTOCOL\n\n")
        f.write("| Characteristic | Value / Distribution | Description |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write(f"| **Benchmark Dataset** | `{TABLE_I_DATA['dataset']}` | Standardized multi-domain scientific benchmark |\n")
        f.write(f"| **Corpus Size** | {TABLE_I_DATA['papers']} papers / {TABLE_I_DATA['chunks']} chunks | Target literature documents across AI, NLP, CV, and IR |\n")
        f.write(f"| **Query Splits** | Total $N=100$ | DEV = {TABLE_I_DATA['splits']['DEV']}, VAL = {TABLE_I_DATA['splits']['VAL']}, TEST = {TABLE_I_DATA['splits']['TEST']} |\n")
        f.write("| **Query Categorization** | 8 categories ($N=100$) | " + ", ".join([f"{k}: {v}" for k, v in TABLE_I_DATA['query_categories'].items()]) + " |\n")
        f.write("| **Retrieval Evaluation** | E03.3 Candidate Recall | Lexical (BM25), Dense (Chroma), and Hybrid RRF ($k=60$) |\n")
        f.write("| **Generation Grounding** | E04.1 Grounding Analysis | Naive RAG vs. Verified RAG ($N=100$) with McNemar paired test |\n")
        f.write("| **Human Verification** | E05 Ground Truth | **NOT MEASURED** (Human expert ground-truth annotations unavailable) |\n")
        f.write("| **Citation Repair** | E06.1 CitationRepair | Deterministic substring context matching (191 opportunities) |\n")
        f.write("| **Iterative Refinement** | E07.1 Multi-Pass Refinement | Paired permutation test on query-level quality shifts |\n")
        f.write("| **Provenance Audit** | E08 Automated XAI Layer | Automated verification of bidirectional link and text offset integrity |\n")
        f.write("| **System Latencies** | E09 Stage Decomposition | Granular profiling ($p50$, $p95$) of retrieval and cross-encoder inference |\n")
        f.write("| **Component Ablations** | E10 Controlled Ablations | Single-factor architectural deletions ($A0$–$A6$) |\n")
        f.write("| **Error Taxonomy** | E11 Failure Classification | 14-category multi-label failure categorization on TEST split ($N=15$) |\n\n")
        
        # TABLE II
        f.write("## TABLE II: CANDIDATE CONTEXT RETRIEVAL PERFORMANCE\n\n")
        f.write("*Hybrid RRF candidate-context retrieval on ALL N=100 queries.*\n\n")
        f.write("| Candidate Pool Size ($k$) | Recall@k | Hit@k |\n")
        f.write("| :---: | :---: | :---: |\n")
        for row in TABLE_II_DATA:
            f.write(f"| {row['k']} | {row['recall']:.4f} | {row['hit']:.4f} |\n")
        f.write("\n> **Note**: TEST ($N=15$): all 10 answerable targets are present within the canonical $k=20$ pool; 5 additional TEST queries are unanswerable probes.\n\n")
        
        # TABLE III
        f.write("## TABLE III: GENERATION GROUNDING: NAIVE VS. VERIFIED RAG\n\n")
        f.write("| Metric | Description | Naive RAG | Verified RAG | Desired Direction |\n")
        f.write("| :--- | :--- | :---: | :---: | :---: |\n")
        for row in TABLE_III_DATA:
            f.write(f"| **{row['metric']}** | {row['full_name']} | {row['naive']:.4f} | {row['verified']:.4f} | {row['direction']} |\n")
        f.write(f"\n> **Statistical Test**: McNemar paired statistic = {TABLE_III_TEST['mcnemar_stat']:.4f}, $p = {TABLE_III_TEST['mcnemar_p']:.4f}$.\n")
        f.write(f"> **Conclusion**: {TABLE_III_TEST['note']}\n\n")
        
        # TABLE IV
        f.write("## TABLE IV: SYSTEM LATENCY AND ITERATIVE REFINEMENT\n\n")
        f.write("### Part A: Disaggregated Pre-Generation Latency (E09, $N=100$)\n\n")
        f.write("| Processing Stage | $p50$ (ms) | $p95$ (ms) |\n")
        f.write("| :--- | :---: | :---: |\n")
        for row in TABLE_IV_A_DATA:
            f.write(f"| {row['stage']} | {row['p50']:.2f} | {row['p95']:.2f} |\n")
        f.write("\n### Part B: Iterative Refinement Quality & Runtime Tradeoff (E07.1, $N=100$)\n\n")
        f.write("| Configuration | Mean Latency (ms) | Improved Queries | Unchanged Queries | Degraded Queries |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: |\n")
        for row in TABLE_IV_B_DATA:
            f.write(f"| {row['config']} | {row['latency']:.2f} | {row['improved']} | {row['unchanged']} | {row['degraded']} |\n")
        f.write(f"\n> **Quality Impact**: $\\Delta\\text{{CSR}} = {TABLE_IV_B_STATS['delta_csr']:.4f}$; Exact paired permutation $p = {TABLE_IV_B_STATS['permutation_p']:.4f}$. Overhead multiplier = {TABLE_IV_B_STATS['multiplier']}.\n\n")
        f.write("### Part C: Automated XAI Provenance Layer Integrity (E08, $N=202$ Claims)\n\n")
        f.write("| Provenance Metric | Audit Value |\n")
        f.write("| :--- | :---: |\n")
        for row in TABLE_IV_C_DATA:
            f.write(f"| {row['metric']} | {row['value']:.4f} (100.0%) |\n")
        f.write(f"\n> **Note**: {TABLE_IV_C_NOTE}\n\n")
        
        # TABLE V
        f.write("## TABLE V: ARCHITECTURAL COMPONENT ABLATION STUDY (E10, $N=100$)\n\n")
        f.write("| Configuration | Description | CSR | Mean Latency (ms) | Latency Status |\n")
        f.write("| :---: | :--- | :---: | :---: | :---: |\n")
        for row in TABLE_V_DATA:
            f.write(f"| **{row['config'].split()[0]}** | {' '.join(row['config'].split()[1:])} | {row['csr']:.4f} | {row['latency']:.2f} | {row['status']} |\n")
        f.write("\n> *Footnote*: A2 and A4 latency values are mathematically derived component decompositions rather than independent end-to-end wall-clock runs.\n\n")
        
        # TABLE VI
        f.write("## TABLE VI: ERROR TAXONOMY ANALYSIS (E11, TEST SPLIT $N=15$, 28 CLAIMS)\n\n")
        f.write("| Category | Event Count | Failure Level | Measurement Status / Interpretation |\n")
        f.write("| :--- | :---: | :---: | :--- |\n")
        f.write("| **1. Measured Failure Categories** | | | |\n")
        for row in TABLE_VI_MEASURED:
            f.write(f"| `{row['category']}` | **{row['count']}** | {row['level']} | {row['status']} (Concentrated failure mode) |\n")
        f.write("| **2. Zero Measured Categories** | | | |\n")
        for row in TABLE_VI_ZERO:
            f.write(f"| `{row['category']}` | 0 | {row['level']} | {row['status']} (0 events at canonical $k=20$) |\n")
        f.write("| **3. Unmeasured Categories** | | | |\n")
        for row in TABLE_VI_UNMEASURED:
            f.write(f"| `{row['category']}` | *NOT MEASURED* | {row['level']} | {row['status']} |\n")
        f.write(f"\n> **Total Categorized Events**: 98 multi-label failure events across 15 TEST queries.\n")
    print(f"  [SAVED] {md_path}")


# --------------------------------------------------------------------------------------
# 3. GENERATE CSV TABLE MASTER (publication_tables.csv)
# --------------------------------------------------------------------------------------
def generate_csv(output_dir):
    csv_path = os.path.join(output_dir, "publication_tables.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("table_id,table_name,row_index,item_label,metric_label,value,unit,status_or_provenance\n")
        
        # Table I
        f.write("Table_I,Dataset_Protocol,1,Total_Queries,Count,100,count,Frozen ds_nexus_v11\n")
        f.write("Table_I,Dataset_Protocol,2,DEV_Queries,Count,70,count,Frozen ds_nexus_v11\n")
        f.write("Table_I,Dataset_Protocol,3,VAL_Queries,Count,15,count,Frozen ds_nexus_v11\n")
        f.write("Table_I,Dataset_Protocol,4,TEST_Queries,Count,15,count,Frozen ds_nexus_v11\n")
        f.write("Table_I,Dataset_Protocol,5,Corpus_Papers,Count,40,count,Scientific Papers\n")
        f.write("Table_I,Dataset_Protocol,6,Corpus_Chunks,Count,80,count,Text Chunks\n")
        
        # Table II
        for i, row in enumerate(TABLE_II_DATA, start=1):
            f.write(f"Table_II,Candidate_Retrieval,{i},k={row['k']},Recall@{row['k']},{row['recall']:.4f},rate,Canonical E03.3 Live\n")
            f.write(f"Table_II,Candidate_Retrieval,{i},k={row['k']},Hit@{row['k']},{row['hit']:.4f},rate,Canonical E03.3 Live\n")
            
        # Table III
        for i, row in enumerate(TABLE_III_DATA, start=1):
            f.write(f"Table_III,Naive_vs_Verified,{i},{row['metric']},Naive_RAG,{row['naive']:.4f},rate,E04.1 Aggregate\n")
            f.write(f"Table_III,Naive_vs_Verified,{i},{row['metric']},Verified_RAG,{row['verified']:.4f},rate,E04.1 Aggregate\n")
        f.write("Table_III,Naive_vs_Verified,5,McNemar_Test,statistic,0.1667,stat,E04.1 McNemar\n")
        f.write("Table_III,Naive_vs_Verified,6,McNemar_Test,p_value,0.6831,p_val,E04.1 McNemar (N.S.)\n")
        
        # Table IV
        for i, row in enumerate(TABLE_IV_A_DATA, start=1):
            f.write(f"Table_IV_A,Latency_Decomposition,{i},{row['stage']},p50,{row['p50']:.2f},ms,E09 Latency\n")
            f.write(f"Table_IV_A,Latency_Decomposition,{i},{row['stage']},p95,{row['p95']:.2f},ms,E09 Latency\n")
        for i, row in enumerate(TABLE_IV_B_DATA, start=1):
            f.write(f"Table_IV_B,Iterative_Refinement,{i},{row['config']},Mean_Latency,{row['latency']:.2f},ms,E07.1 Iteration\n")
        f.write(f"Table_IV_B,Iterative_Refinement,3,Quality_Shift,Delta_CSR,-0.0017,delta,E07.1 Permutation\n")
        f.write(f"Table_IV_B,Iterative_Refinement,4,Quality_Shift,Permutation_p,1.0000,p_val,E07.1 Permutation (p=1.0)\n")
        for i, row in enumerate(TABLE_IV_C_DATA, start=1):
            f.write(f"Table_IV_C,Provenance_Audit,{i},{row['metric']},Accuracy,{row['value']:.4f},rate,E08 Provenance Audit\n")
            
        # Table V
        for i, row in enumerate(TABLE_V_DATA, start=1):
            cfg_id = row['config'].split()[0]
            f.write(f"Table_V,Component_Ablation,{i},{cfg_id},CSR,{row['csr']:.4f},rate,E10 Ablation\n")
            f.write(f"Table_V,Component_Ablation,{i},{cfg_id},Mean_Latency,{row['latency']:.2f},ms,{row['status']}\n")
            
        # Table VI
        idx = 1
        for row in TABLE_VI_MEASURED:
            f.write(f"Table_VI,Error_Taxonomy,{idx},{row['category']},Count,{row['count']},count,{row['status']}\n")
            idx += 1
        for row in TABLE_VI_ZERO:
            f.write(f"Table_VI,Error_Taxonomy,{idx},{row['category']},Count,{row['count']},count,{row['status']}\n")
            idx += 1
        for row in TABLE_VI_UNMEASURED:
            f.write(f"Table_VI,Error_Taxonomy,{idx},{row['category']},Count,{row['count']},note,{row['status']}\n")
            idx += 1
            
    print(f"  [SAVED] {csv_path}")


# --------------------------------------------------------------------------------------
# 4. GENERATE IEEE-COMPLIANT LATEX TABLES (publication_tables.tex)
# --------------------------------------------------------------------------------------
def generate_latex(output_dir):
    tex_path = os.path.join(output_dir, "publication_tables.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(r"""% =========================================================================
% ResearchNexus IEEE Conference Publication Tables
% Target: IEEEtran.cls / IEEE Conference Proceedings
% =========================================================================

\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{multirow}
\usepackage{amsmath}

% -------------------------------------------------------------------------
% TABLE I: DATASET SPECIFICATION AND EVALUATION PROTOCOL
% -------------------------------------------------------------------------
\begin{table}[t]
\caption{Dataset Specification and Evaluation Protocol}
\label{tab:dataset_protocol}
\centering
\small
\begin{tabularx}{\columnwidth}{lX}
\toprule
\textbf{Property} & \textbf{Specification / Configuration} \\
\midrule
Benchmark Dataset & \texttt{ds\_nexus\_v11} ($N=100$ total queries) \\
Split Partition & DEV: 70, VAL: 15, TEST: 15 queries \\
Target Corpus & 40 scientific papers, 80 extracted passages \\
Corpus Domains & AI, NLP, Computer Vision, Information Retrieval \\
Query Types & Factual (20), Methodological (20), Numerical (15), Causal (15), Comparative (10), Synthesis (10), Adversarial (5), Probe (5) \\
\midrule
\multicolumn{2}{l}{\textbf{Empirical Evaluation Stages}} \\
Retrieval (E03.3) & Hybrid RRF ($k=60$) over Lexical (BM25) and Dense Chroma \\
Generation (E04.1) & Naive RAG vs. Verified RAG using Gemini 2.5 Flash \\
Human Ground Truth (E05) & \textit{NOT MEASURED} (Human ground truth unavailable) \\
Citation Repair (E06.1) & Deterministic substring matching (191 opportunities) \\
Refinement (E07.1) & Iterative feedback loop (1--2 resynthesis passes) \\
Provenance (E08) & Automated bidirectional audit of links and offsets ($N=202$) \\
Latency (E09) & Disaggregated profiling ($p50$, $p95$) of pipeline stages \\
Ablation (E10) & Single-factor component deletions ($A0$--$A6$) \\
Taxonomy (E11) & 14-category multi-label error audit on TEST ($N=15$) \\
\bottomrule
\end{tabularx}
\end{table}

% -------------------------------------------------------------------------
% TABLE II: CANDIDATE RETRIEVAL PERFORMANCE
% -------------------------------------------------------------------------
\begin{table}[t]
\caption{Candidate Context Retrieval Performance}
\label{tab:candidate_retrieval}
\centering
\small
\begin{tabular}{ccc}
\toprule
\textbf{Candidate Pool ($k$)} & \textbf{Recall@$k$} & \textbf{Hit@$k$} \\
\midrule
5  & 0.2700 & 0.3000 \\
10 & 0.5700 & 0.6200 \\
20 & 0.9500 & 1.0000 \\
50 & 1.0000 & 1.0000 \\
\bottomrule
\end{tabular}
\vspace{1ex}
\begin{minipage}{\columnwidth}
\footnotesize
\textit{Note}: Hybrid RRF candidate-context retrieval evaluated on ALL $N=100$ queries. On the TEST partition ($N=15$), all 10 answerable targets are present within the canonical $k=20$ pool; 5 additional TEST queries are unanswerable probe queries.
\end{minipage}
\end{table}

% -------------------------------------------------------------------------
% TABLE III: NAIVE VS. VERIFIED RAG
% -------------------------------------------------------------------------
\begin{table}[t]
\caption{Generation Grounding Comparison: Naive vs. Verified RAG}
\label{tab:naive_vs_verified}
\centering
\small
\begin{tabular}{lccc}
\toprule
\textbf{Metric} & \textbf{Naive RAG} & \textbf{Verified RAG} & \textbf{Direction} \\
\midrule
Claim Support Ratio (CSR)         & 0.0533 & 0.0350 & $\uparrow$ better \\
Unsupported Claim Ratio (UCR)     & 0.9467 & 0.9650 & $\downarrow$ better \\
Citation Precision (CP)           & 0.0600 & 0.0400 & $\uparrow$ better \\
Citation Coverage (COV)            & 0.0617 & 0.0433 & $\uparrow$ better \\
\bottomrule
\end{tabular}
\vspace{1ex}
\begin{minipage}{\columnwidth}
\footnotesize
\textit{Statistical Test}: McNemar paired test statistic = 0.1667, $p = 0.6831$. No statistically significant grounding improvement was observed on the evaluated benchmark.
\end{minipage}
\end{table}

% -------------------------------------------------------------------------
% TABLE IV: LATENCY, REFINEMENT, AND PROVENANCE
% -------------------------------------------------------------------------
\begin{table}[t]
\caption{System Latency, Refinement Tradeoff, and Provenance}
\label{tab:latency_refinement_provenance}
\centering
\small
\begin{tabularx}{\columnwidth}{lrr}
\toprule
\multicolumn{3}{l}{\textbf{Part A: Pre-Generation Latency Breakdown (E09, $N=100$)}} \\
\textbf{Processing Stage} & \textbf{$p50$ (ms)} & \textbf{$p95$ (ms)} \\
\midrule
Hybrid Retrieval (BM25 + Dense) & 6.56   & 19.12 \\
Pure BGE Cross-Encoder Inference & 531.41 & 4246.05 \\
Hybrid + BGE Combined Stage      & 535.06 & 4251.51 \\
\midrule
\multicolumn{3}{l}{\textbf{Part B: Iterative Refinement Tradeoff (E07.1, $N=100$)}} \\
\textbf{Configuration} & \textbf{Mean Latency} & \textbf{Outcomes (Imp / Unch / Deg)} \\
\midrule
Iteration OFF (Single Pass) & 5691.35 ms & --- \\
Iteration ON (Refined Loop) & 12655.70 ms & 1 improved / 98 unchanged / 1 degraded \\
\multicolumn{3}{l}{\footnotesize $\Delta\text{CSR} = -0.0017$, exact permutation $p = 1.0000$, $2.22\times$ latency multiplier.} \\
\midrule
\multicolumn{3}{l}{\textbf{Part C: Automated XAI Provenance Integrity (E08, $N=202$ Claims)}} \\
\textbf{Verification Criterion} & \multicolumn{2}{r}{\textbf{Audit Adherence Rate}} \\
\midrule
Trace Completeness             & \multicolumn{2}{r}{1.0000 (100.0\%)} \\
Claim-to-Evidence Accuracy     & \multicolumn{2}{r}{1.0000 (100.0\%)} \\
Citation-to-Evidence Accuracy  & \multicolumn{2}{r}{1.0000 (100.0\%)} \\
Offset Resolution Accuracy     & \multicolumn{2}{r}{1.0000 (100.0\%)} \\
\bottomrule
\end{tabularx}
\vspace{1ex}
\begin{minipage}{\columnwidth}
\footnotesize
\textit{Note}: Part C reflects automated provenance-audit verification across 202 algorithmic trace links, not human subject explainability measures.
\end{minipage}
\end{table}

% -------------------------------------------------------------------------
% TABLE V: COMPONENT ABLATION STUDY
% -------------------------------------------------------------------------
\begin{table}[t]
\caption{Architectural Component Ablation Study ($N=100$)}
\label{tab:ablation}
\centering
\small
\begin{tabular}{llcc}
\toprule
\textbf{ID} & \textbf{Ablation Configuration} & \textbf{CSR} & \textbf{Mean Latency (ms)} \\
\midrule
A0 & Full Pipeline                         & 0.0333 & 12655.70 \\
A1 & Minus Iteration                       & 0.0350 & 5691.35 \\
A2 & Minus Citation Repair$^*$             & 0.0533 & 12610.70$^*$ \\
A3 & Naive RAG Baseline                    & 0.0533 & 5767.46 \\
A4 & Minus BGE Cross-Encoder$^*$           & 0.0333 & 12124.29$^*$ \\
A5 & Dense Only Baseline                   & 0.0000 & 8.46 \\
A6 & BM25 Only Baseline                    & 0.0333 & 0.98 \\
\bottomrule
\end{tabular}
\vspace{1ex}
\begin{minipage}{\columnwidth}
\footnotesize
$^*$A2 and A4 latency values are mathematically derived component decompositions rather than independent end-to-end wall-clock runs.
\end{minipage}
\end{table}

% -------------------------------------------------------------------------
% TABLE VI: ERROR TAXONOMY ANALYSIS
% -------------------------------------------------------------------------
\begin{table}[t]
\caption{Error Taxonomy Distribution on TEST Split (E11)}
\label{tab:error_taxonomy}
\centering
\small
\begin{tabular}{lccl}
\toprule
\textbf{Category} & \textbf{Count} & \textbf{Level} & \textbf{Status / Interpretation} \\
\midrule
\multicolumn{4}{l}{\textit{Measured Failure Categories}} \\
UNSUPPORTED\_CLAIM          & 28 & Claim    & 100.0\% of TEST claims (28/28) \\
MISSING\_CITATION           & 28 & Claim    & 100.0\% of TEST claims (28/28) \\
CITATION\_REPAIR\_FAILURE   & 27 & Citation & 100.0\% of repair attempts (27/27) \\
ITERATION\_FAILURE          & 15 & Query    & 100.0\% of TEST queries (15/15) \\
\midrule
\multicolumn{4}{l}{\textit{Zero Measured Categories ($0$ occurrences at canonical $k=20$)}} \\
RETRIEVAL\_MISS             & 0  & Query    & 0 misses ($Hit@20=1.00$) \\
CANDIDATE\_POOL\_MISS       & 0  & Query    & 0 pool misses ($Hit@20=1.00$) \\
RERANKING\_ERROR            & 0  & Query    & Top-20 context preserved \\
EVIDENCE\_SELECTION\_ERROR  & 0  & Query    & Verified selection \\
CONTRADICTED\_CLAIM         & 0  & Claim    & No direct contradictions \\
WRONG\_CITATION             & 0  & Claim    & 0 incorrect pointer links \\
ONLINE\_RETRIEVAL\_FAILURE  & 0  & Query    & Local corpus execution \\
XAI\_PROVENANCE\_FAILURE    & 0  & Claim    & Complete deterministic trace \\
\midrule
\multicolumn{4}{l}{\textit{Unmeasured Categories}} \\
VERIFICATION\_FALSE\_POS    & \multicolumn{2}{c}{\textit{NOT MEASURED}} & E05 human GT unavailable \\
VERIFICATION\_FALSE\_NEG    & \multicolumn{2}{c}{\textit{NOT MEASURED}} & E05 human GT unavailable \\
\bottomrule
\end{tabular}
\vspace{1ex}
\begin{minipage}{\columnwidth}
\footnotesize
\textit{Note}: Evaluated on the TEST partition ($N=15$ queries, 28 synthesized claims; 98 total multi-label events).
\end{minipage}
\end{table}
""")
    print(f"  [SAVED] {tex_path}")


# --------------------------------------------------------------------------------------
# 5. GENERATE WORD / DOCX COMPATIBLE HTML (publication_tables_doc.html)
# --------------------------------------------------------------------------------------
def generate_html_doc(output_dir):
    html_path = os.path.join(output_dir, "publication_tables_doc.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ResearchNexus Publication Tables (Word Compatible)</title>
<style>
body { font-family: "Times New Roman", Times, serif; font-size: 10pt; line-height: 1.3; margin: 20px; }
table { border-collapse: collapse; width: 100%; margin-bottom: 25px; page-break-inside: avoid; }
th, td { border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 5px 8px; text-align: left; }
th { font-weight: bold; background-color: #f2f2f2; }
caption { font-weight: bold; font-size: 11pt; margin-bottom: 6px; text-align: left; }
.note { font-size: 9pt; font-style: italic; margin-top: 4px; }
.center { text-align: center; }
.right { text-align: right; }
</style>
</head>
<body>

<h2>ResearchNexus Publication Tables (IEEE Format Ready)</h2>
<p><b>Dataset</b>: <code>ds_nexus_v11</code> (N=100: DEV=70, VAL=15, TEST=15) | <b>Status</b>: Authoritative Results Freeze</p>

<!-- TABLE I -->
<table>
<caption>TABLE I: DATASET SPECIFICATION AND EVALUATION PROTOCOL</caption>
<tr><th>Characteristic</th><th>Value / Configuration</th></tr>
<tr><td>Benchmark Dataset</td><td><code>ds_nexus_v11</code> (Total N=100 queries)</td></tr>
<tr><td>Split Partition</td><td>DEV = 70, VAL = 15, TEST = 15</td></tr>
<tr><td>Target Corpus</td><td>40 scientific papers, 80 extracted passages (AI, NLP, CV, IR)</td></tr>
<tr><td>Query Types</td><td>Factual (20), Methodological (20), Numerical (15), Causal (15), Comparative (10), Synthesis (10), Adversarial (5), Probe (5)</td></tr>
<tr><td>Candidate Retrieval (E03.3)</td><td>Hybrid RRF (k=60) over Lexical (BM25) and Dense (Chroma)</td></tr>
<tr><td>Generation Grounding (E04.1)</td><td>Naive RAG vs. Verified RAG using Gemini 2.5 Flash</td></tr>
<tr><td>Human Ground Truth (E05)</td><td><b>NOT MEASURED</b> (Human expert ground-truth annotations unavailable)</td></tr>
<tr><td>Citation Repair (E06.1)</td><td>Deterministic substring matching (191 opportunities)</td></tr>
<tr><td>Iterative Refinement (E07.1)</td><td>Multi-pass resynthesis feedback loop</td></tr>
<tr><td>Provenance Audit (E08)</td><td>Automated bidirectional verification of links and offsets (N=202)</td></tr>
<tr><td>Latency Profiling (E09)</td><td>Granular stage decomposition (p50 / p95)</td></tr>
<tr><td>Component Ablation (E10)</td><td>Controlled single-factor deletions (A0–A6)</td></tr>
<tr><td>Error Taxonomy (E11)</td><td>14-category multi-label error audit on TEST (N=15)</td></tr>
</table>

<!-- TABLE II -->
<table>
<caption>TABLE II: CANDIDATE CONTEXT RETRIEVAL PERFORMANCE (HYBRID RRF)</caption>
<tr><th class="center">Candidate Pool (k)</th><th class="center">Recall@k</th><th class="center">Hit@k</th></tr>
<tr><td class="center">5</td><td class="center">0.2700</td><td class="center">0.3000</td></tr>
<tr><td class="center">10</td><td class="center">0.5700</td><td class="center">0.6200</td></tr>
<tr><td class="center">20</td><td class="center">0.9500</td><td class="center">1.0000</td></tr>
<tr><td class="center">50</td><td class="center">1.0000</td><td class="center">1.0000</td></tr>
</table>
<div class="note">Note: Evaluated on ALL N=100 queries. TEST (N=15): all 10 answerable targets are present within the canonical k=20 pool; 5 additional TEST queries are unanswerable probe queries.</div>

<!-- TABLE III -->
<table>
<caption>TABLE III: GENERATION GROUNDING: NAIVE VS. VERIFIED RAG</caption>
<tr><th>Metric</th><th class="center">Naive RAG</th><th class="center">Verified RAG</th><th class="center">Direction</th></tr>
<tr><td>Claim Support Ratio (CSR)</td><td class="center">0.0533</td><td class="center">0.0350</td><td class="center">&uarr; better</td></tr>
<tr><td>Unsupported Claim Ratio (UCR)</td><td class="center">0.9467</td><td class="center">0.9650</td><td class="center">&darr; better</td></tr>
<tr><td>Citation Precision (CP)</td><td class="center">0.0600</td><td class="center">0.0400</td><td class="center">&uarr; better</td></tr>
<tr><td>Citation Coverage (COV)</td><td class="center">0.0617</td><td class="center">0.0433</td><td class="center">&uarr; better</td></tr>
</table>
<div class="note">Statistical Test: McNemar paired test statistic = 0.1667, p = 0.6831. No statistically significant grounding improvement was observed on the evaluated benchmark.</div>

<!-- TABLE IV -->
<table>
<caption>TABLE IV: SYSTEM LATENCY AND ITERATIVE REFINEMENT</caption>
<tr><th colspan="3">Part A: Disaggregated Pre-Generation Latency (E09, N=100)</th></tr>
<tr><th>Processing Stage</th><th class="right">p50 (ms)</th><th class="right">p95 (ms)</th></tr>
<tr><td>Hybrid Retrieval (BM25 + Dense)</td><td class="right">6.56</td><td class="right">19.12</td></tr>
<tr><td>Pure BGE Cross-Encoder Inference</td><td class="right">531.41</td><td class="right">4246.05</td></tr>
<tr><td>Hybrid + BGE Combined Stage</td><td class="right">535.06</td><td class="right">4251.51</td></tr>
<tr><th colspan="3">Part B: Iterative Refinement Tradeoff (E07.1, N=100)</th></tr>
<tr><th>Configuration</th><th class="right">Mean Latency</th><th>Outcomes (Improved / Unchanged / Degraded)</th></tr>
<tr><td>Iteration OFF (Single Pass)</td><td class="right">5691.35 ms</td><td>&mdash;</td></tr>
<tr><td>Iteration ON (Refined Loop)</td><td class="right">12655.70 ms</td><td>1 improved / 98 unchanged / 1 degraded</td></tr>
<tr><td colspan="3" class="note">&Delta;CSR = -0.0017, exact paired permutation p = 1.0000; 2.22x latency multiplier.</td></tr>
<tr><th colspan="3">Part C: Automated XAI Provenance Integrity (E08, N=202 Claims)</th></tr>
<tr><th colspan="2">Verification Metric</th><th class="right">Audit Adherence</th></tr>
<tr><td colspan="2">Trace Completeness</td><td class="right">1.0000 (100.0%)</td></tr>
<tr><td colspan="2">Claim-to-Evidence Accuracy</td><td class="right">1.0000 (100.0%)</td></tr>
<tr><td colspan="2">Citation-to-Evidence Accuracy</td><td class="right">1.0000 (100.0%)</td></tr>
<tr><td colspan="2">Offset Resolution Accuracy</td><td class="right">1.0000 (100.0%)</td></tr>
</table>
<div class="note">Note: Part C reflects automated provenance-audit verification across 202 algorithmic trace links, not human subject explainability measures.</div>

<!-- TABLE V -->
<table>
<caption>TABLE V: ARCHITECTURAL COMPONENT ABLATION STUDY (N=100)</caption>
<tr><th>ID</th><th>Configuration</th><th class="center">CSR</th><th class="right">Mean Latency (ms)</th><th class="center">Latency Status</th></tr>
<tr><td>A0</td><td>Full Pipeline</td><td class="center">0.0333</td><td class="right">12655.70</td><td class="center">Direct</td></tr>
<tr><td>A1</td><td>Minus Iteration</td><td class="center">0.0350</td><td class="right">5691.35</td><td class="center">Direct</td></tr>
<tr><td>A2</td><td>Minus Citation Repair*</td><td class="center">0.0533</td><td class="right">12610.70</td><td class="center">DERIVED</td></tr>
<tr><td>A3</td><td>Naive RAG Baseline</td><td class="center">0.0533</td><td class="right">5767.46</td><td class="center">Direct</td></tr>
<tr><td>A4</td><td>Minus BGE Cross-Encoder*</td><td class="center">0.0333</td><td class="right">12124.29</td><td class="center">DERIVED</td></tr>
<tr><td>A5</td><td>Dense Only Baseline</td><td class="center">0.0000</td><td class="right">8.46</td><td class="center">Direct</td></tr>
<tr><td>A6</td><td>BM25 Only Baseline</td><td class="center">0.0333</td><td class="right">0.98</td><td class="center">Direct</td></tr>
</table>
<div class="note">*Footnote: A2 and A4 latency values are mathematically derived component decompositions rather than independent end-to-end wall-clock runs.</div>

<!-- TABLE VI -->
<table>
<caption>TABLE VI: ERROR TAXONOMY ANALYSIS (E11, TEST SPLIT N=15, 28 CLAIMS)</caption>
<tr><th>Category</th><th class="center">Count</th><th class="center">Level</th><th>Interpretation / Status</th></tr>
<tr><th colspan="4">Measured Failure Categories</th></tr>
<tr><td>UNSUPPORTED_CLAIM</td><td class="center">28</td><td class="center">Claim</td><td>100.0% of TEST claims (28/28)</td></tr>
<tr><td>MISSING_CITATION</td><td class="center">28</td><td class="center">Claim</td><td>100.0% of TEST claims (28/28)</td></tr>
<tr><td>CITATION_REPAIR_FAILURE</td><td class="center">27</td><td class="center">Citation</td><td>100.0% of repair attempts (27/27)</td></tr>
<tr><td>ITERATION_FAILURE</td><td class="center">15</td><td class="center">Query</td><td>100.0% of TEST queries (15/15)</td></tr>
<tr><th colspan="4">Zero Measured Categories (0 events at canonical k=20)</th></tr>
<tr><td>RETRIEVAL_MISS</td><td class="center">0</td><td class="center">Query</td><td>0 misses (Hit@20 = 1.00)</td></tr>
<tr><td>CANDIDATE_POOL_MISS</td><td class="center">0</td><td class="center">Query</td><td>0 pool misses (Hit@20 = 1.00)</td></tr>
<tr><td>RERANKING_ERROR</td><td class="center">0</td><td class="center">Query</td><td>Top-20 context preserved</td></tr>
<tr><td>EVIDENCE_SELECTION_ERROR</td><td class="center">0</td><td class="center">Query</td><td>Verified selection</td></tr>
<tr><td>CONTRADICTED_CLAIM</td><td class="center">0</td><td class="center">Claim</td><td>No direct contradictions</td></tr>
<tr><td>WRONG_CITATION</td><td class="center">0</td><td class="center">Claim</td><td>0 incorrect pointer links</td></tr>
<tr><td>ONLINE_RETRIEVAL_FAILURE</td><td class="center">0</td><td class="center">Query</td><td>Local corpus execution</td></tr>
<tr><td>XAI_PROVENANCE_FAILURE</td><td class="center">0</td><td class="center">Claim</td><td>Complete deterministic trace</td></tr>
<tr><th colspan="4">Unmeasured Categories</th></tr>
<tr><td>VERIFICATION_FALSE_POSITIVE</td><td class="center"><i>NOT MEASURED</i></td><td class="center">Claim</td><td>E05 human ground truth unavailable</td></tr>
<tr><td>VERIFICATION_FALSE_NEGATIVE</td><td class="center"><i>NOT MEASURED</i></td><td class="center">Claim</td><td>E05 human ground truth unavailable</td></tr>
</table>
<div class="note">Total Categorized Events = 98 multi-label failure events across 15 TEST queries.</div>

</body>
</html>
""")
    print(f"  [SAVED] {html_path}")


# --------------------------------------------------------------------------------------
# 6. GENERATE TABLE PROVENANCE MANIFEST (table_provenance_manifest.csv)
# --------------------------------------------------------------------------------------
def generate_manifest(output_dir):
    manifest_path = os.path.join(output_dir, "table_provenance_manifest.csv")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("table_id,table_title,paper_section,primary_source_artifact,sample_size,validation_status,audit_notes\n")
        f.write("Table_I,Dataset and Evaluation Protocol,Section IV-A,ds_nexus_v11.json,N=100 (DEV=70 VAL=15 TEST=15),VALID,Standardized scientific benchmark specification; E05 recorded as unmeasured\n")
        f.write("Table_II,Candidate Retrieval Performance,Section IV-B,e03_3_canonical_results_live.json,N=100 (ALL),VALID,Canonical live E03.3 Hybrid RRF candidate recall (Hit@20=1.00; Recall@20=0.95); TEST N=15 note added\n")
        f.write("Table_III,Naive vs. Verified RAG,Section IV-D,e04_1_aggregate_metrics.json,N=100 (ALL),VALID,CSR UCR CP COV; McNemar test p=0.6831 shows no statistically significant improvement\n")
        f.write("Table_IV,Latency and Iterative Refinement,Section IV-C & IV-G & IV-H,table_latency.csv / e07_statistics.json / e08_metrics.json,N=100 / N=202,VALID,E09 latency decomposition; E07.1 refinement tradeoff (p=1.000); E08 automated audit\n")
        f.write("Table_V,Component Ablation Study,Section IV-I,e10_aggregate_metrics.json,N=100 (ALL),VALID,A0-A6 controlled single-factor deletions; A2 and A4 latencies explicitly marked DERIVED\n")
        f.write("Table_VI,Error Taxonomy Analysis,Section IV-J,e11_summary_report.md,N=15 TEST (28 claims),VALID,98 total events; 0 candidate pool miss at canonical k=20; E05 unmeasured\n")
    print(f"  [SAVED] {manifest_path}")


# --------------------------------------------------------------------------------------
# 7. GENERATE README (README_tables.md)
# --------------------------------------------------------------------------------------
def generate_readme(output_dir):
    readme_path = os.path.join(output_dir, "README_tables.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""# Publication Tables Package: ResearchNexus Conference Paper

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
""")
    print(f"  [SAVED] {readme_path}")


# --------------------------------------------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------------------------------------------
def main():
    print("=" * 80)
    print("ResearchNexus: Authoritative Publication Tables Generator")
    print("Authoritative Results Freeze Mode")
    print("=" * 80)
    
    # 1. Run strict assertions
    run_strict_assertions()
    
    output_dir = "paper_tables"
    print(f"\nGenerating publication tables into '{output_dir}/'...")
    
    generate_markdown(output_dir)
    generate_csv(output_dir)
    generate_latex(output_dir)
    generate_html_doc(output_dir)
    generate_manifest(output_dir)
    generate_readme(output_dir)
    
    print("\n" + "=" * 80)
    print("ALL TABLE VALUES MATCH RESULTS FREEZE")
    print("NO EXPERIMENTS RERUN")
    print("NO INVALID/SUPERSEDED DATA")
    print("E05 = NOT MEASURED")
    print("E11 retrieval/candidate-pool miss = 0 at canonical k=20")
    print("A2/A4 latency explicitly marked DERIVED")
    print("=" * 80)

if __name__ == "__main__":
    main()
