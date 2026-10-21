# XAI Provenance Amendments (V1.1 Amendment)

## 1. Executive Summary & Rationale

Antigravity support for online/web search integration requires extending the XAI provenance model to support both local database chunk traces and online web provider traces.

---

## 2. Expanded Provenance Models

### 2.1 Local Database Trace Chain
$$\text{Final Claim} \longrightarrow \text{Inline Citation} \longrightarrow \text{Evidence Block Text} \longrightarrow \text{Chunk ID / Paper ID} \longrightarrow \text{BGE Score} \longrightarrow \text{RRF Rank} \longrightarrow \text{Retrieval Source (BM25/Dense)}$$

### 2.2 Online Web Search Trace Chain
$$\text{Final Claim} \longrightarrow \text{Inline Citation} \longrightarrow \text{Evidence Block Text} \longrightarrow \text{Normalized Source ID} \longrightarrow \text{Search Provider} \longrightarrow \text{Original Result URL/Title} \longrightarrow \text{Retrieval Timestamp}$$

---

## 3. XAI Evaluation Metrics

1. **Trace Completeness**: Fraction of generated answer claims where all applicable links for the source type (Local or Online) resolve successfully down to raw source records.
2. **Trace Resolution Accuracy**: Accuracy of exact text character-offset matching between evidence block quotes and underlying source documents.
3. **Claim-to-Evidence Link Accuracy**: Precision of linking extracted claims to correct supporting evidence paragraphs.
4. **Citation-to-Evidence Link Accuracy**: Precision of linking inline citations to entailing evidence blocks.
