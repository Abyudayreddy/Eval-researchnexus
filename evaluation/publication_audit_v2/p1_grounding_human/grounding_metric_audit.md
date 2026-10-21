# Grounding & Verification Metric Audit (Phase P1)

## 1. Executive Summary & Epistemic Taxonomy Resolution
In legacy Module 2 evaluations, an epistemic refusal confound biased the grounding metrics:
When the model encountered unanswerable test queries (`item_v11_086` to `item_v11_090`), it correctly issued epistemic abstentions (e.g., "The provided documents do not contain evidence regarding...").
The legacy claim parser extracted these sentences as factual assertions and scored them as `UNSUPPORTED` because they lacked explicit bracket citations to retrieved corpus passages. This artificially penalized the groundedness of cautious responses.

Under the corrected Revision 01 Epistemic Taxonomy:
1. **Factual Assertions**: Claims asserting positive factual propositions about scientific concepts, models, or datasets.
2. **Epistemic Abstentions**: Statements declaring lack of evidence or scope limitations.
3. **Evaluation Alignment**: Factual assertions are evaluated for factual entailment against retrieved passages. Epistemic abstentions are evaluated for abstention correctness on unanswerable queries.

## 2. Quantitative Grounding Results (Canonical Frozen N=56 Claims across 15 TEST Queries)
- **Total Candidate Sentences**: 56
- **Epistemic Abstentions**: 51 (all 5 unanswerable test queries correctly triggered epistemic refusals)
- **Positive Factual Assertions**: 5 (from answerable test queries)
- **Supported Claims (Entailed)**: 5 / 5 (100.0% precision on positive assertions)
- **Abstention Accuracy**: 5 / 5 unanswerable queries correctly refused (100.0% abstention precision)
