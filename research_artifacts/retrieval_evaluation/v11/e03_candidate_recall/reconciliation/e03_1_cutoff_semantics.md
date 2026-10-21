# Cutoff Semantics Specification

## 1. Overview

This document specifies the cutoff semantics for candidate retrieval evaluation in E03 and E03.1.

---

## 2. Cutoff Rules & Deduplication Timing

1. **Retrieval Output Depth**:
   - `k=5`, `k=10`, `k=20`, `k=50` represent live retrieval calls executed at that specific cutoff depth. No smaller lists are padded.
2. **Deduplication Timing**:
   - Retrieval operates on document chunks.
   - For paper-level Recall@k and Hit@k evaluation, duplicate paper IDs resulting from multiple chunks of the same paper are **deduplicated preserving rank order** before selecting top-$k$ paper candidates.
