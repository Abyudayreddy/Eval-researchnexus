# Revised Publication Figures Package: ResearchNexus Conference Paper

**Paper Title**: *ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis*  
**Format Standard**: IEEE Conference Guidelines (Vector PDF/SVG + High-Resolution 600 DPI PNG)  
**Dataset**: `ds_nexus_v11` ($N=100$: DEV=70, VAL=15, TEST=15)  
**Package Status**: REVISED & FROZEN (100% Reconciled Results Freeze)

---

## 1. Directory Structure

```
paper_figures/
├── fig01_researchnexus_architecture.{png,svg,pdf}  # Figure 1: Clean Left-to-Right architectural pipeline
├── fig02_retrieval_performance.{png,svg,pdf}        # Figure 2: Recall@k & Hit@k (ALL N=100, TEST annotated)
├── fig03_naive_vs_verified.{png,svg,pdf}            # Figure 3: Three aligned subpanels (CSR ↑, UCR ↓, CP ↑)
├── fig04_latency_decomposition.{png,svg,pdf}        # Figure 4: Log-scale p50/p95 latency breakdown
├── fig05_iteration_tradeoff.{png,svg,pdf}           # Figure 5: Neutral refinement tradeoff (2.2x cost)
├── fig06_ablation.{png,svg,pdf}                     # Figure 6: Component ablations with log-scale ms latency
├── fig07_error_taxonomy.{png,svg,pdf}               # Figure 7: Measured taxonomy modes with unmeasured note
├── fig08_provenance_integrity.{png,svg,pdf}         # Figure 8: Automated provenance audit (N=202 claims)
├── paper_figure_data.csv                            # Raw numeric series used across all plots
├── figure_provenance_manifest.csv                   # Full provenance traceability and audit log
└── README_figures.md                                # This documentation
```

---

## 2. Reproduction Instructions (Google Colab / Standalone Python)

To reproduce these figures in Google Colab or any local terminal:
1. Ensure `matplotlib` and `pandas` are installed:
   ```bash
   pip install matplotlib pandas
   ```
2. Run the self-contained generation script:
   ```bash
   python generate_publication_figures.py
   ```
3. All figures will be exported deterministically in `paper_figures/`.
