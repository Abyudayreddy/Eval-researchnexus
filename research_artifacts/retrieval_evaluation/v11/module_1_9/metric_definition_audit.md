# Metric Definition Audit Report

## 1. Audit Overview

This document records the formal mathematical and functional audit of the retrieval metrics implemented in the ResearchNexus evaluation engine (`compute_item_metrics`).

---

## 2. Metric-by-Metric Specification & Audit

| Metric | Ranking Cutoff | Relevance Target | Duplicate Handling | MRR / NDCG Cutoff | Handling of No Match | Handling of Multiple Matches | Mathematical Consistency Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hit@1** | 1 | `paper_ids` | Deduplicated | N/A | Returns `0.0` | Any hit in top-1 = `1.0` | **YES** |
| **Hit@5** | 5 | `paper_ids` | Deduplicated | N/A | Returns `0.0` | Any hit in top-5 = `1.0` | **YES** |
| **Recall@5** | 5 | `paper_ids` | Deduplicated | N/A | Returns `0.0` | $\| \text{hits in top 5} \| / \| \text{gold set} \|$ | **YES** |
| **Precision@5** | 5 | `paper_ids` | Deduplicated | N/A | Returns `0.0` | $\| \text{hits in top 5} \| / 5.0$ | **YES** |
| **MRR** | Full List | `paper_ids` | Deduplicated | Full List | Returns `0.0` | $1 / \text{rank of first hit}$ | **YES** |
| **NDCG@5** | 5 | `paper_ids` | Deduplicated | Cutoff = 5 | Returns `0.0` | $\text{DCG@5} / \text{IDCG@5}$ (Binary relevance) | **YES** |

---

## 3. Mathematical Formula Statements

- **Hit@k**:
  $$\text{Hit@k} = \mathbb{I}\left( \text{retrieved}_{1..k} \cap \text{gold} \neq \emptyset \right)$$

- **Recall@k**:
  $$\text{Recall@k} = \frac{|\text{retrieved}_{1..k} \cap \text{gold}|}{|\text{gold}|}$$

- **Precision@k**:
  $$\text{Precision@k} = \frac{|\text{retrieved}_{1..k} \cap \text{gold}|}{k}$$

- **MRR**:
  $$\text{MRR} = \frac{1}{\min \{ r \mid \text{retrieved}_r \in \text{gold} \}}$$

- **NDCG@5**:
  $$\text{DCG@5} = \sum_{i=1}^{5} \frac{\mathbb{I}(\text{retrieved}_i \in \text{gold})}{\log_2(i+1)}, \quad \text{IDCG@5} = \sum_{i=1}^{\min(|\text{gold}|, 5)} \frac{1}{\log_2(i+1)}$$

---

## 4. Final Verdict

> **"Is the implementation mathematically consistent with the metric name and the intended evaluation protocol?"**
> **YES.** The metric implementation in `compute_item_metrics` is rigorous, mathematically sound, and fully compliant with standard Information Retrieval evaluation conventions.
