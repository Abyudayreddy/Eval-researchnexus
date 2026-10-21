# Module 1: Information Retrieval Metric Definitions

This document provides formal, unambiguous mathematical definitions for all evaluation metrics employed in Module 1.

Module 1 evaluates two distinct relevance entities separately:
1. **Paper-Level Relevance (Document Discovery)**: Measures whether a retrieved chunk belongs to a gold paper ($d \in \text{GoldPapers}_q$).
2. **Evidence-Level Relevance (Chunk Grounding)**: Measures whether the exact retrieved chunk is an identified gold evidence chunk ($c \in \text{GoldEvidence}_q$).

---

## 1. Mathematical Definitions

Let $Q$ denote the evaluation query set, where $|Q| = N$.  
For each query $q \in Q$:
- $\text{Gold}_q$ denotes the set of relevant items (either relevant papers $\mathcal{P}_q^*$ or relevant chunks $\mathcal{E}_q^*$).
- $R_{q, K} = [r_{q, 1}, r_{q, 2}, \dots, r_{q, K}]$ denotes the ordered list of top-$K$ retrieved items.
- $\mathbb{I}(\cdot)$ is the indicator function, returning $1$ if the condition is true and $0$ otherwise.

### 1.1 Hit Rate at K (Hit@K)
$$\text{Hit@K}(q) = \begin{cases} 
1 & \text{if } \exists i \in \{1, \dots, K\} \text{ such that } r_{q, i} \in \text{Gold}_q \\ 
0 & \text{otherwise} 
\end{cases}$$

$$\text{Hit@K} = \frac{1}{|Q|} \sum_{q \in Q} \text{Hit@K}(q)$$

*Special Condition*: For unanswerable or adversarial queries where $|\text{Gold}_q| = 0$, $\text{Hit@K}(q) = 0.0$ (no relevant items exist to be hit).

### 1.2 Recall at K (Recall@K)
$$\text{Recall@K}(q) = \begin{cases}
\frac{|\{r_{q, 1}, \dots, r_{q, K}\} \cap \text{Gold}_q|}{|\text{Gold}_q|} & \text{if } |\text{Gold}_q| > 0 \\
\text{N/A (or } 0.0 \text{ in macro-average)} & \text{if } |\text{Gold}_q| = 0
\end{cases}$$

$$\text{Recall@K} = \frac{1}{|Q_{|\text{Gold}| > 0}|} \sum_{q \in Q_{|\text{Gold}| > 0}} \text{Recall@K}(q)$$

*Consistency Constraint*: If $|\text{Gold}_q| > 0$, $\text{Hit@K}(q) = 1 \iff \text{Recall@K}(q) > 0$. If $\text{Hit@K}(q) = 0 \iff \text{Recall@K}(q) = 0$.

### 1.3 Precision at K (Precision@K)
$$\text{Precision@K}(q) = \frac{|\{r_{q, 1}, \dots, r_{q, K}\} \cap \text{Gold}_q|}{K}$$

$$\text{Precision@K} = \frac{1}{|Q|} \sum_{q \in Q} \text{Precision@K}(q)$$

### 1.4 Mean Reciprocal Rank (MRR)
Let $\text{rank}_q^*$ denote the 1-based rank index of the *first* relevant retrieved item for query $q$:
$$\text{RR}(q) = \begin{cases} 
\frac{1}{\text{rank}_q^*} & \text{if } \exists r_{q, i} \in \text{Gold}_q \\ 
0.0 & \text{if no relevant item is retrieved} 
\end{cases}$$

$$\text{MRR} = \frac{1}{|Q|} \sum_{q \in Q} \text{RR}(q)$$

### 1.5 Normalized Discounted Cumulative Gain at K (nDCG@K)
With binary relevance labels $rel_q(r_{q, i}) \in \{0, 1\}$:
$$\text{DCG@K}(q) = \sum_{i=1}^K \frac{rel_q(r_{q, i})}{\log_2(i + 1)}$$

$$\text{IDCG@K}(q) = \sum_{i=1}^{\min(|\text{Gold}_q|, K)} \frac{1}{\log_2(i + 1)}$$

$$\text{nDCG@K}(q) = \begin{cases} 
\frac{\text{DCG@K}(q)}{\text{IDCG@K}(q)} & \text{if } \text{IDCG@K}(q) > 0 \\ 
0.0 & \text{otherwise} 
\end{cases}$$

$$\text{nDCG@K} = \frac{1}{|Q|} \sum_{q \in Q} \text{nDCG@K}(q)$$

---

## 2. Evaluation Cutoffs
Standard evaluation cutoffs evaluated: $K \in \{5, 10, 20, 50\}$.

---

## 3. Entity-Level Distinction
- **Paper-Level Metrics**: Evaluated after mapping chunk items to unique paper identifiers $\text{paper\_id}(c)$. Duplicate chunks from the same paper within a cutoff window are deduplicated so each unique paper occupies exactly one rank position.
- **Evidence-Level Metrics**: Evaluated over the raw chunk identifiers $c$ directly against $\text{GoldEvidence}_q$ without deduplication.
