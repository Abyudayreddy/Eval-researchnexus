# ResearchNexus AI — Module 3 Historical Result Reconciliation

## 1. Executive Summary
Prior to this controlled evaluation, earlier project phases reported citation repair metrics under varying benchmark splits and protocols (notably in `research_artifacts/citation_evaluation/v11/e06_1_corrected/` and `e06_citation_repair/`).

This document reconciles historical findings against Module 3's controlled protocol on the frozen TEST split ($N=15$).

---

## 2. Status Classification of Historical Artifacts

| Historical Artifact | Historical Claim | Module 3 Controlled Status | Scientific Reconciliation |
| :--- | :--- | :--- | :--- |
| **`e06_citation_repair`** | 100% repair success rate reported across synthetic sample sets. | **SUPERSEDED** | The historical E06 run used synthetic test queries with single exact text injections. On the frozen benchmark `ds_nexus_v11`, conservative repair strictly prevents ambiguous multi-chunk assignments. |
| **`e06_1_corrected`** | 0 repairs applied on TEST queries (`item_v11_086` to `item_v11_100`). | **REPRODUCED** | Module 3 exactly reproduces this result: on the frozen TEST split, 0 false citations were added because candidate text matches spanned multiple papers, correctly triggering the conservative ambiguity constraint. |
| **E04.1 Citation Precision** | Reported 1.0 (100%) citation precision on Naive RAG. | **REPRODUCED WITH LIMITATION** | Reproduced exactly. However, Module 3 clarifies that this 1.0 precision was derived from a single cited claim (`item_v11_089`), and thus has low statistical power ($N=1$). |

---

## 3. Methodological Differences & Confounders Identified
1. **Multi-Chunk Lexical Redundancy**: In synthetic benchmarks, target phrases exist in exactly one chunk. In the real scientific KB (`ResearchMind_LocalKB`), foundational background claims (e.g. *"scaling challenges and novel loss function"*) occur in multiple interrelated papers across AI subfields. The conservative repair algorithm's condition `len(matching_evidence) == 1` correctly rejected all 4 candidate repairs, preventing arbitrary citation binding.
2. **Epistemic Refusal Separation**: Historical runs attempted repair on negative findings and refusals. Module 3 formally marked these as `not_eligible`, establishing that citation repair should never be forced onto statements of non-existence.
