# ResearchNexusAI — Corpus Ingestion & Indexing Pipeline

> **Scripts:** `chunk_corpus.py` -> `embed_corpus.py` -> `build_indexes.py`  
> **Status:** Preprocessing Pipeline Specification  

---

## 1. Sequential Pipeline Flow

```text
ResearchMind_Dataset/*.pdf
            |
            v
[ extract_text.py / extract_metadata.py ]
            |
            v
ResearchMind_LocalKB/extracted_text/*.json
            |
            v
[ chunk_corpus.py ] ──► Sliding-window token chunking with passage overlap
            |
            v
ResearchMind_LocalKB/chunks/*.json
            |
      +-----+-----+
      |           |
      v           v
[ embed_corpus.py ]  [ build_indexes.py ]
      |                    |
      v                    v
ChromaDB Vector DB    BM25 Inverted Index
(embeddings/)         (bm25_index.pkl)
```

## 2. Execution Parameters
- **Chunking Window:** Typically 256-512 tokens with 50-token overlap to maintain cross-sentence semantic context.
- **Dense Embedding Model:** `BAAI/bge-base-en-v1.5` producing 768-dim normalized vectors.
- **Lexical Index:** Rank-BM25 Okapi algorithm with lowercase tokenization and punctuation stripping.
