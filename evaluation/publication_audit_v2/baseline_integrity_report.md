# Baseline Integrity Report

## 1. Overview
Audit of baseline configurations across retrieval, generation, verification, and repair pipelines to ensure benchmark integrity and eliminate methodological artifacts.

## 2. Model & Runtime Integrity
- **Frozen Generator LLM**: `gemini-2.5-flash` (Google GenAI SDK)
- **Temperature**: `0.0` (Deterministic greedy decoding)
- **Embedding Model**: `BAAI/bge-base-en-v1.5` (768 dimensions, cosine similarity)
- **Reranker Model**: `BAAI/bge-reranker-base` (Cross-encoder sequence pair classification)
- **Benchmark Split**: `ds_nexus_v11` (N=100: DEV=70, VAL=15, TEST=15)

## 3. Discrepancy Reconciliation
1. **Model Name Ambiguity**: Historical drafts informally noted "Gemini 3.5 Flash Lite" or "gemini-1.5-flash". Codebase inspection confirms the actual execution engine is `gemini-2.5-flash`.
2. **Benchmark Query Split**: Exactly 15 TEST queries (`item_v11_086` through `item_v11_100`). Five are unanswerable/adversarial queries designed to test epistemic abstention.
3. **Retrieval Granularity Conflation**: Paper-level metrics vs Chunk-level metrics must never be mixed in the same table column without explicit granularity annotation.
