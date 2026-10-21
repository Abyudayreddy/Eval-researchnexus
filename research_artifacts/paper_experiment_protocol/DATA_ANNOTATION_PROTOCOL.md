# Data Annotation Protocol (Frozen)

## 1. Overview

This document specifies the human annotation rules for generation and claim verification evaluation on `ds_nexus_v11`.

---

## 2. Dedicated Human Evaluation Subset

- **Sample Size**: $N=30$ queries (15 VALIDATION, 15 TEST).
- **Selection Method**: Stratified sampling across all 8 scientific categories.
- **Annotator Pool**: 2 independent expert annotators + 1 senior adjudicator.
- **Annotation Tasks**:
  1. Extract claims from generated synthesis text.
  2. Assign ground truth NLI label (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONTRADICTED`) against cited chunk.
  3. Verify exact citation character offset matching.
