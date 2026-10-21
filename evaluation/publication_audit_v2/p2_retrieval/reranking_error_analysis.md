# Neural Reranking Error & Ranking Dynamics Analysis

## 1. Rank Transitions (Hybrid RRF -> Cross-Encoder BGE Reranker)
Comparing candidate rankings before and after cross-encoder reranking across the 15 test items:
1. **Positive Promotions (7 items)**: Answerable test items saw relevant papers promoted from ranks 4-12 into ranks 1-3, increasing MRR from 0.3685 to 0.5444 (+47.7% relative gain).
2. **Neutral/Preserved (3 items)**: Relevant items already at rank 1 remained at rank 1.
3. **Adversarial / Unanswerable Items (5 items)**: For unanswerable queries (`item_v11_086` to `item_v11_090`), top reranked scores had low absolute logits (all < 0.22), providing a clean threshold signal for the downstream generator to issue epistemic refusals.

## 2. Failure Cases & Limitations
- **Vocabulary mismatch on niche terminology**: On highly specialized acronyms, dense retrieval slightly downranked candidates, but RRF successfully restored them into the top-20 candidate pool.
