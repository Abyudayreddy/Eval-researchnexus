# ResearchNexus AI — Module 2 Human Annotation Guidelines & Protocol

## 1. Status: HUMAN_VALIDATION_BLOCKED
In strict adherence to the empirical integrity guidelines of the ResearchNexus project, no fabricated human labels are produced. Human ground truth annotation remains **BLOCKED** due to the absence of independent human subject annotators in this execution environment.

This document and associated blank templates are provided for future independent study reproduction.

---

## 2. Annotation Task Overview
Annotators are presented with:
1. **Research Question ($Q$)**
2. **Retrieved Context Chunks ($C$)**
3. **Generated Sentences / Claims ($c_i$)** from both Condition A (Naive RAG) and Condition B (Verified RAG).

Annotators blind to condition assignment classify each claim into one of four labels:
- **`SUPPORTED`**: The factual content of the claim is directly and unambiguously substantiated by the referenced evidence chunk.
- **`PARTIALLY_SUPPORTED`**: Some facets of the claim are substantiated by the text, but minor details or extrapolations are unmentioned.
- **`CONTRADICTED`**: The claim directly contradicts facts established in the referenced evidence.
- **`UNSUPPORTED`**: The claim makes assertions completely absent from the evidence, cites a non-existent or irrelevant chunk, or lacks evidence backing.

---

## 3. Human Annotation Template Format

CSV Schema (`human_annotation_template.csv`):
```csv
query_id,condition,sentence_id,claim_text,cited_chunk_ids,human_grounding_label,annotator_notes
item_v11_086,A,s1,"...",[1],PENDING_HUMAN_LABEL,
item_v11_086,B,s1,"...",[1],PENDING_HUMAN_LABEL,
```

No synthetic or mock human labels have been or will be populated into these fields.
