# ResearchNexus AI — Module 2 Revision 01 Metric Definitions

## 1. Unit of Analysis
The unit of analysis is:
1. **Claim Level**: For factual claim grounding, negative evidence findings, and claim support classification.
2. **Query / Answer Level**: For end-to-end abstention correctness on unanswerable and answerable items.
3. **Citation Level**: For citation precision, coverage, and repair correctness.

---

## 2. Decoupled Metric Definitions

### 2.1 Grounding Metrics (Factual Assertions Only)

Let $\mathcal{C}_{\text{fact}}$ be the set of extracted claims that are positive factual assertions ($\text{is\_factual\_assertion} = \text{True}$).

1. **Factual Claim Support Precision ($\text{FCSP}$)**:
   $$\text{FCSP} = \frac{|\{c \in \mathcal{C}_{\text{fact}} : \text{status}(c) = \text{SUPPORTED}\}|}{|\mathcal{C}_{\text{fact}}|}$$
   - **Numerator ($\text{TP}$)**: Positive factual claims verified as `SUPPORTED_FACTUAL_CLAIM`.
   - **Denominator ($\text{TP} + \text{FP}$)**: Total factual claims asserted by the system ($|\mathcal{C}_{\text{fact}}|$).
   - *Note*: If $|\mathcal{C}_{\text{fact}}| = 0$ (e.g. system completely abstains without asserting positive facts), $\text{FCSP}$ is undefined or conventionally $1.0$ (no false positive assertions made).

2. **Unsupported Factual Claim Rate ($\text{UFCR}$)**:
   $$\text{UFCR} = \frac{|\{c \in \mathcal{C}_{\text{fact}} : \text{status}(c) = \text{UNSUPPORTED}\}|}{|\mathcal{C}_{\text{fact}}|}$$
   - **Numerator ($\text{FP}$)**: Positive factual claims unsupported by evidence.
   - **Denominator**: Total positive factual claims ($|\mathcal{C}_{\text{fact}}|$).

3. **Contradiction Rate ($\text{CR}$)**:
   $$\text{CR} = \frac{|\{c \in \mathcal{C}_{\text{fact}} : \text{status}(c) = \text{CONTRADICTED}\}|}{|\mathcal{C}_{\text{fact}}|}$$

---

### 2.2 Abstention & Epistemic Finding Metrics

Let $Q_{\text{unans}}$ be the set of adversarial / unanswerable queries where retrieved context lacks the queried factual target ($N=5$, queries 96–100).
Let $Q_{\text{ans}}$ be the answerable empirical queries ($N=10$, queries 86–95).

1. **Appropriate Abstention Rate on Unanswerable Queries ($\text{AAR}_{\text{unans}}$)**:
   $$\text{AAR}_{\text{unans}} = \frac{|\{q \in Q_{\text{unans}} : \text{abstains}(q) = \text{True}\}|}{|Q_{\text{unans}}|}$$
   - **Numerator ($\text{TN}$)**: Unanswerable queries where the model correctly abstains or declares lack of evidence.
   - **Denominator**: Total unanswerable queries ($|Q_{\text{unans}}| = 5$).

2. **Insufficient Evidence Finding Rate ($\text{IEFR}$)**:
   $$\text{IEFR} = \frac{|\{c \in \mathcal{C} : \text{epistemic\_type}(c) = \text{INSUFFICIENT\_EVIDENCE\_FINDING}\}|}{|\mathcal{C}|}$$
   - Proportional frequency of meta-statements correctly identifying missing context.

3. **Hallucinated Answer Rate on Unanswerable Queries ($\text{HAR}_{\text{unans}}$)**:
   $$\text{HAR}_{\text{unans}} = \frac{|\{q \in Q_{\text{unans}} : \text{asserts\_factual\_answer}(q)\}|}{|Q_{\text{unans}}|}$$

---

### 2.3 Citation Metrics

1. **Citation Existence ($\text{CE}$)**:
   Proportion of claims that carry citation bracket tags.
2. **Citation Precision ($\text{CP}$)**:
   Proportion of cited claims where the cited chunk actually supports the claim:
   $$\text{CP} = \frac{\text{TP}_{\text{cit}}}{\text{TP}_{\text{cit}} + \text{FP}_{\text{cit}}}$$
3. **Citation Repair Safety ($\text{CRS}$)**:
   Proportion of automated citation repairs that correctly map to supporting chunks without introducing ungrounded bindings.

---

### 2.4 Separation of Automated Verifier Metrics from Human Ground Truth
- **System Verifier Metrics**: Derived automatically via Stage A deterministic matching and Stage B NLI model inference.
- **Human Ground Truth Metrics**: Derived exclusively from human expert consensus annotations. Must remain marked as `HUMAN_VALIDATION_BLOCKED` when external human annotators are unavailable.
