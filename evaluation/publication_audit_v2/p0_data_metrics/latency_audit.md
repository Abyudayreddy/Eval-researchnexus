# Latency Audit: Component Breakdown vs Post-Generation Overhead

## 1. Measurement Boundaries and Decomposition
A major issue identified in early drafts was conflating raw LLM token generation latency with multi-stage verification, claim extraction, and citation repair overhead.

### Component Latency Profile (Canonical E03 / Module 1-3)
| Pipeline Component | Measurement Boundary | p50 Latency (ms) | Mean Latency (ms) | Overhead Type |
| :--- | :--- | :---: | :---: | :--- |
| **BM25 Search** | In-memory tokenization & scoring | 0.69 | 1.12 | First-Stage Retrieval |
| **Dense Search** | Embedding inference + Chroma ANN query | 13.51 | 16.84 | First-Stage Retrieval |
| **RRF Fusion** | Reciprocal Rank calculation (k=60) | 0.12 | 0.18 | Stage Fusion |
| **BGE Reranker** | Cross-encoder sequence-pair inference (top-20) | 48.20 | 54.10 | Neural Reranking |
| **LLM Generation** | Gemini 2.5 Flash initial synthesis (temp 0.0) | 1,420.00 | 1,650.00 | Core Generation |
| **Claim Extraction** | Regex & syntactic span parsing | 4.50 | 6.20 | Post-Generation Verification |
| **Claim NLI Verification** | Multi-premise NLI entailment checks | 320.00 | 410.00 | Post-Generation Verification |
| **Citation Repair** | Deterministic bracket alignment search | 8.10 | 12.40 | Post-Generation Repair |
| **Iterative Refinement** | Secondary LLM pass (when triggered) | 1,510.00 | 1,720.00 | Optional Refinement |

### Key Findings
1. First-stage retrieval and reranking comprise under 4% of total pipeline latency (<70 ms).
2. Primary latency bottleneck is LLM generation (1.4-1.6s).
3. Post-generation verification adds an additional ~330-430 ms of deterministic latency overhead.
4. Iterative refinement, when triggered, roughly doubles total generation latency (+105% latency increase) while providing marginal empirical gain.
