# ResearchNexus AI — Module 2 Deduplication & Context Formatting Policy

## 1. Deduplication Invariants
1. **Candidate Level**: Candidate chunk pools are retrieved via Module 1 frozen B3 Hybrid RRF ranking ($k=20$).
2. **Chunk Deduplication**: Chunk IDs must appear at most once in the synthesized context prompt. Duplicate appearances of the same chunk are discarded upon their first occurrence.
3. **Evidence Ranking Preservation**: The relative rank of unique retrieved chunks is strictly preserved from the B3 retrieval output (Rank 1 through $N$, $N \le 20$).

## 2. Citation Serialization Format
Evidence provided to the generator follows a standardized, immutable syntax:

```text
CITATION [i]:
Paper: <Title or Topic>
Evidence: <Cleaned Evidence Text>
```

Where:
- `[i]` is a 1-indexed sequential integer matching the context rank.
- Citation map maps bracket index string `[i]` directly to the chunk metadata dictionary `{'chunk_id', 'paper_id', 'title', 'evidence_text', ...}`.

## 3. Cryptographic Verification Policy
- Every query's serialized evidence prompt string must be hashed via SHA-256 prior to generation.
- The condition pair (Naive RAG vs Verified RAG) must yield identical `context_hash` strings:
$$\text{SHA256}(\text{Context}_{\text{Naive}}) \equiv \text{SHA256}(\text{Context}_{\text{Verified}})$$
- Any deviation in `context_hash` between conditions invalidates the test run.
