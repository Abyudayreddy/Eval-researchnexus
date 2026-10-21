# Iterative Synthesis Refinement Ablation & Trade-off Analysis

## 1. Empirical Impact Summary (E07 / E07.1 Historical Records)
Across the full 100-query benchmark:
- **Improved Grounding**: 1 query (1.0%)
- **Unchanged Response**: 98 queries (98.0%)
- **Degraded Grounding**: 1 query (1.0%)
- **Net Grounding Gain**: 0.0%

## 2. Latency & Resource Trade-Off
- **Baseline Synthesis Latency (p50)**: 1,420 ms
- **Refinement Pass Latency (p50)**: 2,930 ms (+106.3% latency penalty)
- **Token Cost**: +112% input/output tokens per refined query

## 3. Publication Recommendation
The empirical data clearly indicates that iterative refinement provides negligible accuracy gain while more than doubling compute latency and cost.
In the IEEE paper, this should be explicitly presented as an architectural trade-off analysis: lightweight single-pass synthesis with deterministic NLI verification is substantially more Pareto-optimal than iterative regeneration loops.
