# IEEE Paper Preparation Data: ResearchNexus AI

## 1. Title Suggestions
- An Explainable Research Assistant Using Hybrid Retrieval, XAI, and Enhanced RAG
- ResearchNexus AI: A System for Explainable, Context-Bound Academic Question Answering
- Integrating Hybrid Retrieval and Iterative RAG for Transparent Research Assistance
- Towards Transparent Academic Search: A Hybrid RAG Architecture with Explicit Citation Verification and Baseline-Locked Evaluation

## 2. Abstract Draft
With the rapid expansion of scientific literature, researchers increasingly rely on large language models for literature review and synthesis. However, existing retrieval-augmented generation (RAG) systems often suffer from hallucinated citations, lack of transparency, and poor retrieval for domain-specific queries. We present ResearchNexus AI, an explainable research assistant built on a hybrid retrieval architecture, an enhanced RAG pipeline, and an integrated publication evaluation console. Our approach combines sparse BM25 and dense ChromaDB retrieval using Reciprocal Rank Fusion (RRF, k=60), followed by BGE cross-encoder reranking. To ensure transparency, we implement a 10-stage local execution timeline that exposes retrieval and generation traces to the user. Additionally, the system employs context-bound generation with deterministic and semantic claim verification for citation repair, alongside a bounded iterative refinement cycle (max 2 passes). To make experimental evaluation scientifically defensible, ResearchNexus AI incorporates a dedicated Evaluation & Publication Console featuring baseline locking (`B0_LLM_ONLY` to `B7_ITERATIVE_RAG`), RRF sensitivity analysis, an ablation matrix generator, blinded human evaluation, and automatic reproducibility package export. Unmeasured metrics strictly display as **NOT MEASURED** until benchmark execution. In this paper, we describe the system design, implementation, and evaluation methodology on a multi-domain corpus of 706 papers alongside 5 online academic repositories.

## 3. Keywords
- Retrieval-Augmented Generation (RAG)
- Hybrid Retrieval
- Explainable AI (XAI)
- Scientific Document Retrieval
- Citation Verification
- Cross-Encoder Reranking
- Iterative Refinement
- Baseline-Locked Evaluation
- Reproducible AI Benchmarking

## 4. Introduction Points
- **The Problem:** Exponential growth of scientific literature makes literature reviews time-consuming, while LLMs alone hallucinate and lack up-to-date domain knowledge.
- **Current Limitations:** Existing academic search tools lack transparency in answer derivation and fail to verify claims against retrieved context. Furthermore, many research systems report unverified or cherry-picked metrics.
- **The Need for Transparency & Defensibility:** Explainability (XAI) is critical; users must trust source provenance. Evaluation must be reproducible, with immutable baseline configurations and explicit metric compatibility definitions.
- **Proposed Solution:** ResearchNexus AI introduces a context-bound, scope-enforced enhanced RAG system with a transparent 10-stage execution timeline and a dedicated Phase 3.10 Evaluation Console.
- **Key Mechanisms:** Integration of hybrid retrieval (BM25 + Dense + RRF + BGE Reranking), deterministic/semantic claim verification, iterative refinement, and baseline-locked benchmarking.

## 5. Related Work
- **General Academic Search (Google Scholar, Semantic Scholar):** Keyword/graph retrieval without generative synthesis or explainable timeline traces.
- **LLM-Based Search (Perplexity):** Generative answers with citations, but opaque retrieval mechanics and lack of explicit claim verification.
- **OpenScholar:** State-of-the-art open-source LLM for literature synthesis. ResearchNexus differentiates by emphasizing an explainable workspace, 10-stage timeline transparency, isolated personal vector collections, and an integrated evaluation console.
- **Traditional RAG:** Single-stage dense retrieval, missing exact keyword matches crucial for scientific entities.
- **Hybrid RAG & Evaluation:** ResearchNexus extends hybrid RAG with BGE cross-encoder reranking, claim verification, citation repair, and a locked baseline evaluation console.

## 6. OpenScholar Positioning Table

| Dimension | OpenScholar | ResearchNexus AI |
| :--- | :--- | :--- |
| **Scale** | Large-scale parameter model, cloud-oriented | Local/Modular (React + FastAPI + Gemini Flash) |
| **Corpus** | Massive web-scale academic corpus | Curated (706 papers, 26,179 chunks) + 5 Online Sources |
| **Retriever** | Proprietary/Optimized Dense | Hybrid (BM25 + ChromaDB) with RRF(k=60) |
| **Reranker** | Integrated/Proprietary | Explicit BGE cross-encoder (BAAI/bge-reranker-base) |
| **Iteration** | Multi-step reasoning internal to model | Explicit 2-cycle max, self-feedback, anti-oscillation |
| **Citation Verification** | Implicit in generation | Explicit: Stage A deterministic + Stage B semantic (5 statuses), citation repair |
| **XAI** | Limited trace visibility | High: 10-stage local & 8-stage online timeline with full trace transparency |
| **Evaluation Console** | Standard evaluation scripts | Integrated Console: Baseline locking (B0-B7), Ablation Matrix, Blinded Human Eval, Export Package |
| **Metric Governance** | Published offline metrics | Strict policy: Unmeasured metrics render as **NOT MEASURED** |

## 7. Proposed Method
- **System Architecture:** Modular stack comprising React 19 frontend, FastAPI backend, PostgreSQL relational/evaluation store, and ChromaDB vector store.
- **Hybrid Retrieval Pipeline:** Queries processed simultaneously by BM25 (sparse) and ChromaDB using BAAI/bge-base-en-v1.5 (dense), merged via RRF (k=60) and reranked by BAAI/bge-reranker-base.
- **Context Engine & Privacy Isolation:** 5 modes, 5 scopes, SHA-256 context hashing, immutable snapshots. Dedicated Chroma vector collection for user document uploads (Phase 3.8).
- **Enhanced RAG Generation:** Grounded prompt construction, Gemini Flash generation.
- **Claim Verification & Repair:** 6 claim types, Stage A deterministic checks + Stage B semantic LLM checks, 5 verification statuses, conservative citation repair.
- **Iterative Refinement:** Self-feedback loop (max 2 cycles) with anti-oscillation safeguards using feedback signatures.
- **Evaluation Console (Phase 3.10):**
  - **Baseline Locking:** 8 immutable baselines (`B0` to `B7`).
  - **RRF Sensitivity Study:** Automated evaluation across `k = [20, 40, 60, 100]`.
  - **Ablation Study Matrix:** Full system vs. minus individual components.
  - **Blinded Human Evaluation:** 7 rating dimensions (Relevance, Completeness, Correctness, Citation Accuracy, Clarity, Conciseness, Overall Trust).
  - **Claim Audit:** System-wide audit of publication claims.
  - **Reproducibility Export:** One-click JSON package generator.

## 8. Baselines Locked in Evaluation Console
1. **B0_LLM_ONLY:** Zero-shot Gemini Flash without context injection.
2. **B1_DENSE_RAG:** Standard ChromaDB dense retrieval + LLM.
3. **B2_BM25_RAG:** Standard BM25 sparse retrieval + LLM.
4. **B3_HYBRID_RAG:** BM25 + Dense + RRF(k=60) + LLM (no reranker).
5. **B4_HYBRID_BGE:** BM25 + Dense + RRF + BGE Reranker + LLM.
6. **B5_ENHANCED_RAG:** Hybrid + BGE Reranker + Context Engine + Enhanced RAG.
7. **B6_ENHANCED_VERIFICATION:** Enhanced RAG + Claim Verification & Citation Repair (single pass).
8. **B7_ITERATIVE_RAG:** Full system with bounded iterative refinement (max 2 passes).

## 9. Evaluation Metrics Framework
- **Retrieval Metrics:** Recall@K, Precision@K, Mean Reciprocal Rank (MRR), nDCG@K, Hit@K.
- **Generation & Faithfulness Metrics:** Claim Support Rate (%), Citation Precision (%), Citation Coverage (%), Unsupported Claim Rate (%).
- **Efficiency Metrics:** Latency breakdown (P50/P95 in ms) across retrieval, reranking, generation, verification, and total pipeline execution. Enforces realistic minimum floor (`max(..., 515.0)` ms).
- **Metric Compatibility Schema:** Each metric stores `metric_name`, `dataset`, `split`, `evaluation_protocol`, `unit`, `is_comparable`, and `comparison_note`.

## 10. Publication Tables Schema (Enforcing "NOT MEASURED" until Benchmark Run)

**Table 1: Baseline Comparison Matrix**
| Baseline ID | Description | Recall@5 | Recall@10 | Citation Precision | Claim Support Rate | Latency P50 (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B0_LLM_ONLY | Zero-shot Gemini Flash | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| B1_DENSE_RAG | Dense (ChromaDB) + LLM | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| B2_BM25_RAG | Sparse (BM25) + LLM | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| B3_HYBRID_RAG | BM25 + Dense + RRF | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| B4_HYBRID_BGE | Hybrid + BGE Reranker | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| B5_ENHANCED_RAG| Enhanced RAG Pipeline | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| B6_ENHANCED_VER| Single-pass + Verification | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| B7_ITERATIVE_RAG| Complete System (2-pass) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |

**Table 2: RRF Sensitivity Study Matrix**
| RRF k | Recall@5 | Recall@10 | MRR | nDCG@10 |
| :--- | :--- | :--- | :--- | :--- |
| k = 20 | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| k = 40 | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| k = 60 (Default) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| k = 100 | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |

**Table 3: Ablation Study Matrix**
| Variant | Citation Precision | Claim Support Rate | Latency P50 (ms) |
| :--- | :--- | :--- | :--- |
| Full System (B7) | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| - Iterative Refinement | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| - Claim Verification | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| - BGE Reranking | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| - Sparse BM25 (Dense Only) | NOT MEASURED | NOT MEASURED | NOT MEASURED |

## 11. Research Contributions
- **System Architecture:** End-to-end explainable research operating system featuring 10-stage execution timeline transparency.
- **Engineering Contribution:** Integration of hybrid retrieval (RRF k=60), BGE reranking, context scope engine with SHA-256 hashing, and isolated user upload collections.
- **Scientific & Evaluation Contribution:** First academic research assistant featuring a baseline-locked Evaluation & Publication Console with strict **NOT MEASURED** metric governance and automated reproducibility package generation.

## 12. Conclusion & Next Steps
- ResearchNexus AI provides a complete, auditable platform for scientific paper synthesis.
- The completion of Phase 3.10 provides the infrastructure needed for rigorous, reproducible benchmarking.
- Next steps involve executing benchmark runs across the multi-domain evaluation datasets and publishing empirical comparison tables.
