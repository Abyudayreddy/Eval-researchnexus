# ResearchNexus AI — Module 2 Metric Definitions

## 1. Scope and Objective
This document defines the formal mathematical metrics, verification states, and evaluation protocols for Module 2: Controlled Answer Grounding & Claim Verification Evaluation.

Module 2 tests the research question:
> *Does claim-level verification and citation validation improve factual grounding compared with conventional context-bounded RAG, given the identical frozen retrieval evidence, question, model (Gemini 2.5 Flash), and prompt conditions?*

---

## 2. Experimental Conditions

- **Condition A (`NAIVE_RAG`)**:
  - Input: User Query $Q$, Frozen Candidate Evidence Context $C$ ($k=20$, B3 Hybrid RRF).
  - Generation: Direct LLM generation from frozen evidence context prompt.
  - Evaluation: Canonical sentence-level claim extraction $\rightarrow$ Stage A deterministic verification $\rightarrow$ Stage B semantic verification. (No verification feedback loop or citation repair applied to output).

- **Condition B (`VERIFIED_RAG`)**:
  - Input: Identical User Query $Q$, Identical Frozen Candidate Evidence Context $C$ (`context_hash` match).
  - Generation: Draft generation $\rightarrow$ Claim extraction $\rightarrow$ Stage A deterministic verification $\rightarrow$ Stage B semantic NLI verification $\rightarrow$ Conservative `CitationRepair` $\rightarrow$ Independent Post-Repair NLI Re-verification.
  - Output: Verified synthesized answer with citation markers.

---

## 3. Mathematical Metric Definitions

### 3.1 Claim Support Rate (CSR)
The proportion of atomic claims extracted from the answer that are verified as strictly `SUPPORTED` by the attributed evidence chunk.

$$\text{CSR} = \frac{|\{c \in \mathcal{C} : \text{status}(c) = \text{SUPPORTED}\}|}{|\mathcal{C}|}$$

Where:
- $\mathcal{C}$ is the set of all atomic claims extracted from the answer.
- If $|\mathcal{C}| = 0$, $\text{CSR} = 0.0$ by convention.

### 3.2 Unsupported Claim Rate (UCR)
The proportion of atomic claims extracted from the answer that lack empirical backing, have invalid/missing citations, or are determined to be unsupported/hallucinatory.

$$\text{UCR} = \frac{|\{c \in \mathcal{C} : \text{status}(c) = \text{UNSUPPORTED}\}|}{|\mathcal{C}|}$$

Note: In a binary partitioned verification model, $\text{CSR} + \text{UCR} \le 1.0$ (with partial support or insufficient evidence accounting for the remainder).

### 3.3 Citation Precision (CP)
The ratio of citations that accurately substantiate the specific claims they annotate to the total citations present.

$$\text{CP} = \frac{\sum_{c \in \mathcal{C}_{\text{cited}}} \mathbb{I}(\text{status}(c) \in \{\text{SUPPORTED}, \text{PARTIALLY\_SUPPORTED}\})}{|\mathcal{C}_{\text{cited}}|}$$

Where $\mathcal{C}_{\text{cited}}$ denotes claims carrying one or more explicit citation markers. If $|\mathcal{C}_{\text{cited}}| = 0$, $\text{CP} = 0.0$.

### 3.4 Citation Coverage (CC)
The proportion of claims in the generated answer that contain valid citation markers.

$$\text{CC} = \frac{|\mathcal{C}_{\text{cited}}|}{|\mathcal{C}|}$$

### 3.5 Abstention Rate on Unanswerable Queries (AR)
The rate at which the system abstains from making substantive factual claims when the retrieved context lacks gold evidence (specifically queries `item_v11_096` through `item_v11_100`).

$$\text{AR} = \frac{1}{|Q_{\text{unans}}|} \sum_{q \in Q_{\text{unans}}} \mathbb{I}(\text{abstains}(q))$$

---

## 4. Statistical Testing Protocol

1. **Paired Comparison**:
   All 15 TEST queries are evaluated under identical context hashes.
2. **Bootstrap 95% Confidence Intervals**:
   1,000 resamples with replacement computed for CSR and UCR across conditions.
3. **Paired Hypothesis Testing**:
   - Wilcoxon signed-rank test and McNemar's exact/discordant test for paired differences in claim support and ungrounded claim occurrence.
   - Significance threshold: $\alpha = 0.05$.
