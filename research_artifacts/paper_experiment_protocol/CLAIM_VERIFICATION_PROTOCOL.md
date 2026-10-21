# Claim Verification Protocol (Frozen)

## 1. Overview

This document specifies the verification metrics and 4-class annotation protocol for NLI claim verification.

---

## 2. Claim Classification Classes

1. **`SUPPORTED`**: The cited evidence chunk directly entails the extracted claim.
2. **`PARTIALLY_SUPPORTED`**: The evidence chunk contains partial premise support but lacks full scope entailment.
3. **`UNSUPPORTED`**: The evidence chunk contains no relevant premises or mentions of the claim.
4. **`CONTRADICTED`**: The evidence chunk explicitly contradicts the claim assertion.

---

## 3. Verification Performance Metrics

- **Verification Precision**: Ratio of correctly predicted class labels to total predicted class labels.
- **Verification Recall**: Ratio of correctly predicted class labels to total gold annotated labels.
- **Verification F1**: Harmonic mean of Precision and Recall.
- **False Positive Rate (FPR)**: Rate at which unsupported/contradicted claims are incorrectly classified as `SUPPORTED`.
- **False Negative Rate (FNR)**: Rate at which supported claims are incorrectly classified as `UNSUPPORTED`.
- **Unsupported Claim Detection Rate**: Recall specifically on `UNSUPPORTED` + `CONTRADICTED` class instances.
