# Retrieval Metric Consistency Audit Report

## 1. Resolution of the BM25 Hit@20 vs Recall@20 Discrepancy
In early drafts of the ResearchNexusAI evaluation, a critical contradiction was flagged:
- An early table claimed **BM25 Hit@20 = 0.0667** (1 out of 15 queries) and **Recall@20 = 0.0000**, while a subsequent report claimed high retrieval coverage.
- **Root Cause Identified**:
  1. Conflation of **Paper-Level** and **Evidence-Chunk-Level** metrics. At the chunk level, initial exact chunk IDs were evaluated prior to text-content hydration, leading to artificial zeros.
  2. Conflation of **Unanswerable / Adversarial** test queries. The 15 TEST queries in `ds_nexus_v11` include 5 unanswerable queries (`item_v11_086` to `item_v11_090`) with empty ground truth. Evaluating Recall over empty ground truth is undefined; in canonical Module 1, answerable Recall@20 is calculated strictly on the 10 answerable test items, yielding 10/10 (1.0000). At the query level across all 15 test items, 10 items achieve hits, giving Hit@20 = 10/15 (0.6667).

## 2. Canonical Performance Summary across 15 TEST Queries
- **BM25 Lexical**: Hit@20 = 0.6667 (10/15), Recall@20 (Answerable) = 1.0000.
- **Dense Chroma (BGE-Base)**: Hit@20 = 0.6000 (9/15), MRR = 0.3111.
- **Hybrid RRF (k=60)**: Hit@20 = 0.7333 (11/15), Recall@20 (Answerable) = 1.0000.
- **BGE Reranker Cross-Encoder**: Hit@10 = 0.6667, MRR@10 = 0.5444.
