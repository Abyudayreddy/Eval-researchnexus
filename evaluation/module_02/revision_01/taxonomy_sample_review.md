# ResearchNexus AI — Module 2 Revision 01: Taxonomy Sample Review

## 1. Overview & Purpose
This document provides an explicit, evidence-backed sample review across all operational epistemic categories used in the Module 2 evaluation. It validates that claims were not classified as non-factual simply because they lacked citations, and that affirmative propositions were distinguished from evidence-bounded negative findings.

---

## 2. Category 1: Factual Assertions (5 Examples)

### Example 1.1 (`item_v11_089`, Naive RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, the documents mention that recent advances in Multimodal Representation Learning face scaling challenges and formulate a novel loss function combining contrastive optimization and adaptive gradient scheduling."*
- **Underlying Evidence**: Paper `paper_res_035` (`paper_res_035_chunk_001`): *"Recent advances in Multimodal Representation Learning face significant scaling challenges... we formulate a novel loss function combining contrastive optimization and adaptive gradient scheduling."*
- **Old Classification**: `SUPPORTED` (Citation `[1]` present)
- **New Classification**: `SUPPORTED_FACTUAL_CLAIM`
- **Reason**: The sentence makes an affirmative factual statement describing background methodology and goals from the cited paper.
- **Citation Required**: Yes, requires an evidence citation because it asserts specific research methodology.

### Example 1.2 (`item_v11_091`, Naive RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, the retrieved documents regarding the studies on Dense Retrieval & Reranking Models state that recent advances in these models face scaling challenges, and the studies formulate a novel loss function combining contrastive optimization and adaptive gradient scheduling [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]."*
- **Underlying Evidence**: `paper_res_032_chunk_001`: *"Dense Retrieval & Reranking Models face scaling challenges... formulate a novel loss function combining contrastive optimization and adaptive gradient scheduling."*
- **Old Classification**: `UNSUPPORTED` (Penalized under Stage A because multiple bracket tags confused deterministic lookup)
- **New Classification**: `SUPPORTED_FACTUAL_CLAIM`
- **Reason**: True affirmative statement substantiated by the retrieved papers.
- **Citation Required**: Yes, empirical proposition requiring evidence attribution.

### Example 1.3 (`item_v11_091`, Verified RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, the studies on Dense Retrieval & Reranking Models state that they 'face scaling challenges' and introduce a 'novel loss function combining contrastive optimization and adaptive gradient scheduling' [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]."*
- **Underlying Evidence**: `paper_res_032_chunk_001`
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `SUPPORTED_FACTUAL_CLAIM`
- **Reason**: Direct quotation and factual assertion accurately reflecting the underlying evidence chunks.
- **Citation Required**: Yes.

### Example 1.4 (`item_v11_093`, Verified RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, the retrieved documents for the studies on Large Language Models & Evaluation state that recent advances face scaling challenges and formulate a novel loss function combining contrastive optimization and adaptive gradient scheduling [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]."*
- **Underlying Evidence**: `paper_res_034_chunk_001`
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `SUPPORTED_FACTUAL_CLAIM`
- **Reason**: Factual background summary substantiated by the corpus.
- **Citation Required**: Yes.

### Example 1.5 (`item_v11_094`, Naive RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, the documents state that recent advances in Multimodal Representation Learning face scaling challenges, and formulate a novel loss function combining contrastive optimization and adaptive gradient scheduling [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]."*
- **Underlying Evidence**: `paper_res_035_chunk_001`
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `SUPPORTED_FACTUAL_CLAIM`
- **Reason**: Factual assertion substantiated by the retrieved paper.
- **Citation Required**: Yes.

---

## 3. Category 2: Insufficient-Evidence Findings (5 Examples)

### Example 2.1 (`item_v11_086`, Naive RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, there is no mention of a '92.4% Precision@5' metric associated with adaptive gradient scheduling in Dense Retrieval & Reranking Models."*
- **Underlying Evidence**: All 20 retrieved chunks from `B3_Hybrid_RRF` for `item_v11_086` lack any mention of "92.4% Precision@5".
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `INSUFFICIENT_EVIDENCE_FINDING`
- **Reason**: The model is reporting an empirical meta-finding regarding the absence of the queried value in the provided documents. It is not asserting that the metric does or does not exist in the real world, only that the evidence text lacks it.
- **Citation Required**: No. A chunk citation is neither expected nor logically possible for the non-existence of a phrase across a document collection.

### Example 2.2 (`item_v11_087`, Verified RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, there is no mention of '92.4% Precision@5' or any specific precision metrics related to adaptive gradient scheduling."*
- **Underlying Evidence**: Retrieval pool lacks the queried figure.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `INSUFFICIENT_EVIDENCE_FINDING`
- **Reason**: Explicit negative finding bounding the system's epistemic horizon.
- **Citation Required**: No.

### Example 2.3 (`item_v11_088`, Naive RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, there is no mention of a '92.4% Precision@5' metric related to adaptive gradient scheduling or Large Language Models & Evaluation."*
- **Underlying Evidence**: Context lacks the figure.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `INSUFFICIENT_EVIDENCE_FINDING`
- **Reason**: Negative finding documenting missing information.
- **Citation Required**: No.

### Example 2.4 (`item_v11_092`, Naive RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, the retrieved documents do not contain any claims regarding a '99.9% accuracy score with zero latency overhead' for the studies on Deep Learning & Neural Architectures."*
- **Underlying Evidence**: Context lacks the claim.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `INSUFFICIENT_EVIDENCE_FINDING`
- **Reason**: Accurate negative finding.
- **Citation Required**: No.

### Example 2.5 (`item_v11_095`, Verified RAG, Claim 02)
- **Claim Text**: *"The retrieved documents do not contain any claims regarding a '99.9% accuracy score with zero latency overhead.' Therefore, I cannot answer this query based on the retrieved documents."*
- **Underlying Evidence**: Context lacks the claim.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `INSUFFICIENT_EVIDENCE_FINDING` (Compound with abstention)
- **Reason**: Accurate statement that retrieved documents omit the target claim.
- **Citation Required**: No.

---

## 4. Category 3: Appropriate Abstentions (5 Examples)

### Example 3.1 (`item_v11_086`, Naive RAG, Claim 02)
- **Claim Text**: *"Therefore, I cannot answer this query based on the retrieved documents."*
- **Underlying Evidence**: Retained context lacks the queried metric.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `APPROPRIATE_ABSTENTION`
- **Reason**: Standard epistemic refusal concluding an unanswerable query.
- **Citation Required**: No.

### Example 3.2 (`item_v11_086`, Verified RAG, Claim 02)
- **Claim Text**: *"Therefore, I cannot answer the research query based on the retrieved documents."*
- **Underlying Evidence**: Same as above.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `APPROPRIATE_ABSTENTION`
- **Reason**: Epistemic refusal to synthesize unsupported facts.
- **Citation Required**: No.

### Example 3.3 (`item_v11_092`, Verified RAG, Claim 02)
- **Claim Text**: *"Therefore, I cannot answer the query based on the retrieved documents."*
- **Underlying Evidence**: Evidence lacks the queried 99.9% accuracy figure.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `APPROPRIATE_ABSTENTION`
- **Reason**: Refusal to fabricate answers on incomplete evidence.
- **Citation Required**: No.

### Example 3.4 (`item_v11_096`, Naive RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, there is no mention of a 'non-existent quantum gravity calibration constant' or '10,000 qubit superconductors.' Therefore, you cannot answer this question based on the retrieved documents."*
- **Underlying Evidence**: Adversarial unanswerable benchmark query; context lacks concept.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `APPROPRIATE_ABSTENTION`
- **Reason**: Explicit refusal on adversarial concept.
- **Citation Required**: No.

### Example 3.5 (`item_v11_100`, Verified RAG, Claim 01)
- **Claim Text**: *"Based on the provided evidence, there is no mention of a 'non-existent quantum gravity calibration constant' or '10,000 qubit superconductors.' Therefore, I cannot answer the query based on the retrieved documents."*
- **Underlying Evidence**: Adversarial query.
- **Old Classification**: `UNSUPPORTED`
- **New Classification**: `APPROPRIATE_ABSTENTION`
- **Reason**: Epistemic refusal.
- **Citation Required**: No.

---

## 5. Category 4: Compound Propositions Audited for Over-Conservatism

### Example 4.1 (`item_v11_090`, Naive RAG, Claim 02)
- **Claim Text**: *"While the evidence notes that recent advances in Dense Retrieval & Reranking Models face scaling challenges and formulate a novel loss function combining contrastive optimization and adaptive gradient scheduling [1, 3, 5, 7, 9, 11, 13, 15, 17, 19], it does not contain information regarding a 92.4% Precision@5 metric."*
- **Audit Findings**:
  - Contains an **affirmative factual proposition**: *"advances face scaling challenges and formulate a novel loss function..."* (Supported by `paper_res_036_chunk_001`).
  - Contains a **negative finding**: *"it does not contain information regarding a 92.4% Precision@5 metric."*
- **Classification**: `COMPOUND_FACTUAL_AND_NEGATIVE_FINDING`
- **Resolution**: This sentence is audited as containing a factual proposition. If evaluated under strict factual claim filtering, it counts as a supported factual proposition ($+1$ to factual claims), rather than being discarded as pure abstention.

### Example 4.2 (`item_v11_089`, Verified RAG, Claim 02)
- **Claim Text**: *"While the evidence notes that multimodal representation learning research formulates novel loss functions combining adaptive gradient scheduling and contrastive optimization to address scaling challenges [1, 3, 5, 7, 9, 11, 13, 15, 17, 19], it does not contain information regarding a 92.4% Precision@5 result."*
- **Audit Findings**:
  - Affirms background methodology substantiated by `paper_res_035_chunk_001`.
  - Concludes with a negative finding regarding the queried precision metric.
- **Classification**: `COMPOUND_FACTUAL_AND_NEGATIVE_FINDING`
- **Resolution**: Counted as a supported factual assertion alongside its negative finding.

---

## 6. Category 5: Claims Reclassified from Legacy UNSUPPORTED (5 Examples)
1. `item_v11_086` claim 01: From `UNSUPPORTED` $\rightarrow$ `INSUFFICIENT_EVIDENCE_FINDING` (Epistemic negative finding).
2. `item_v11_086` claim 02: From `UNSUPPORTED` $\rightarrow$ `APPROPRIATE_ABSTENTION` (Epistemic refusal).
3. `item_v11_091` claim 01: From `UNSUPPORTED` $\rightarrow$ `SUPPORTED_FACTUAL_CLAIM` (Factual background assertion substantiated by paper).
4. `item_v11_096` claim 01: From `UNSUPPORTED` $\rightarrow$ `APPROPRIATE_ABSTENTION` (Adversarial abstention).
5. `item_v11_098` claim 01: From `UNSUPPORTED` $\rightarrow$ `APPROPRIATE_ABSTENTION` (Adversarial abstention).
