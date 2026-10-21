# ResearchNexus AI — Module 2 Revision 01: Human Validation Status

## 1. Status Determination: HUMAN_VALIDATION_BLOCKED
In adherence to the strict empirical rules of the ResearchNexus project, no synthetic or simulated human ratings are generated. Because independent human subject annotators are not available in this CLI environment, human ground-truth validation remains formally **BLOCKED**.

---

## 2. Dependency Matrix: Automated Verifier vs. Human Ground Truth

| Metric | Automatic Result Available? | Independent Human Validation Required? | Human Validation Available? | Publication-Safe Claim Status |
| :--- | :---: | :---: | :---: | :--- |
| **Claim Support Rate (CSR)** | Yes (Deterministic + NLI) | Yes (for factual accuracy claim) | **No** | **Prohibited from claiming verified truth** |
| **Factual Claim Precision** | Yes | Yes | **No** | **Report as automated verifier outcome only** |
| **Citation Correctness** | Yes (heuristic overlap) | Yes (for binding validity) | **No** | **Report as lexical/semantic overlap only** |
| **Appropriate Abstention** | Yes (regex & gold check) | Preferred (for linguistic nuance) | Partial (Gold labels exist) | **Safe to report 5/5 abstention on benchmark** |
| **Context Hash Equivalence** | Yes (SHA-256) | No (cryptographic proof) | Yes | **Publication-Safe** |
| **Pipeline Latency** | Yes (wall-clock timer) | No | Yes | **Publication-Safe** |

---

## 3. Human Annotation Package Specifications
The directory `evaluation/module_02/revision_01/human_annotation/` contains:
- `annotation_guidelines.md`: Protocols for independent raters.
- `annotation_template.json`: Blinded annotation schema.
- `sample_selection.json`: 30-item evaluation sample covering synthesis, numerical checks, and unanswerable queries.
- `annotator_1/`: Directory for Annotator 1 submissions (currently empty).
- `annotator_2/`: Directory for Annotator 2 submissions (currently empty).
- `adjudicated/`: Directory for adjudicated consensus labels (currently empty).

Inter-annotator agreement (Cohen's Kappa / Fleiss' Kappa) will only be computed if and when real independent human raters submit labels.
