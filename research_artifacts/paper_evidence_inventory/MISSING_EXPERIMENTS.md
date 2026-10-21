# Missing Experiments & Evaluation Gaps Report

## 1. Executive Summary

This report identifies all missing experiments and evaluation gaps required to complete a comprehensive scientific paper on ResearchNexus.

---

## 2. Inventory of Missing Experiments

1. **Module 2: RAG Generation Baselines**:
   - **Gap**: No empirical LLM generation runs exist on `ds_nexus_v11`.
   - **Required Experiment**: Run standard RAG literature synthesis (e.g. using Llama-3 / GPT-4) on top of B4 retrieved evidence without verification.
   - **Metrics Needed**: ROUGE-L, BERTScore, Citation Precision, Citation Recall.

2. **Module 2: Multi-Stage Verification Pipeline**:
   - **Gap**: No empirical evaluation of claim extraction and NLI verification.
   - **Required Experiment**: Run multi-stage verified RAG and compute hallucination detection rate.
   - **Metrics Needed**: Claim Verification Precision, Unsupported Claim Rate, Hallucination Reduction %.

3. **Module 2: Citation Repair & Iterative Retrieval**:
   - **Gap**: No empirical runs testing whether citation repair improves factual correctness.
   - **Required Experiment**: Measure citation repair success rate on unverified claims.

4. **Module 2: End-to-End Latency Breakdown**:
   - **Gap**: End-to-end RAG latency (Retrieval + Reranking + Generation + Verification) is unmeasured.
   - **Required Experiment**: Measure p50/p95 latency breakdown across all pipeline stages.
