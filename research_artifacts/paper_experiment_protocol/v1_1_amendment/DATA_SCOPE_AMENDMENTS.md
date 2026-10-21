# Data Scope & Cohort Amendments (V1.1 Amendment)

## 1. Executive Summary & Rationale

V1.1 clarifies the human evaluation scope boundaries and establishes a dual-cohort policy for generation evaluation to prevent conflating automated evaluation ($N=100$) with human evaluation ($N=30$) and to analyze generation performance when relevant evidence is present in context.

---

## 2. Human Evaluation Scope Boundaries

- **SYSTEM / AUTOMATED EVALUATION**: $N=100$ items (`ds_nexus_v11` ALL split). Evaluated via automated scripts.
- **HUMAN-GROUNDED EVALUATION**: $N=30$ items (15 VALIDATION, 15 TEST). Evaluated by 2 independent expert annotators + 1 senior adjudicator.
- **TEST HUMAN EVALUATION**: $N=15$ items (`ds_nexus_v11` TEST split). Dedicated frozen test subset.
- *Rule*: Automated $N=100$ evaluations MUST NEVER be described as human validated.

---

## 3. Dual-Cohort Generation Evaluation Policy

1. **Cohort A — Full Benchmark Cohort ($N=100$)**:
   - Includes all 100 evaluation queries in `ds_nexus_v11`.
   - Evaluates system performance across the complete benchmark without dropping difficult queries.

2. **Cohort B — Evidence-Eligible Subset**:
   - Queries where at least one gold-relevant paper/evidence item is present in the pre-generation retrieved context ($k \le 10$).
   - Determined strictly from frozen retrieval candidate lists **BEFORE** running generation scripts.
   - Evaluates LLM generation and claim verification quality when supporting context is available.

*Rule*: All generation results MUST be reported for Cohort A and Cohort B separately with explicit denominators.
