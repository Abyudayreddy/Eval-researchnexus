# ResearchNexus Paper Experiment Master Plan (Frozen)

## 1. Executive Summary

This master plan freezes the complete experimental roadmap for ResearchNexus.

---

## 2. Master Execution Status & Readiness

```
PROTOCOL_STATUS = FROZEN
```

### 2.1 Experiments Ready to Start Immediately
- **E01 (Retrieval Baselines)**: COMPLETE (Verified artifacts exist).
- **E02 (BGE Reranking)**: COMPLETE (Verified artifacts exist).
- **E03 (Candidate Recall Curves)**: READY (Can process existing E01/E02 candidate lists).
- **E09 (Latency Breakdown)**: COMPLETE (Verified latency artifacts exist).

### 2.2 Experiments Blocked by Missing Annotation / Module 2 Code Execution
- **E04 (Naive vs. Verified RAG)**: Blocked by running Module 2 LLM generation scripts.
- **E05 (Claim Verification Evaluation)**: Blocked by NLI annotation on generated claims.
- **E06 (Citation Repair Evaluation)**: Blocked by Citation Repair execution.
- **E07 (Iterative Refinement)**: Blocked by Module 2 iterative pipeline execution.
- **E08 (XAI Provenance Tracing)**: Blocked by Module 2 trace logging.
- **E10 (Ablation Matrix)**: Blocked by Module 2 ablation runs (A1–A4).
- **E11 (Error Analysis)**: Blocked by human error categorization on TEST set.
