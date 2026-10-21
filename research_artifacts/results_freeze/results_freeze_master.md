# Authoritative Results Freeze Master Table
**Dataset**: `ds_nexus_v11` (N=100: DEV=70, VAL=15, TEST=15)
**Package Status**: FROZEN (Reconciled with Canonical E03.3 Live Candidate Recall)

| Experiment | Name | Split | N | Configuration | Metric | Value | Unit | Stat Test (p-val) | 95% CI | Limitations |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| DATASET | Dataset Specification | ALL | 100 | Frozen ds_nexus_v11 | Total Queries | **100** | count | N/A | N/A |  |
| DATASET | Dataset Specification | DEV | 70 | Frozen ds_nexus_v11 | Development Queries | **70** | count | N/A | N/A |  |
| DATASET | Dataset Specification | VAL | 15 | Frozen ds_nexus_v11 | Validation Queries | **15** | count | N/A | N/A |  |
| DATASET | Dataset Specification | TEST | 15 | Frozen ds_nexus_v11 | Test Queries | **15** | count | N/A | N/A | TEST N=15 limits high statistical power; descriptive analysis primary. |
| E01 | Retrieval Baselines | TEST | 15 | B1_Dense | MRR | **0.0** | score | N/A | N/A |  |
| E01 | Retrieval Baselines | TEST | 15 | B1_Dense | Hit@5 | **0.0** | rate | N/A | N/A |  |
| E01 | Retrieval Baselines | TEST | 15 | B1_Dense | Latency_p50 | **13.51** | ms | N/A | N/A |  |
| E01 | Retrieval Baselines | TEST | 15 | B2_BM25 | MRR | **0.0759** | score | N/A | N/A |  |
| E01 | Retrieval Baselines | TEST | 15 | B2_BM25 | Hit@5 | **0.0** | rate | N/A | N/A |  |
| E01 | Retrieval Baselines | TEST | 15 | B2_BM25 | Latency_p50 | **0.69** | ms | N/A | N/A |  |
| E01 | Retrieval Baselines | TEST | 15 | B3_Hybrid_RRF | MRR | **0.0** | score | N/A | N/A |  |
| E01 | Retrieval Baselines | TEST | 15 | B3_Hybrid_RRF | Hit@5 | **0.0** | rate | N/A | N/A |  |
| E01 | Retrieval Baselines | TEST | 15 | B3_Hybrid_RRF | Latency_p50 | **7.76** | ms | N/A | N/A |  |
| E02 | BGE Cross-Encoder Reranking | TEST | 15 | B4_Hybrid_BGE | MRR | **0.0** | score | N/A | N/A |  |
| E02 | BGE Cross-Encoder Reranking | TEST | 15 | B4_Hybrid_BGE | Hit@5 | **0.0** | rate | N/A | N/A |  |
| E02 | BGE Cross-Encoder Reranking | ALL | 100 | B4_Hybrid_BGE | Genuine_Invocations | **100** | count | N/A | N/A | BGE reranker preserves top-20 context; cannot rescue items absent from pre-rerank pool. |
| E03.3 | Candidate Context Recall | ALL | 100 | B3_Hybrid_RRF | Recall@5 | **0.27** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | ALL | 100 | B3_Hybrid_RRF | Recall@10 | **0.57** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | ALL | 100 | B3_Hybrid_RRF | Recall@20 | **0.95** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | ALL | 100 | B3_Hybrid_RRF | Recall@50 | **1.0** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | ALL | 100 | B3_Hybrid_RRF | Hit@5 | **0.3** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | ALL | 100 | B3_Hybrid_RRF | Hit@10 | **0.62** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | ALL | 100 | B3_Hybrid_RRF | Hit@20 | **1.0** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | ALL | 100 | B3_Hybrid_RRF | Hit@50 | **1.0** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | DEV | 70 | B3_Hybrid_RRF | Recall@20 | **1.0** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | DEV | 70 | B3_Hybrid_RRF | Hit@20 | **1.0** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | VAL | 15 | B3_Hybrid_RRF | Recall@20 | **0.6667** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | VAL | 15 | B3_Hybrid_RRF | Hit@20 | **1.0** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | TEST | 15 | B3_Hybrid_RRF | Recall@20 | **1.0** | rate | N/A | N/A |  |
| E03.3 | Candidate Context Recall | TEST | 15 | B3_Hybrid_RRF | Hit@20 | **1.0** | rate | N/A | N/A |  |
| E04.1 | Generation Evaluation | ALL | 100 | Naive_RAG | CSR | **0.0533** | rate | N/A | [0.0133, 0.1] |  |
| E04.1 | Generation Evaluation | ALL | 100 | Verified_RAG | CSR | **0.035** | rate | N/A | [0.01, 0.075] |  |
| E04.1 | Generation Evaluation | ALL | 100 | Naive_RAG | UCR | **0.9467** | rate | N/A | [0.9, 0.9867] |  |
| E04.1 | Generation Evaluation | ALL | 100 | Verified_RAG | UCR | **0.965** | rate | N/A | [0.925, 0.99] |  |
| E04.1 | Generation Evaluation | ALL | 100 | Naive_RAG | CP | **0.06** | score | N/A | N/A |  |
| E04.1 | Generation Evaluation | ALL | 100 | Verified_RAG | CP | **0.04** | score | N/A | N/A |  |
| E04.1 | Generation Evaluation | ALL | 100 | Naive_vs_Verified | McNemar_Test | **0.1667** | stat | McNemar (0.6831) | N/A | No statistically significant grounding improvement over Naive RAG on this benchmark. |
| E04.1 | Generation Evaluation | ALL | 100 | Naive_RAG | Latency_Mean | **5767.46** | ms | N/A | N/A |  |
| E04.1 | Generation Evaluation | ALL | 100 | Verified_RAG | Latency_Mean | **5691.35** | ms | N/A | N/A |  |
| E05 | Human Ground-Truth Evaluation | ALL | 0 | Human_Annotation | Precision_Recall_F1 | **NOT_MEASURED** | N/A | N/A | N/A | Blocked due to unavailability of human ground-truth annotations. |
| E06.1 | Citation Repair | ALL | 100 | CitationRepair | Opportunities | **191** | count | N/A | N/A |  |
| E06.1 | Citation Repair | ALL | 100 | CitationRepair | Attempts | **191** | count | N/A | N/A |  |
| E06.1 | Citation Repair | ALL | 100 | CitationRepair | Successful_Repairs | **0** | count | N/A | N/A | Under evaluated context and conservative matching policy, no opportunity satisfied repair criterion. |
| E06.1 | Citation Repair | ALL | 100 | CitationRepair | Success_Rate | **0.0** | rate | N/A | N/A |  |
| E06.1 | Citation Repair | ALL | 202 | CitationRepair | Latency_p50 | **0.16** | ms | N/A | N/A |  |
| E07.1 | Iterative Refinement | ALL | 100 | Refinement_Quality | Improved_Queries | **1** | count | N/A | N/A |  |
| E07.1 | Iterative Refinement | ALL | 100 | Refinement_Quality | Unchanged_Queries | **98** | count | N/A | N/A |  |
| E07.1 | Iterative Refinement | ALL | 100 | Refinement_Quality | Degraded_Queries | **1** | count | N/A | N/A |  |
| E07.1 | Iterative Refinement | ALL | 100 | Refinement_Quality | Delta_CSR | **-0.0017** | delta | Exact Paired Permutation (1.0) | [-0.015, 0.01] | Substantial latency increase (2.2x) with no statistically significant grounding benefit. |
| E07.1 | Iterative Refinement | ALL | 100 | Iteration_ON | Latency_Mean | **12655.7** | ms | N/A | N/A |  |
| E07.1 | Iterative Refinement | ALL | 100 | Iteration_OFF | Latency_Mean | **5691.35** | ms | N/A | N/A |  |
| E08 | XAI Provenance Audit | ALL | 202 | Automated_Audit | Trace_Completeness | **1.0** | rate | N/A | N/A | Represents automated audit protocol verification; not subjective human explainability. |
| E08 | XAI Provenance Audit | ALL | 202 | Automated_Audit | Claim_to_Evidence_Accuracy | **1.0** | rate | N/A | N/A |  |
| E08 | XAI Provenance Audit | ALL | 202 | Automated_Audit | Citation_to_Evidence_Accuracy | **1.0** | rate | N/A | N/A |  |
| E08 | XAI Provenance Audit | ALL | 202 | Automated_Audit | Offset_Resolution_Accuracy | **1.0** | rate | N/A | N/A |  |
| E08 | XAI Provenance Audit | ALL | 202 | Automated_Audit | Online_Provenance | **NOT_APPLICABLE** | N/A | N/A | N/A |  |
| E09 | Disaggregated Latency | ALL | 100 | Hybrid_Retrieval | Latency_p50 | **6.56** | ms | N/A | N/A |  |
| E09 | Disaggregated Latency | ALL | 100 | Hybrid_Retrieval | Latency_p95 | **19.12** | ms | N/A | N/A |  |
| E09 | Disaggregated Latency | ALL | 100 | Pure_BGE_Inference | Latency_p50 | **531.41** | ms | N/A | N/A |  |
| E09 | Disaggregated Latency | ALL | 100 | Pure_BGE_Inference | Latency_p95 | **4246.05** | ms | N/A | N/A |  |
| E09 | Disaggregated Latency | ALL | 100 | Total_Hybrid_BGE_Stage | Latency_p50 | **535.06** | ms | N/A | N/A |  |
| E09 | Disaggregated Latency | ALL | 100 | Total_Hybrid_BGE_Stage | Latency_p95 | **4251.51** | ms | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A0_Full | CSR | **0.0333** | rate | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A0_Full | Latency_Mean | **12655.7** | ms | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A1_Minus_Iteration | CSR | **0.035** | rate | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A1_Minus_Iteration | Latency_Mean | **5691.35** | ms | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A2_Minus_Citation_Repair | CSR | **0.0533** | rate | N/A | N/A | Derived decomposed timing from A0 minus CitationRepair stage. |
| E10 | Component Ablation | ALL | 100 | A2_Minus_Citation_Repair | Latency_Mean | **12610.7** | ms | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A3_Naive_RAG | CSR | **0.0533** | rate | N/A | N/A | Combined verification-and-repair pipeline removal. |
| E10 | Component Ablation | ALL | 100 | A3_Naive_RAG | Latency_Mean | **5767.46** | ms | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A4_Minus_BGE | CSR | **0.0333** | rate | N/A | N/A | Derived decomposed timing from A0 minus BGE stage. |
| E10 | Component Ablation | ALL | 100 | A4_Minus_BGE | Latency_Mean | **12124.29** | ms | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A5_Dense_Only | CSR | **0.0** | rate | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A5_Dense_Only | Latency_Mean | **8.46** | ms | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A6_BM25_Only | CSR | **0.0333** | rate | N/A | N/A |  |
| E10 | Component Ablation | ALL | 100 | A6_BM25_Only | Latency_Mean | **0.98** | ms | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 15 | Multi_Label_Taxonomy | RETRIEVAL_MISS | **0** | count | N/A | N/A | 0 at k=20; all 15 TEST queries achieve Hit@20=1.0 in canonical E03.3 candidate pool. |
| E11 | Error Taxonomy | TEST | 15 | Multi_Label_Taxonomy | CANDIDATE_POOL_MISS | **0** | count | N/A | N/A | 0 at k=20; all gold targets present in canonical top-20 candidate pool. |
| E11 | Error Taxonomy | TEST | 15 | Multi_Label_Taxonomy | RERANKING_ERROR | **0** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 15 | Multi_Label_Taxonomy | EVIDENCE_SELECTION_ERROR | **0** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 28 | Multi_Label_Taxonomy | UNSUPPORTED_CLAIM | **28** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 28 | Multi_Label_Taxonomy | CONTRADICTED_CLAIM | **0** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 0 | Multi_Label_Taxonomy | WRONG_CITATION | **0** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 28 | Multi_Label_Taxonomy | MISSING_CITATION | **28** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 0 | Multi_Label_Taxonomy | VERIFICATION_FALSE_POSITIVE | **NOT_MEASURED** | N/A | N/A | N/A | Unmeasurable without human ground truth (E05 blocked). |
| E11 | Error Taxonomy | TEST | 0 | Multi_Label_Taxonomy | VERIFICATION_FALSE_NEGATIVE | **NOT_MEASURED** | N/A | N/A | N/A | Unmeasurable without human ground truth (E05 blocked). |
| E11 | Error Taxonomy | TEST | 27 | Multi_Label_Taxonomy | CITATION_REPAIR_FAILURE | **27** | count | N/A | N/A | 27/27 attempts failed; 1 record pre-supported and unattempted. |
| E11 | Error Taxonomy | TEST | 15 | Multi_Label_Taxonomy | ITERATION_FAILURE | **15** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 15 | Multi_Label_Taxonomy | ONLINE_RETRIEVAL_FAILURE | **0** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 28 | Multi_Label_Taxonomy | XAI_PROVENANCE_FAILURE | **0** | count | N/A | N/A |  |
| E11 | Error Taxonomy | TEST | 15 | Multi_Label_Taxonomy | Total_Categorized_Events | **98** | count | N/A | N/A |  |