# Statistical Analysis Plan (Frozen)

## 1. Overview

This document defines the statistical testing rules for continuous IR metrics and binary claim outcomes.

---

## 2. Statistical Procedures by Metric Type

1. **Continuous IR Metrics (MRR, NDCG@5)**:
   - **Procedure**: Paired two-tailed Student's t-test and Wilcoxon signed-rank test.
   - **Reporting**: $N$, Mean, Median, Absolute Delta, 95% Confidence Interval, $p$-value.
   - **Scope Rule**: Report $p$-values on DEVELOPMENT split ($N=70$) and ALL benchmark ($N=100$). Do NOT report $p$-values on TEST split ($N=15$) if zero variance occurs.

2. **Binary Claim & Citation Outcomes (Claim Support Rate, Success Rate)**:
   - **Procedure**: McNemar's test for paired binary outcomes and Chi-square test.
   - **Reporting**: $N$, Proportion %, Absolute Delta, 95% Score Confidence Interval.
