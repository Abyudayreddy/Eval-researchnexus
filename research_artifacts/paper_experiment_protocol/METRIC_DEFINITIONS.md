# Retrieval Metric Definitions (Frozen)

## 1. Overview

This document specifies the exact mathematical definitions and edge-case handling rules for all retrieval metrics.

---

## 2. Frozen Metric Specifications

### 2.1 Hit@k ($k \in \{1, 5\}$)
- **Definition**: Binary indicator of whether at least one relevant paper ID appears in the top-$k$ retrieved items.
- **Formula**: $\text{Hit@k} = \mathbb{I}\left( \text{retrieved}_{1..k} \cap \text{gold} \neq \emptyset \right)$
- **Relevance Unit**: Deduplicated `paper_id` strings.
- **Edge-Case Handling**: If gold is empty and top-$k$ is empty, returns `1.0`; otherwise returns `0.0`.

### 2.2 Recall@k ($k \in \{5, 10, 20, 50\}$)
- **Definition**: Ratio of unique retrieved gold paper IDs in top-$k$ to total gold paper IDs.
- **Formula**: $\text{Recall@k} = \frac{|\text{retrieved}_{1..k} \cap \text{gold}|}{|\text{gold}|}$
- **Relevance Unit**: Deduplicated `paper_id` strings.

### 2.3 Precision@5
- **Definition**: Fraction of top-5 retrieved paper IDs that are relevant.
- **Formula**: $\text{Precision@5} = \frac{|\text{retrieved}_{1..5} \cap \text{gold}|}{5.0}$

### 2.4 Mean Reciprocal Rank (MRR)
- **Definition**: Reciprocal rank of the first relevant paper ID in the full returned list.
- **Formula**: $\text{MRR} = \frac{1}{\min \{ r \mid \text{retrieved}_r \in \text{gold} \}}$ (Returns `0.0` if no hit exists).

### 2.5 Normalized Discounted Cumulative Gain (NDCG@5)
- **Definition**: DCG normalized by Ideal DCG over top-5 positions using binary relevance.
- **Formula**:
  $$\text{DCG@5} = \sum_{i=1}^{5} \frac{\mathbb{I}(\text{retrieved}_i \in \text{gold})}{\log_2(i+1)}, \quad \text{IDCG@5} = \sum_{i=1}^{\min(|\text{gold}|, 5)} \frac{1}{\log_2(i+1)}$$
