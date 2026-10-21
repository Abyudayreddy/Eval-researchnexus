# ResearchNexusAI — LLM Generation & Synthesis Engine

> **Source Implementation:** ackend/app/services/llm_provider.py & ackend/app/services/assistant/synthesis_engine.py  
> **Status:** Authoritative RAG Review Note  

---

## 1. Generation Architecture
The generation stage synthesizes verified multi-document literature reviews from retrieved passages.
- **Provider Abstraction (llm_provider.py):** Unified interface supporting Groq (llama-3.3-70b-versatile, mixtral-8x7b-32768), Google Gemini (gemini-1.5-flash), OpenAI (gpt-4o), and Anthropic Claude.
- **Deterministic Hyperparameters:** Configured with low temperature ( \approx 0.1 - 0.2$) to minimize hallucination and enforce factual grounding.

## 2. Structured Multi-Paper Synthesis
The SynthesisEngine formats prompts to enforce:
1. **Thematic Clustering:** Grouping findings across papers by methodological approach or domain findings.
2. **Inline Citation Anchors:** Emitting bracketed numeric anchors [1], [2] linking statements directly to source chunk IDs.
3. **Contrastive Phrasing:** Explicitly highlighting agreements, disagreements, and research gaps across literature.
