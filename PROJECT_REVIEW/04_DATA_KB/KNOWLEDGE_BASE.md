# ResearchNexusAI — Local Knowledge Base (ResearchMind_LocalKB)

> **Location:** `ResearchMind_LocalKB/`  
> **Status:** Indexed Knowledge Base Architecture  

---

## 1. Knowledge Base Layout
`ResearchMind_LocalKB/` houses precomputed indexes, parsed full text, metadata, and vector databases:

```text
ResearchMind_LocalKB/
|-- extracted_text/      (687 individual JSON files containing extracted PDF text)
|-- chunks/              (Domain-partitioned text passages ready for retrieval)
|-- metadata/            (Structured metadata records: title, authors, DOI, year, abstract)
|-- indexes/
|   |-- bm25_index.pkl   (Serialized Okapi BM25 index)
|   |-- bm25_mapping.json(Document ID to corpus chunk mapping table)
|   +-- chroma/          (ChromaDB collection files for dense passage embeddings)
+-- reports/             (Corpus integrity, extraction validation, and count reports)
```

## 2. Local Querying Architecture
- **In-Memory Loading (`local_evidence.py`):** On startup, `LocalEvidenceRetriever` caches `bm25_index.pkl` and `bm25_mapping.json` for microsecond lexical candidate lookups.
- **ChromaDB Client:** Connects to the local persistent directory to query 768-dimensional BGE embeddings.
- **Zero Online Dependency:** Operates fully offline without requiring real-time PDF parsing during user search.
