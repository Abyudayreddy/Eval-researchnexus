# ResearchNexus AI — Module 2 Revision 01: Statistical Unit Audit

## 1. Audit Objective & Scope
This audit scrutinizes every statistical test, paired comparison, confidence interval, and sample size cited in Module 2 Revision 01. Its purpose is to guarantee that:
1. The mathematical unit of analysis is explicit and appropriate for each test.
2. No continuous metric is evaluated using an inapplicable discrete test (e.g. McNemar's test on continuous proportions).
3. Statistical inferences drawn from small sample sizes ($N=15$ queries, $N=7$ to $9$ factual assertions) are rigorously identified as **LOW-POWER / DESCRIPTIVE**, rather than presented as confirmatory proof.

---

## 2. Inventory of Evaluated Tests & Metrics

| Test | Operational Metric | Mathematical Unit of Analysis | Sample Size ($N$) | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_1$) | $p$-value / CI | Statistical Power & Inference Status |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **Wilcoxon Signed-Rank Test** | Factual Claim Support Precision | Query-level paired precision ($p_{\text{ver}} - p_{\text{naive}}$) | $N = 15$ queries (15 pairs) | Median paired difference $\Delta = 0$ | Median paired difference $\Delta \ne 0$ | $p = 1.000$ | **LOW-POWER / DESCRIPTIVE**. Precision was 1.0 across all non-empty pairs; zero discordant variation exists. |
| **Bootstrap Resampling (1,000 iter)** | Factual Claim Precision 95% CI | Query-level mean precision | $N = 15$ queries | N/A (Parameter Estimation) | N/A | Naive: $[1.0, 1.0]$<br>Verif: $[1.0, 1.0]$ | **DESCRIPTIVE**. Narrow interval reflects uniform lack of false positive assertions in test answers. |
| **Bootstrap Resampling (1,000 iter)** | Legacy Claim Support Rate (CSR) | Claim-level binary support indicator | $N = 56$ claims | N/A (Parameter Estimation) | N/A | Naive: $[0.0, 0.067]$<br>Verif: $[0.0, 0.0]$ | **CONFOUNDED**. Metric conflated refusals with hallucinations. Retained for historical comparison only. |
| **McNemar's Test (Historical Audit)** | Binary Presence of Any Unsupported Claim | Query-level binary discordance ($2\times 2$) | $N = 15$ queries ($b=0, c=0$) | Discordant proportion $P(b) = P(c)$ | Discordant proportion $P(b) \ne P(c)$ | $p = 1.000$ | **INVALID AS CSR TEST**. Evaluated query-level binary thresholding, not continuous support rate. Formally removed from CSR interpretation. |
| **Exact Binomial / Proportion Test** | Appropriate Abstention Rate on Unanswerable Items | Query-level binary abstention | $N = 5$ unanswerable queries | Abstention probability $P \le 0.5$ | Abstention probability $P > 0.5$ | $p = 0.03125$ ($5/5$) | **CONFIRMATORY WITHIN BENCHMARK**. Demonstrates consistent refusal on adversarial items ($5/5$). |

---

## 3. Findings on Factual Claim Count (4 Naive vs. 3 Verified, plus 2 Compound)
- Total extracted claims across both systems: $N = 56$ (28 Naive, 28 Verified).
- Affirmative factual claims: $N = 4$ Naive, $N = 3$ Verified (plus $1$ compound sentence in each system).
- **Audit Determination**: The small count of affirmative factual propositions is **genuinely representative of the generated answers on this split**. Because 100% of the TEST queries probed metrics absent from the evidence, the generator produced epistemic refusals for the majority of queries, asserting background literature facts in only 3 to 4 instances.
- **Statistical Power Warning**: Any hypothesis test conducted specifically on the subset of affirmative factual assertions is based on fewer than 10 total sentences. Therefore, all such tests are formally designated **DESCRIPTIVE AND LOW-POWER**.
