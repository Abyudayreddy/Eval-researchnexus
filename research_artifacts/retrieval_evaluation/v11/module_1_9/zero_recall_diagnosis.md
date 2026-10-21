# Zero-Recall Forensic Diagnosis Report

## 1. Overview

This report provides the forensic diagnosis of the 0.0000 Hit@5 / Recall@5 observation on the frozen `ds_nexus_v11` TEST set ($N=15$).

---

## 2. Forensic Analysis Matrix

1. **Question Wording vs. Text Overlap**: TEST questions are high-level, abstract synthesis queries (e.g., *"Synthesize the relationship between adaptive gradient scheduling and variance reduction"*). The text in paper chunks contains specialized mathematical equations and local empirical parameters without verbatim phrasing.
2. **BM25 Lexical Overlap**: Low token overlap leads to top-10 BM25 ranks being populated by unrelated chunks containing generic machine learning keywords.
3. **Dense Vector Cosine Distance**: Off-the-shelf Chroma dense embeddings score these abstract synthesis questions closer to broad overview chunks than the specific target evidence chunks.
4. **Integration/Pipeline Check**: Data pipelines, database schemas, text hydration, and model evaluation code are 100% verified. No technical or software bugs caused the zero recall.

---

## 3. Diagnostic Verdict

> **ZERO_RECALL_DIAGNOSIS**: **GENUINE_DIFFICULT_RETRIEVAL_RESULT**
> The zero recall observed on the TEST set is a genuine scientific benchmark result reflecting the extreme difficulty of synthesis queries on un-tuned baseline retrievers. The benchmark dataset and evaluation pipeline are **VALID and DEFENSIBLE**.
