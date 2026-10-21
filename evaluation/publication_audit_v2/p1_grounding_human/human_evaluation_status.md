# Human Evaluation Status: Validation Blocked

## 1. Formal Status: HUMAN_VALIDATION_BLOCKED / NOT_MEASURED
In accordance with absolute scientific integrity rules:
- **No external double-blind human annotations exist** in the repository.
- Synthesizing, simulating, or fabricating human annotator scores, Cohen's kappa, or Fleiss' kappa is strictly prohibited.
- Human ground truth validation is formally declared **BLOCKED / NOT_MEASURED**.

## 2. Annotation Package Prepared
To facilitate future peer-reviewed empirical validation, a complete double-blind annotation package has been constructed in `human_annotation_package/`:
1. `annotation_guidelines.md`: Explicit 3-page scoring guide covering claim entailment, citation validity, and hallucination taxonomy.
2. `blinded_30_item_sample.json`: Stratified sample of 30 generated scientific synthesis claims (15 factual, 15 epistemic/abstention) with identifiers blinded.
3. `annotation_template.csv`: Standardized annotation sheet with required fields for dual independent annotators and adjudicator reconciliation.
