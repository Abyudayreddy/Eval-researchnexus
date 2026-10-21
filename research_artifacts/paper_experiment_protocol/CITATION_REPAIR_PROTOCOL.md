# Citation Repair Protocol (Frozen)

## 1. Overview

This document specifies the evaluation rules and metrics for automatic Citation Repair.

---

## 2. Citation Repair Metrics

1. **Citation Repair Success Rate (CRSR)**:
   $$\text{CRSR} = \frac{\text{Count of Repaired Claims Confirmed SUPPORTED by Independent NLI}}{\text{Total Claims Targeted for Citation Repair}}$$
2. **Citation Precision Delta**: $\text{Precision}_{\text{After}} - \text{Precision}_{\text{Before}}$
3. **Unsupported Claim Rate Delta**: $\text{UCR}_{\text{Before}} - \text{UCR}_{\text{After}}$

---

## 3. Strict Verification Rule

> A citation repair operation is classified as **SUCCESSFUL** if and only if independent NLI evaluation confirms that the newly assigned evidence chunk entails the final generated claim.
