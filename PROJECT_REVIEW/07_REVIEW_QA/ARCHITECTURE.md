# ResearchNexusAI — Architecture Questions

### 1. Why did you choose a decoupled FastAPI + React architecture?
- **Answer:** FastAPI provides asynchronous request handling, native Pydantic data validation, and high performance necessary for multi-step AI orchestration. React with TypeScript allows modular rendering of interactive XAI graphs and synthesis workspaces without full-page reloads.

### 2. How are BM25 and ChromaDB vector search merged?
- **Answer:** Via Reciprocal Rank Fusion (RRF) with smoothing parameter k=60:
  $$RRF(d) = \sum_{m \in \{BM25, Dense\}} \frac{1}{60 + r_m(d)}$$
  This operates on relative ranks rather than incompatible raw scores.

### 3. What role does BGE reranker play?
- **Answer:** It acts as a cross-encoder stage rescoring the Top-20 RRF candidates using full query-passage cross-attention before passages are packaged into the generation prompt.

### 4. Where does the verification step sit in the pipeline?
- **Answer:** It sits directly after generation and before user presentation. Synthesized text is decomposed into atomic claims, and each claim is checked for factual entailment against the retrieved evidence chunks.
