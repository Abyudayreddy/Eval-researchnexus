# ResearchNexusAI — Claim Verification Engine

> **Source Implementation:** ackend/app/services/assistant/claim_verifier.py & claim_extractor.py  
> **Status:** Authoritative RAG Review Note  

---

## 1. Why Claim Verification?
Standard RAG pipelines generate fluent text that may contain subtle hallucinations or ungrounded claims. ResearchNexusAI adds an explicit automated verification gate between generation and final output presentation.

## 2. Verification Procedure
`	ext
Synthesized Response
       │
       ▼
[ claim_extractor.py ] ────► Decomposes response into atomic factual statements
       │
       ▼
[ claim_verifier.py ] ─────► Natural Language Inference (NLI) against retrieved chunks
       │
       ├─────────────────────┬─────────────────────┐
       ▼                     ▼                     ▼
   ENTAILED             CONTRADICTED          UNVERIFIED
(High confidence      (Direct conflict     (Context lacks
 context support)      with evidence)       sufficient proof)
       │                     │                     │
       ▼                     ▼                     ▼
 Green Citation Badge   Red Warning Badge   Citation Repair Candidate
`

## 3. Metrics Calculated
- **Grounding Precision:** Ratio of verified claims to total generated claims.
- **Grounding Recall:** Ratio of verified claims to all eligible factual ground-truth points.
