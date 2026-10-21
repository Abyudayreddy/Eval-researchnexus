# E03 Candidate Recall Curve Methodology Specification

## 1. Executive Summary

This document records the exact experimental methodology for **E03: Candidate Recall Curve Experiment** conducted over the frozen **`ds_nexus_v11`** benchmark.

---

## 2. Experimental Setup

- **Benchmark Dataset**: `ds_nexus_v11` (100 items: 70 DEVELOPMENT, 15 VALIDATION, 15 TEST).
- **Retrieval Configurations**:
  - `B1_Dense`: Cosine similarity retrieval over Chroma vector store.
  - `B2_BM25`: Okapi BM25 lexical retrieval.
  - `B3_Hybrid_RRF`: Reciprocal Rank Fusion ($k=60$) combining BM25 and Dense outputs.
- **Evaluated Candidate Cutoffs**: $k \in \{5, 10, 20, 50\}$.
- **Execution Protocol**: Live production retrieval executed at each specific cutoff depth $k$ without padding or truncating pre-existing lists.

---

## 3. Metric Calculations

- **Recall@k**:
  $$\text{Recall@k} = \frac{|\text{retrieved}_{1..k} \cap \text{gold}|}{|\text{gold}|}$$
- **Hit@k**:
  $$\text{Hit@k} = \mathbb{I}\left( \text{retrieved}_{1..k} \cap \text{gold} \neq \emptyset \right)$$
- **First Gold Rank / Cutoff (`first_gold_k`)**:
  Smallest cutoff $k \in \{5, 10, 20, 50, \text{never}\}$ at which a gold-relevant paper first enters the candidate pool.
