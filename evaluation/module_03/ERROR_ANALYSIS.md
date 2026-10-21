# ResearchNexus AI — Module 3 Error Analysis

## 1. Overview & Categorization
This error analysis documents the 13 formal failure modes and behavioral bottlenecks identified during Module 3's controlled evaluation on the frozen TEST split ($N=15$).

---

## 2. Failure Mode Breakdown

| Failure Mode | Count | % of Claims | Representative Example | Root Cause | Remediation Path |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **A. Missing Citation** | 4 | 14.3% | `item_v11_091` claim 01 (state that models face scaling challenges) | LLM generated multi-bracket string `[1, 3, 5...]` not parsed as single citation marker. | Evaluation parsing enhancement for multi-brackets. |
| **B. Incorrect Citation** | 0 | 0.0% | None observed | N/A | Maintained by strict NLI and deterministic filters. |
| **C. Partial Citation** | 0 | 0.0% | None observed | N/A | N/A |
| **D. Wrong-Paper Citation** | 0 | 0.0% | None observed | N/A | Prevented by invariant local chunk indexing. |
| **E. Wrong-Evidence Citation** | 0 | 0.0% | None observed | N/A | Prevented by exact chunk ID resolution. |
| **F. Numerical Mismatch** | 10 | 35.7% | `item_v11_086` claim 01 ("92.4% Precision@5") | The query asked about a metric absent from evidence. | Epistemic refusal (valid system behavior). |
| **G. Citation Repair False Positive** | 0 | 0.0% | None observed | Conservative rule `len(matching_evidence) == 1` rejected candidates. | Desired safety feature. |
| **H. Citation Repair Ambiguity** | 4 | 14.3% | `item_v11_090` claim 02 (10 candidate matches in context) | Multiple chunks shared the phrase "scaling challenges... novel loss function". | Disambiguation requires semantic re-ranking. |
| **I. Provenance Break** | 0 | 0.0% | None observed | All citations trace to valid local KB chunk IDs. | Architecture maintains stable provenance keys. |
| **J. Metadata Mismatch** | 0 | 0.0% | None observed | Invariant chunk JSON schema. | Verified. |
| **K. Unsupported Factual Proposition** | 0 | 0.0% | None observed | Model did not hallucinate affirmative facts. | Verified. |
| **L. Appropriate Uncited Abstention** | 15 | 53.6% | `item_v11_086` claim 02 ("Therefore, I cannot answer") | Model correctly refused to answer ungrounded queries. | Handled via epistemic taxonomy. |
| **M. Insufficient-Evidence Finding** | 9 | 32.1% | `item_v11_086` claim 01 ("there is no mention of...") | Model documented absence of queried metric. | Handled via epistemic taxonomy. |

---

## 3. In-Depth Analysis of Key Behaviors

### 3.1 Why Zero False Citations Were Introduced (Repair Safety)
The `CitationRepair` algorithm requires that an uncited claim matches *exactly one* chunk in the retrieved context pool:
```python
if len(matching_evidence) == 1:
    # apply repair
```
In `item_v11_090`, `item_v11_091`, `item_v11_094`, and `item_v11_095`, the phrase *"face scaling challenges and formulate a novel loss function combining contrastive optimization and adaptive gradient scheduling"* appeared across multiple papers in the retrieved top-20 context. Consequently, `len(matching_evidence)` was 10. The repair algorithm safely declined to guess which specific paper was intended, resulting in 0 incorrect repairs.

### 3.2 Numerical Claim Integrity
Queries 86–95 explicitly probed whether models achieved specific numerical thresholds (e.g. 92.4% Precision@5 or 99.9% accuracy). In 100% of cases, the validation system verified that no chunk substantiated these numerical values, preventing false-positive entailment bindings.
