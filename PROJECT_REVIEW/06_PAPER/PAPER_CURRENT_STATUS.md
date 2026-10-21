# ResearchNexusAI — IEEE Paper Current Status

> **Document:** `ieee_paper/ResearchNexus_AI_Paper.tex`  
> **Target Venue:** IEEE Conference Format (Maximum 6 Pages)  
> **Author Guidance:** `evaluation/Re-evaluation of mistakes/CURRENT_LATEX_V4_UPDATE_INSTRUCTIONS.md`  

---

## 1. Status Summary
The IEEE LaTeX manuscript draft currently sits in `ieee_paper/`. To ensure scientific integrity and eliminate reviewer rejection risks, the manuscript is undergoing updates using the **V4 canonical evaluation evidence**.

## 2. Key Update Requirements for Paper Authors
1. **Retrieval Table I:** Replace any historical placeholder numbers with exact values from `canonical_retrieval_metrics.csv` (Hybrid Hit@20 = 0.867).
2. **Reranking Tone:** Tone down claims of large statistical retrieval gains from cross-encoder reranking; discuss reranker value in contextual passage precision for generation rather than raw recall superiority.
3. **Citation & Repair Section:** Accurately present the Module 3 audited findings (1/5 eligible claims grounded; repair effectiveness not demonstrated) as an honest scientific limitation and motivation for future agentic workflows.
4. **Human Evaluation:** Explicitly state that automated NLI verifier judgments were audited and that human evaluation is designated as future work.
