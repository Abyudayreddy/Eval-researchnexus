# ResearchNexusAI — Tricky Reviewer Questions & Defenses

### 1. "Your BGE reranker doesn't improve Hit@20 over Hybrid. Why include it?"
- **Defense:** *"That is an accurate observation from our canonical evaluation. While Hit@20 remains at 0.867 because the top candidate pool is already captured, the cross-encoder reranker improves contextual passage ordering and precision within the prompt window, which directly aids generation grounding even when raw recall reaches an upper plateau."*

### 2. "Your Citation Repair only grounds 1 out of 5 claims. Did the repair fail?"
- **Defense:** *"Yes, our forensic audit established that rule-based citation repair was not demonstrated to be effective on this test benchmark. Rather than masking this inconvenient result or generating synthetic numbers, we locked this finding as a documented limitation in our paper, providing motivation for future agentic LLM repair loops."*

### 3. "How do you know your automated claim verifier isn't hallucinating its judgments?"
- **Defense:** *"The verifier operates on localized NLI entailment prompts with low temperature and strict context bounds. However, we explicitly acknowledge that automated verification is a proxy for human expert judgment, which is why we audited its decision matrix and placed human validation in our future work roadmap."*
