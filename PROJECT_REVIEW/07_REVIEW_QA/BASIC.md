# ResearchNexusAI — Basic Project Questions

### 1. What is ResearchNexusAI?
- **Answer:** ResearchNexusAI is an Explainable Multi-Stage Retrieval-Augmented Generation (RAG) framework tailored for scientific literature synthesis across multi-disciplinary research corpuses.

### 2. What problem does it solve?
- **Answer:** Traditional LLMs hallucinate citations and scientific claims when summarizing academic papers. Standard RAG frameworks also lack transparent evidence tracking and fail to verify whether generated statements are entailed by retrieved passages. ResearchNexusAI solves this via hybrid retrieval, NLI claim verification, and provenance tracking.

### 3. What corpus was used for validation?
- **Answer:** A curated corpus of 687 peer-reviewed papers spanning Artificial Intelligence, Environmental Science, and Interdisciplinary domains (Smart Cities, Digital Twins, Computational Biology) stored in `ResearchMind_Dataset`.

### 4. What is the difference between lexical and dense retrieval?
- **Answer:** Lexical retrieval (BM25) matches exact keywords and specialized terminology using inverted index term frequencies. Dense retrieval matches latent semantic concepts by comparing high-dimensional neural vector embeddings (BGE-base) using cosine similarity.
