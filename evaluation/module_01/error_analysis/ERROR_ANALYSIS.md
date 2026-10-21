# Module 1: Comprehensive Error Analysis & Rank Forensic Report

## 1. Executive Summary

This error analysis investigates the exact retrieval and ranking dynamics across the four evaluated configurations (**B1: BM25**, **B2: Dense BGE-1.5**, **B3: Hybrid RRF**, and **B4: BGE Cross-Encoder**) across the 15 frozen TEST queries in `ds_nexus_v11`.

### Key Findings:
1. **Adversarial & Unanswerable Queries ($N=5$)**:
   - Queries `item_v11_096` through `item_v11_100` are intentionally unanswerable/adversarial queries with zero gold papers and zero gold evidence passages.
   - All 4 retrievers correctly produce zero false-positive hits on these queries, validating the robustness of the benchmark and consistency checker.
2. **Dense Semantic Failure Mode on Exact Benchmarking Terminology ($N=10$)**:
   - On the 10 answerable TEST queries (`item_v11_086` through `item_v11_095`), pure Dense retrieval (**B2**) failed completely ($\text{Recall@20} = 0.0000$, $\text{Hit@20} = 0.0000$).
   - **Root Cause**: The queries feature precise empirical and numerical terminology (e.g. *"adaptive gradient scheduling formulation and the resulting 92.4% Precision@5"*). Bi-encoder vector representations map these queries into broad Deep Learning semantic clusters in the 26,179-chunk corpus, missing the specific paper containing the exact mathematical formulation.
3. **BM25 Lexical Precision**:
   - Pure BM25 (**B1**) successfully retrieved the gold paper within the top 10 for all 10 answerable queries ($\text{Recall@10} = 1.0000$, $\text{Hit@10} = 0.6667$ across all 15 queries).
   - Ranks for the gold papers under BM25 ranged between rank 8 and rank 9.
4. **RRF Rank Dynamics ($k=60$)**:
   - In **B3**, fusing the top-50 BM25 list with the top-50 Dense list pushed the gold paper down from ranks 8–9 to ranks 15–17.
   - **Root Cause**: Because Dense retrieval scored the gold paper at rank $>50$ (score $0.0$), high-ranking Dense false-positive chunks received RRF scores $\ge \frac{1}{60 + 1} = 0.01639$, interleaving above the BM25-only gold paper.
   - However, **B3 preserved 100% Recall@20** among answerable queries, guaranteeing that the gold document remained in the candidate pool for the cross-encoder.
5. **BGE Cross-Encoder Reranking Dynamics (B3 $\rightarrow$ B4)**:
   - When evaluating the top-20 B3 candidates, BGE cross-encoder reranked the items:
     - **Promoted Gold Document** (4 queries):
       - `item_v11_088`: Rank 17 $\rightarrow$ Rank 12 ($+5$ positions)
       - `item_v11_089`: Rank 17 $\rightarrow$ Rank 11 ($+6$ positions)
       - `item_v11_092`: Rank 17 $\rightarrow$ Rank 13 ($+4$ positions)
       - `item_v11_093`: Rank 17 $\rightarrow$ Rank 12 ($+5$ positions)
     - **Demoted Gold Document** (4 queries):
       - `item_v11_086`: Rank 15 $\rightarrow$ Rank 18 ($-3$ positions)
       - `item_v11_090`: Rank 17 $\rightarrow$ Rank 19 ($-2$ positions)
       - `item_v11_091`: Rank 15 $\rightarrow$ Rank 17 ($-2$ positions)
       - `item_v11_095`: Rank 17 $\rightarrow$ Rank 18 ($-1$ position)
     - **Unchanged Rank** (2 queries):
       - `item_v11_087`: Rank 17 $\rightarrow$ Rank 17
       - `item_v11_094`: Rank 17 $\rightarrow$ Rank 17

---

## 2. Per-Query Gold Paper Rank Forensic Table

| Query ID | Gold Paper ID | Expected Evidence Chunks | B1 (BM25) Rank | B2 (Dense) Rank | B3 (RRF) Rank | B4 (BGE) Rank | BGE Movement |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `item_v11_086` | `paper_res_032` | 2 chunks (`chunk_001`, `chunk_002`) | **8** | Miss ($>50$) | 15 | 18 | Demoted ($-3$) |
| `item_v11_087` | `paper_res_033` | 2 chunks (`chunk_001`, `chunk_002`) | **9** | Miss ($>50$) | 17 | 17 | Unchanged ($0$) |
| `item_v11_088` | `paper_res_034` | 2 chunks (`chunk_001`, `chunk_002`) | **9** | Miss ($>50$) | 17 | **12** | **Promoted ($+5$)** |
| `item_v11_089` | `paper_res_035` | 2 chunks (`chunk_001`, `chunk_002`) | **9** | Miss ($>50$) | 17 | **11** | **Promoted ($+6$)** |
| `item_v11_090` | `paper_res_036` | 2 chunks (`chunk_001`, `chunk_002`) | **9** | Miss ($>50$) | 17 | 19 | Demoted ($-2$) |
| `item_v11_091` | `paper_res_032` | 1 chunk (`chunk_002`) | **8** | Miss ($>50$) | 15 | 17 | Demoted ($-2$) |
| `item_v11_092` | `paper_res_033` | 1 chunk (`chunk_002`) | **9** | Miss ($>50$) | 17 | **13** | **Promoted ($+4$)** |
| `item_v11_093` | `paper_res_034` | 1 chunk (`chunk_002`) | **9** | Miss ($>50$) | 17 | **12** | **Promoted ($+5$)** |
| `item_v11_094` | `paper_res_035` | 1 chunk (`chunk_002`) | **9** | Miss ($>50$) | 17 | 17 | Unchanged ($0$) |
| `item_v11_095` | `paper_res_036` | 1 chunk (`chunk_002`) | **9** | Miss ($>50$) | 17 | 18 | Demoted ($-1$) |
| `item_v11_096` | *None (Unanswerable)* | 0 chunks | — | — | — | — | Correct Rejection |
| `item_v11_097` | *None (Unanswerable)* | 0 chunks | — | — | — | — | Correct Rejection |
| `item_v11_098` | *None (Unanswerable)* | 0 chunks | — | — | — | — | Correct Rejection |
| `item_v11_099` | *None (Unanswerable)* | 0 chunks | — | — | — | — | Correct Rejection |
| `item_v11_100` | *None (Unanswerable)* | 0 chunks | — | — | — | — | Correct Rejection |

---

## 3. Scientific Implications

1. **Context Distraction in Dense Retrieval**:
   Dense vector embeddings alone are completely insufficient for scientific retrieval when queries specify precise mathematical or empirical constraints. BM25 is essential to prevent zero-recall catastrophic failures.
2. **Candidate Pool Bounding for Cross-Encoders**:
   Because BGE cross-encoder takes the top 20 candidates from B3, it cannot promote an item into the top-5 unless its cross-attention score is substantially higher than all 14 distracting chunks ahead of it. While BGE promoted gold items by up to 6 rank positions, the concentration of distractor chunks kept them outside the top-10 in this configuration.
