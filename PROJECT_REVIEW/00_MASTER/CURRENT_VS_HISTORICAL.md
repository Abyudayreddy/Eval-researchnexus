# ResearchNexusAI — Current vs. Historical Separation Guide

> **Principle:** Clear separation of current authoritative evidence from superseded experiments.  

---

## 1. What is CURRENT & AUTHORITATIVE

| Area | Current Authoritative Source | Key Characteristics |
|---|---|---|
| **Code Architecture** | `src/` and `backend/app/` | Active production application |
| **Code Inventory** | `PROJECT_REVIEW_CODE_INVENTORY.md` | Authoritative 665-file scan, 23 A+ core files |
| **Evaluation Evidence** | `evaluation/Re-evaluation of mistakes/` | V4 canonical reconciliation: Hit@20 = 0.867, Grounding Precision = 88.4% |
| **Citation Repair Status** | Module 3 Final Interpretation Lock | 20.0% coverage (1/5 claims); Not Demonstrated |
| **Paper Manuscript** | `ieee_paper/ResearchNexus_AI_Paper.tex` | 6-page IEEE conference format draft |
| **Review Guidance** | `PROJECT_REVIEW/` | Single entry point for viva and technical review |

---

## 2. What is HISTORICAL & SUPERSEDED

| Area | Historical Location | Why it is Superseded |
|---|---|---|
| **Old Reranking Claims** | Historical E02 reports | Claims of statistical reranking superiority over hybrid were withdrawn |
| **Old Citation Claims** | Historical Module 3 drafts | Claims of automated repair effectiveness were reconciled to 20% (1/5 claims) |
| **Early Audit JSONs** | `publication_audit/` (01 to 13) | Early exploratory audits superseded by V4 canonical reconciliation |
| **Patch Scripts** | Root `fix_*.py`, `edit_*.py`, `patch_*.py` | One-time development fixes whose changes are already integrated |
| **Scratchpad Work** | `scratch/*` | Temporary inspection utilities not part of core runtime |
