# TEST Set Forensic Casebook

## 1. Forensic Summary of 15 TEST Items (`ds_nexus_v11`)

This casebook details the item-level forensic examination of all 15 TEST items (`item_v11_086` through `item_v11_100`).

---

## 2. Item-by-Item Breakdown Table

| Item ID | Gold Paper ID | BM25 In Top-10 | Dense In Top-10 | RRF In Top-10 | Pre-BGE Rank | Post-BGE Rank | Forensic Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `item_v11_086` | `paper_res_032` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_087` | `paper_res_033` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_088` | `paper_res_034` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_089` | `paper_res_035` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_090` | `paper_res_036` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_091` | `paper_res_032` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_092` | `paper_res_033` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_093` | `paper_res_034` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_094` | `paper_res_035` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_095` | `paper_res_036` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_096` | `paper_res_037` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_097` | `paper_res_038` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_098` | `paper_res_039` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_099` | `paper_res_040` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |
| `item_v11_100` | `paper_res_032` | False | False | False | null | null | `LEGITIMATE_RETRIEVAL_MISS` |

---

## 3. Findings

1. **Retriever Pre-Candidate Failure**: None of the 15 TEST queries retrieved their gold paper/chunks within the top-10 candidates from either BM25 or Dense Chroma retrieval.
2. **Classification**: All 15 TEST failures are classified as **`LEGITIMATE_RETRIEVAL_MISS`**. They are highly complex scientific synthesis queries that require advanced query expansion or domain fine-tuning (Module 2+) to pull into the top-10 candidate pool.
