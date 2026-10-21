# ResearchNexusAI — 2-Minute Technical Summary

> **Problem:**
> *"When researchers use LLMs to survey scientific literature, models frequently fabricate citations, fail to notice contradictions between studies, and present summaries without verifiable provenance.*
>
> **Our Solution:**
> *To address this, we engineered ResearchNexusAI, a multi-stage RAG framework built on FastAPI and React TypeScript. Our pipeline operates across three technical stages:*
>
> 1. *First, **Hybrid Retrieval with Reciprocal Rank Fusion (RRF)**: We index 687 full-text scientific papers across AI, Environmental Science, and Interdisciplinary domains. We query Okapi BM25 and BGE dense vector embeddings in parallel, fusing them with an RRF constant of k=60. This achieves a verified Hit@20 of 86.7% (78/90 queries) on our canonical benchmark.*
>
> 2. *Second, **Generation & Automated Claim Verification**: Top passages are rescored using a BGE cross-encoder and passed to our LLM synthesis engine. Before the response is shown to the user, an automated Natural Language Inference verifier breaks the response into atomic propositions and checks factual entailment against source chunks, attaining 88.4% grounding precision.*
>
> 3. *Third, **Explainable AI Provenance**: Every statement is visually linked back to exact document chunks, bounding boxes, and similarity scores on an interactive provenance graph.*
>
> *Our framework provides researchers with transparent, verifiable scientific literature synthesis backed by reproducible canonical evaluation."*
