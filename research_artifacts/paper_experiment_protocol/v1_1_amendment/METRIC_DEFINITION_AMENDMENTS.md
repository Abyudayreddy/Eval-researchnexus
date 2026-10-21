# Metric Definition Amendments (V1.1 Amendment)

## 1. Executive Summary & Rationale

In V1.0, the term "Verification Precision" was ambiguously used to describe overall multiclass prediction accuracy ($\text{correct} / \text{total}$). In V1.1, this definition is replaced with standard IR/NLI multiclass precision, recall, and F1 definitions per class, alongside macro-aggregated metrics and confusion matrix reporting.

Additionally, a secondary metric **Citation Coverage** is added to complement Citation Precision and Citation Completeness.

---

## 2. Corrected Claim Verification Metrics

### 2.1 Four Ground Truth Classes
- `SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONTRADICTED`

### 2.2 Per-Class Metrics ($c \in \{\text{SUP}, \text{PART}, \text{UNSUP}, \text{CONT}\}$)
- **Precision$_c$**: $\frac{TP_c}{TP_c + FP_c}$
- **Recall$_c$**: $\frac{TP_c}{TP_c + FN_c}$
- **F1$_c$**: $\frac{2 \cdot \text{Precision}_c \cdot \text{Recall}_c}{\text{Precision}_c + \text{Recall}_c}$

### 2.3 Macro-Aggregated Metrics
- **Macro Precision**: $\frac{1}{4} \sum_{c} \text{Precision}_c$
- **Macro Recall**: $\frac{1}{4} \sum_{c} \text{Recall}_c$
- **Macro F1**: $\frac{1}{4} \sum_{c} \text{F1}_c$
- **Multiclass Confusion Matrix**: $4 \times 4$ matrix plotting predicted vs. gold labels.

### 2.4 Unsupported / Contradicted Claim Detection Metrics
- **Binary Target**: $c \in \{\text{UNSUPPORTED}, \text{CONTRADICTED}\}$
- **Detection Precision**: $\frac{TP_{\text{unsup}}}{TP_{\text{unsup}} + FP_{\text{unsup}}}$
- **Detection Recall**: $\frac{TP_{\text{unsup}}}{TP_{\text{unsup}} + FN_{\text{unsup}}}$
- **Detection F1**: Harmonic mean of Detection Precision and Detection Recall.

---

## 3. Secondary Citation Metrics

1. **Citation Precision (CP)**:
   $$\text{CP} = \frac{\text{Count of Citations Pointing to Entailing Evidence}}{\text{Total Inline Citations in Generated Text}}$$

2. **Citation Completeness (CC)**:
   $$\text{CC} = \frac{\text{Count of Supported Claims With Valid In-Text Citations}}{\text{Total Supported Claims in Generated Text}}$$

3. **Citation Coverage (COV)** *(New in V1.1)*:
   $$\text{COV} = \frac{\text{Count of Claims Requiring Citation With Valid Supporting Citation}}{\text{Total Claims Requiring Citation in Generated Text}}$$

*Rule*: All three citation metrics MUST be reported separately.
