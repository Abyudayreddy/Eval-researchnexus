# ResearchNexus AI — Evaluation Epistemic Taxonomy

## 1. Motivation
In RAG evaluation benchmarks—especially those containing adversarial queries or difficult queries where retrieved context lacks the queried metric—large language models frequently generate evidence-bounded negative findings and abstentions (e.g., *"Based on the provided evidence, there is no mention of X"*).

Treating all such statements as standard factual claims that must possess explicit bracket citations `[i]` introduces a critical evaluation pathology:
- Correct epistemic refusals lack positive citation markers because no chunk in the context supports the non-existent claim.
- If the evaluation pipeline marks every uncited sentence as `UNSUPPORTED`, accurate model abstentions are penalized identically to hallucinations.

This taxonomy decouples factual assertions from negative findings and abstentions at the evaluation layer.

---

## 2. Epistemic Classification Categories

| Category | Definition | Example |
| :--- | :--- | :--- |
| **`SUPPORTED_FACTUAL_CLAIM`** | A positive factual assertion regarding the scientific topic that is substantiated by the cited retrieved evidence chunk. | *"The study introduces a novel loss function combining contrastive optimization and adaptive gradient scheduling [1]."* |
| **`PARTIALLY_SUPPORTED_FACTUAL_CLAIM`** | A positive factual assertion where core claims are substantiated but peripheral details lack explicit support. | *"The model achieves substantial precision gains while maintaining constant training stability [1]."* |
| **`CONTRADICTED_FACTUAL_CLAIM`** | A factual assertion that directly contradicts findings, figures, or statements in the retrieved evidence. | *"The paper achieved 99.9% accuracy score with zero latency overhead."* (when evidence notes substantial latency) |
| **`UNSUPPORTED_FACTUAL_CLAIM`** | A positive factual assertion that makes ungrounded, fabricated, or hallucinated claims not backed by the evidence. | *"Adaptive gradient scheduling achieves 92.4% Precision@5 in Dense Retrieval."* (when metric is absent) |
| **`INSUFFICIENT_EVIDENCE_FINDING`** | An evidence-grounded meta-finding explicitly stating that the retrieved context lacks information, metrics, or entities queried. | *"Based on the provided evidence, there is no mention of a '92.4% Precision@5' metric."* |
| **`APPROPRIATE_ABSTENTION`** | An explicit refusal or statement of inability to answer the research query because the context lacks supporting evidence. | *"Therefore, I cannot answer this query based on the retrieved documents."* |
| **`INAPPROPRIATE_ABSTENTION`** | A refusal to answer when the retrieved context actually contains sufficient gold evidence to answer the question. | *"I cannot answer this query."* (when gold chunk containing the exact answer is present in rank 1) |
| **`NON_FACTUAL_STATEMENT`** | Conversational, formatting, or hedging statements that do not convey factual assertions or evidence findings. | *"In conclusion, further work is necessary."* |

---

## 3. Preservation of Production Compatibility
- The production `ClaimObject` schema remains unchanged (`claim_id`, `claim_text`, `support_status`, `citation_ids`, `evidence_ids`).
- The fields `epistemic_type`, `is_factual_assertion`, `is_negative_finding`, and `is_abstention` are strictly evaluation-layer metadata added during benchmark scoring.
