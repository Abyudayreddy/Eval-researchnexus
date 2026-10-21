"""
Section builders: Multi-Paper Comparison, Literature Review Workflow,
Research Review Toolkit (Scenario Banks), and Live Demo Guide & Speaking Scripts.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helpers import (
    add_header_styled, add_body_p, add_bullet_p,
    add_callout, add_code_block, add_table_styled
)

def build_comparison_demo_scripts(doc):
    # SECTION 15: MULTI-PAPER MATRIX COMPARISON
    add_header_styled(doc, "15. Multi-Paper Matrix Comparison: Structured Synthesis Without Contamination", level=1)
    add_body_p(
        doc,
        "When literature reviews evaluate multiple papers, students and researchers frequently get confused about which paper used which "
        "dataset, which baseline achieved what score, and what specific limitations each author acknowledged. "
        "ResearchNexus AI introduces an automated Multi-Paper Comparison Engine (`backend/app/services/assistant/comparison_engine.py`)."
    )
    add_body_p(
        doc,
        "The 10 Structured Scientific Dimensions:\n"
        "1. Research Objective & Problem Formulation\n"
        "2. Core Proposed Methodology / Architecture\n"
        "3. Key Datasets & Benchmarks Evaluated\n"
        "4. Primary Quantitative Results & Performance Metrics\n"
        "5. Baseline Models Compared Against\n"
        "6. Computational Complexity & Resource Requirements (GPU/VRAM/Compute)\n"
        "7. Major Theoretical & Empirical Strengths\n"
        "8. Stated Weaknesses & Critical Failure Modes\n"
        "9. Real-World Practical Applicability & Deployment Readiness\n"
        "10. Authors' Stated Future Research Directions"
    )

    add_callout(
        doc,
        "CRITICAL ARCHITECTURAL SAFEGUARD: ZERO CROSS-PAPER CONTAMINATION",
        "How do we prevent the LLM from attributing Paper A's results to Paper B? "
        "In `comparison_engine.py`, each matrix cell is populated by querying the LLM with an isolated context envelope: "
        "ONLY the chunks corresponding to Paper X are provided when extracting Paper X's methodology and metrics. "
        "The comparative synthesis is generated only after all individual cells are independently verified against their respective source documents.",
        bg_hex="EAF2F8",
        border_hex="2471A3"
    )

    # SECTION 16: LITERATURE REVIEW WORKFLOW
    add_header_styled(doc, "16. Literature Review Workflow: From Search to Synthesis", level=1)
    add_body_p(
        doc,
        "The Literature Review page (`src/pages/LiteratureReviewPage.tsx`) unifies the entire research discovery pipeline into a four-step flow:\n"
        "1. Paper Selection: Pick 3 to 10 papers directly from your Personal Library or from Explorer search results.\n"
        "2. Focus Area & Topic Scoping: Choose specific thematic angles (e.g. 'Methodological Evolution', 'Empirical Baselines', 'Open Challenges').\n"
        "3. Synthesis Generation: The system drafts a cohesive, thematic multi-section literature review citing every paper with inline chunk references.\n"
        "4. Export & Note Sync: Export the verified review directly into BibTeX, Markdown, or your Research Notebook."
    )

    # SECTION 17: RESEARCH REVIEW TOOLKIT & SCENARIO BANKS
    add_header_styled(doc, "17. Research Review Toolkit: 3 Production Scenario Banks", level=1)
    add_body_p(
        doc,
        "To ensure the system works reliably across different researcher personas, we built and tested three distinct scenario banks "
        "(documented in `src/data/research_review_toolkit.md`):"
    )
    add_bullet_p(doc, "Focuses on rapid literature triage. A student searches for a broad topic (e.g. 'federated learning non-IID data'), skims top reranked chunks, saves 3 papers to their library, and reads a 3-bullet verified summary.", bold_prefix="1. Daily Research Scenarios (Rapid Triage): ")
    add_bullet_p(doc, "Focuses on rigorous comparative analysis. An author compares two competing architectures (e.g. LoRA vs Prefix Tuning) across parameter counts, training latency, and benchmark scores using the 10-dimension comparison matrix.", bold_prefix="2. Deep Investigation Scenarios (Comparative Rigor): ")
    add_bullet_p(doc, "Stress-tests the system under adversarial conditions: conflicting findings between papers, unanswerable queries outside the corpus, and confidential single-PDF uploads. In all cases, the system cleanly abstains or highlights contradictions rather than hallucinating.", bold_prefix="3. Edge & Boundary Scenarios (Robustness & Integrity): ")

    # SECTION 18: COMPLETE LIVE DEMO PREPARATION (WHAT TO SHOW MAM)
    add_header_styled(doc, "18. Complete Live Demo Preparation: Step-by-Step Script for Tuesday", level=1)
    add_body_p(
        doc,
        "During your presentation, follow this 8-step live demo sequence. It showcases every major capability in logical order without hiccups:"
    )

    headers_demo = ["Step / Screen", "Action on Screen", "What You Point Out to Mam"]
    rows_demo = [
        [
            "DEMO 1: Dashboard",
            "Open browser at localhost:5173. Show Dashboard overview.",
            "Explain the active workspace, 687 ingested research papers, 26,000+ indexed chunks, and recent query history."
        ],
        [
            "DEMO 2: Explorer Search",
            "Type query: 'causes of concept drift in continual learning'. Click Search.",
            "Highlight the two-stage search: BM25 lexical match + BGE dense semantic match fused via RRF k=60, then reranked by Cross-Encoder in ~500ms."
        ],
        [
            "DEMO 3: Cache Handoff",
            "Click the 'Ask AI' button directly from the search results toolbar.",
            "Explain that the browser transfers the exact cached chunk IDs to the Assistant. No redundant retrieval or wasted server compute!"
        ],
        [
            "DEMO 4: Verified Synthesis",
            "Watch Gemini 2.5 Flash stream the synthesis with inline citations [1], [2].",
            "Show how each statement makes a concrete scientific claim backed by chunk keys."
        ],
        [
            "DEMO 5: Proof Drawer (XAI)",
            "Click the green 'Verified' badge next to a claim to open ClaimProofDrawer.",
            "Show the exact supporting sentence snippet, the paper title, DOI, cosine similarity score, and cryptographic SHA-256 evidence hash."
        ],
        [
            "DEMO 6: Multi-Paper Compare",
            "Navigate to Compare Page. Select 2 papers on Continual Learning.",
            "Show the 10-dimension matrix generated side-by-side with zero cross-paper hallucination or cell bleeding."
        ],
        [
            "DEMO 7: Document-Only Mode",
            "Upload a sample research PDF. Ask a question specific to that paper.",
            "Explain that the system isolates the PDF into a temporary collection with strict zero-leakage guarantee."
        ],
        [
            "DEMO 8: Analytics Page",
            "Switch to Analytics tab. Show latency breakdown & benchmark charts.",
            "Present real empirical metrics: 531ms median reranker latency and 100% verified provenance links."
        ]
    ]
    add_table_styled(doc, headers_demo, rows_demo, [Inches(1.8), Inches(2.5), Inches(2.5)])

    # SECTION 19: NATURAL SPEAKING SCRIPTS (WHAT TO SAY WHILE DEMONSTRATING)
    add_header_styled(doc, "19. Natural Speaking Scripts: What to Say in the Live Demo", level=1)
    add_body_p(
        doc,
        "Use these exact speaking points while operating the interface so your explanation flows naturally and professionally:"
    )

    add_callout(
        doc,
        "SCRIPT 1: DURING RESEARCH EXPLORER SEARCH",
        "\"Mam, let's start with Research Explorer. In traditional academic search, if a researcher enters 'causes of concept drift in continual learning', "
        "keyword search only finds papers with those exact words, missing synonyms like 'distribution shift' or 'catastrophic interference'. "
        "Our system immediately executes hybrid retrieval: rank-bm25 captures exact technical terminology, while BAAI/bge-base-en-v1.5 projects the query "
        "into a 768-dimensional semantic space. Reciprocal Rank Fusion combines the top candidates with k=60 smoothing. Then, our BAAI/bge-reranker-base "
        "cross-encoder evaluates full token-to-token attention in just 531 milliseconds, ranking the most relevant experimental chunks at the very top.\"",
        bg_hex="FEF9E7",
        border_hex="F39C12"
    )

    add_callout(
        doc,
        "SCRIPT 2: DURING 'ASK AI' AND PROOF DRAWER INSPECTION",
        "\"Now, watch what happens when I click 'Ask AI'. Notice that the assistant begins synthesizing immediately without re-querying the database. "
        "That is our Explorer-to-Assistant cache handoff. Gemini 2.5 Flash generates a structured synthesis. But here is the critical difference: "
        "our PROVE engine intercepts the output. It decomposes the synthesis into individual claims, runs a deterministic token-overlap check, "
        "and then validates semantic entailment. When I click this green 'Verified' badge, our Claim Proof Drawer slides out. You can inspect the "
        "exact sentence from the source paper, the paper title, author, and even the SHA-256 cryptographic hash of the evidence chunk. "
        "There are no phantom footnotes or ungrounded assertions in ResearchNexus AI.\"",
        bg_hex="EAF2F8",
        border_hex="2471A3"
    )

    return doc
