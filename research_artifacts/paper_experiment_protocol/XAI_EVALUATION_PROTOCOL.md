# Explainable AI (XAI) Evaluation Protocol (Frozen)

## 1. Overview

This document specifies the metrics for evaluating Explainable AI (XAI) provenance tracing in ResearchNexus.

---

## 2. Provenance Chain Definition

A complete XAI provenance trace must link:
$$\text{Final Answer Claim} \longrightarrow \text{Inline Citation} \longrightarrow \text{Evidence Block Text} \longrightarrow \text{Paper ID / Chunk ID} \longrightarrow \text{BGE Score} \longrightarrow \text{RRF Rank} \longrightarrow \text{Retrieval Source (BM25/Dense)}$$

---

## 3. XAI Evaluation Metrics

1. **Trace Completeness**: Fraction of generated answer claims that possess a non-broken end-to-end provenance link down to raw database chunk offsets.
2. **Trace Resolution Accuracy**: Accuracy of exact character-offset matching between evidence block quotes and SQLite `PaperChunk` text.
3. **Claim-to-Evidence Link Accuracy**: Precision of linking claims to correct supporting paragraphs.
