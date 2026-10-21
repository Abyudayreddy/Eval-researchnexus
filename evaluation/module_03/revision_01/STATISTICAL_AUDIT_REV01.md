# ResearchNexus AI — Module 3 Revision 01: Statistical Audit

## 1. Audit Scope & Statistical Units
This audit reviews every statistical metric, paired comparison, sample size, and hypothesis test in Module 3. It enforces correct statistical units, removes inappropriate tests (such as McNemar on continuous/fractional rates), and explicitly labels low-power and inestimable metrics.

---

## 2. Statistical Unit & Hypothesis Test Inventory

| Metric / Comparison | Statistical Unit | Sample Size ($N$) | Observed Values | Statistical Test | Inference Status |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Citation Precision (C0 vs C1 vs C2)** | Citation marker | $N = 1$ citation | C0: $1.000$<br>C1: $1.000$<br>C2: $1.000$ | Descriptive exact match | **DESCRIPTIVE / VERY LOW POWER** ($N=1$). Insufficient to establish generalized citation precision. |
| **Citation Coverage (C0 vs C1 vs C2)** | Factual claim | $N = 5$ eligible factual claims | C0: $20.0\%$ (1/5)<br>C1: $20.0\%$ (1/5)<br>C2: $20.0\%$ (1/5) | Paired difference ($\Delta = 0$) | **DESCRIPTIVE / LOW POWER** ($N=5$). Coverage did not change across conditions (**NOT OBSERVED**). |
| **Repair Opportunity Rate** | Uncited factual claim | $N = 4$ uncited factual claims | 0 actionable opportunities / 4 uncited claims | Exact count | **CONFIRMATORY WITHIN BENCHMARK** (0/4 actionable). |
| **Repair Effectiveness (Success Rate)** | Actionable repair opportunity | $N = 0$ actionable opportunities | 0 repairs applied | Inestimable ($0/0$) | **NOT ESTIMABLE / NOT DEMONSTRATED** ($0/0$). No repairs applied. |
| **Successful-Repair Safety** | Applied repair | $N = 0$ applied repairs | 0 incorrect repairs | Inestimable ($0/0$) | **NOT ESTIMABLE** ($0/0$). Cannot calculate a repair false-positive rate from 0 incorrect / 0 applied. |
| **Ambiguous Candidate Rejection** | Ambiguous candidate claim | $N = 4$ ambiguous claims | 4 rejected ($100\%$) | Exact Binomial | **OBSERVED CONSERVATIVE REJECTION** (4/4 multi-chunk ambiguous candidates safely rejected). |
| **Provenance Completeness** | Validated citation | $N = 1$ validated citation | 1 complete chain ($100\%$) | Exact trace | **DESCRIPTIVE** ($N=1$). Complete provenance observed for the validated citation in the sample. |
| **Post-Generation Processing Overhead** | Query-level paired latency | $N = 15$ paired queries | Validation only: $+1,397.50$ ms mean<br>Validation + repair: $+1,434.68$ ms mean | Paired Wilcoxon signed-rank / Paired t-test | **STATISTICALLY SIGNIFICANT OVERHEAD** ($p < 0.001$). Added processing overhead is statistically detectable. |

---

## 3. Explicit Prohibitions & Removals
1. **McNemar Test**: Must NOT be applied to fractional citation coverage ($20\%$) or continuous latency. McNemar is strictly for $2\times 2$ binary discordant matrices.
2. **"Repair Safety: Statistically Powered"**: Formally **REMOVED**. Because zero repairs were applied, successful-repair safety is mathematically inestimable ($0/0$). No inferential significance may be assigned to a zero-repair denominator.
3. **Generalization Warnings**: All citation metrics derived from $N=1$ citation and $N=5$ factual claims are strictly marked **DESCRIPTIVE / VERY LOW POWER**.
