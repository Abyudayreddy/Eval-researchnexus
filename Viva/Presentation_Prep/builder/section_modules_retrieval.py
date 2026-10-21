"""
Section builders: Product Modules Breakdown (Features & honest status tags),
Retrieval Engine Deep Dive (BM25, Dense, RRF k=60), Cross-Encoder Reranker,
RAG from Zero to Synthesis, and Research Gap & Motivation.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helpers import (
    add_header_styled, add_body_p, add_bullet_p,
    add_callout, add_code_block, add_table_styled
)

def build_modules_and_retrieval(doc):
    # SECTION 5: PRODUCT MODULES / MAJOR FEATURES
    add_header_styled(doc, "5. Product Modules & Major Features (With Honest Implementation Status)", level=1)
    add_body_p(
        doc,
        "During your presentation, transparency about what is running live in the codebase versus what is partially implemented "
        "or planned demonstrates high scientific integrity. Below is the authoritative breakdown of every module:"
    )

    headers_mod = ["Module / Feature", "Implementation Status", "Functionality & Working Reality", "Where in Codebase"]
    rows_mod = [
        [
            "Dashboard Page",
            "IMPLEMENTED",
            "Shows quick statistics, quick navigation buttons, recent search queries, and active workspace switcher.",
            "src/pages/DashboardPage.tsx"
        ],
        [
            "Research Explorer (Hybrid Search)",
            "IMPLEMENTED",
            "Performs BM25 + Dense ChromaDB retrieval, RRF k=60 fusion, Cross-Encoder reranking, domain filtering, and year range filters.",
            "src/pages/HybridSearchPage.tsx, backend/app/services/retrieval.py"
        ],
        [
            "Domain Filtering (8 Domains)",
            "PARTIALLY IMPLEMENTED",
            "UI supports 8 domains. Offline corpus (687 papers) is verified primarily in Artificial Intelligence, Environmental Science, and Interdisciplinary.",
            "src/pages/HybridSearchPage.tsx, backend/app/services/retrieval.py"
        ],
        [
            "Research Assistant (Ask AI)",
            "IMPLEMENTED",
            "Multi-turn scientific dialogue, caching context passed from Explorer, verified claim auditing, and structured scientific synthesis.",
            "src/pages/AssistantPage.tsx, backend/app/services/assistant/enhanced_rag.py"
        ],
        [
            "Multi-Paper Comparison",
            "IMPLEMENTED",
            "Compares 2 to 5 papers side-by-side across 10 structured scientific dimensions with strictly isolated prompt cells to prevent blending.",
            "src/pages/ComparisonPage.tsx, backend/app/services/assistant/comparison_engine.py"
        ],
        [
            "PROVE Verification Engine",
            "IMPLEMENTED",
            "Decomposes synthesis into atomic claims, runs deterministic token overlap check, then executes semantic NLI verification.",
            "backend/app/services/assistant/claim_verifier.py"
        ],
        [
            "XAI Provenance Ledger & Drawer",
            "IMPLEMENTED",
            "Interactive slide-out drawer showing exact supporting sentence snippets, chunk IDs, cosine scores, and cross-encoder logits.",
            "src/components/assistant/ClaimProofDrawer.tsx"
        ],
        [
            "Document-Only PDF Analysis",
            "IMPLEMENTED",
            "User uploads local PDF; PyMuPDF parses text into a temporary isolated ChromaDB collection. Strict zero-leakage guarantee.",
            "backend/app/services/document_service.py"
        ],
        [
            "Dynamic Paper Ingestion Pipeline",
            "IMPLEMENTED",
            "Asynchronous status machine: UPLOADED -> PARSING -> CHUNKING -> EMBEDDING -> INDEXED -> READY with progress tracking.",
            "backend/app/services/document_service.py"
        ],
        [
            "Literature Review Generator",
            "PARTIALLY IMPLEMENTED",
            "Produces structured thematic reviews from selected library papers; citation synthesis active, background auto-clustering in progress.",
            "src/pages/LiteratureReviewPage.tsx"
        ],
        [
            "Personal Library & Collections",
            "IMPLEMENTED",
            "Allows saving papers from search results, organizing into custom folders/tags, and batch-selecting papers for comparison.",
            "src/pages/LibraryPage.tsx"
        ],
        [
            "Research Notebook & Workspace",
            "IMPLEMENTED",
            "Markdown note-taking integrated directly beside paper viewing panes, with citation dragging.",
            "src/pages/NotebookPage.tsx"
        ],
        [
            "System Analytics Dashboard",
            "IMPLEMENTED",
            "Displays retrieval latency benchmarks, reranking distributions, cache hit rates, and claim verification statistics.",
            "src/pages/AnalyticsPage.tsx"
        ]
    ]
    add_table_styled(doc, headers_mod, rows_mod, [Inches(1.5), Inches(1.2), Inches(2.6), Inches(1.5)])

    # SECTION 6: RETRIEVAL EXPLAINED AS A STORY
    add_header_styled(doc, "6. Retrieval Explained as a Story: The Battle Between Keywords & Concepts", level=1)
    add_body_p(
        doc,
        "Imagine you are in a massive university library containing 26,000 research articles. You ask a junior librarian: "
        "'Find papers discussing how neural networks lose previously learned skills when trained on new tasks.'"
    )
    add_body_p(
        doc,
        "If the librarian only knows strict keyword matching (like classical BM25), they look through the index for the words "
        "'neural networks lose skills'. If a seminal paper titled 'Catastrophic Forgetting in Continual Learning' never uses the exact "
        "phrase 'lose skills', the librarian walks right past it. That is the fundamental weakness of lexical search: vocabulary mismatch."
    )
    add_body_p(
        doc,
        "Now imagine a second librarian who works entirely through conceptual vibes (dense vector embeddings). They understand that "
        "'losing skills' relates to 'catastrophic forgetting'. But if you give them a precise query like 'BERT-large F1 score on SQuAD v2', "
        "they might hand you a paper about RoBERTa on GLUE because conceptually both are transformer language models! The vector similarity "
        "glosses over the exact model name and numerical benchmark."
    )
    add_body_p(
        doc,
        "How ResearchNexus AI Solves This: The Hybrid RRF Pipeline\n"
        "We combine both librarians using Reciprocal Rank Fusion (RRF with k=60). The BM25 engine guarantees that exact acronyms, "
        "dataset names, and mathematical terms are prioritized. Simultaneously, the BAAI/bge-base-en-v1.5 embedding engine projects "
        "both query and chunks into a 768-dimensional latent space to capture semantic intent. RRF calculates a combined score:"
    )

    add_code_block(
        doc,
        "RRF_Score(d) = sum( 1 / (k + rank_i(d)) ) for each retriever i\n"
        "where k = 60 (standard Cormack et al. smoothing constant).\n\n"
        "If a chunk ranks 1st in BM25:  1 / (60 + 1) = 0.01639\n"
        "If that chunk ranks 3rd in Dense: 1 / (60 + 3) = 0.01587\n"
        "Combined RRF Score = 0.01639 + 0.01587 = 0.03226 -> Dominates candidate ranking!",
        caption="Reciprocal Rank Fusion Formulation"
    )

    add_body_p(
        doc,
        "In our frozen experimental evaluation across 100 benchmark queries (ds_nexus_v11), this hybrid strategy achieved:\n"
        "• Dense-only Recall@20: 0.9000 (TEST split: 0.9000)\n"
        "• BM25-only Recall@20: 0.8800 (TEST split: 0.9333)\n"
        "• Hybrid RRF k=20 Candidate Recall: 0.9500 (TEST split: 1.0000 - perfect recall!)"
    )

    # SECTION 7: NEURAL CROSS-ENCODER RERANKING
    add_header_styled(doc, "7. Neural Cross-Encoder Reranking: Why Dense Cosine Similarity Isn't Enough", level=1)
    add_body_p(
        doc,
        "A common viva question is: 'If your bi-encoder embeddings already scored the similarity, why do you need a second reranking model?'"
    )
    add_body_p(
        doc,
        "The answer lies in how bi-encoders work versus cross-encoders:\n"
        "• Bi-Encoder (bge-base-en-v1.5): The query and the document chunk are encoded into vectors independently. "
        "The interaction is computed as a simple dot product: cos_sim(u, v) = u . v. This allows lightning-fast approximate nearest neighbor "
        "search over 26,000 vectors, but the model cannot see the query tokens and document tokens simultaneously. Cross-attention is impossible.\n"
        "• Cross-Encoder (bge-reranker-base): We take the top 20 candidates from RRF and feed the combined string: [CLS] Query [SEP] Chunk [SEP] "
        "directly into a 12-layer transformer. Every single word in the query attends to every single word in the research chunk. "
        "This captures subtle logical nuances, negations, conditionality ('effective under low temperature, but fails under high latency'), "
        "and eliminates superficial keyword coincidences."
    )

    add_callout(
        doc,
        "REAL SYSTEM PERFORMANCE METRIC",
        "Our empirical evaluation measures the cross-encoder reranking latency:\n"
        "• Median Latency: 531.41 ms (p50)\n"
        "• 90th Percentile Latency: 642.10 ms (p90)\n"
        "This half-second overhead is well within the acceptable budget for academic research synthesis, while boosting answer "
        "grounding precision dramatically.",
        bg_hex="EAF2F8",
        border_hex="2471A3"
    )

    # SECTION 8: RAG FROM ZERO TO SCIENTIFIC SYNTHESIS
    add_header_styled(doc, "8. RAG from Zero to Scientific Synthesis: Avoiding the Common Traps", level=1)
    add_body_p(
        doc,
        "Retrieval-Augmented Generation (RAG) is commonly implemented by taking top chunks, concatenating them into a prompt, "
        "and asking an LLM: 'Answer the question based on the text above.' In scientific research, this naive approach fails catastrophically:"
    )
    add_bullet_p(doc, "The LLM blurs contradictory findings from Paper A and Paper B into a single compromise claim.", bold_prefix="Contradiction Blurring: ")
    add_bullet_p(doc, "The model attaches footnote [1] to a sentence, but paper [1] only discusses the background, not the metric.", bold_prefix="Phantom Footnotes: ")
    add_bullet_p(doc, "When retrieved chunks contain partial answers, the LLM hallucinates the missing methodological steps to make the paragraph read smoothly.", bold_prefix="Extrapolative Smoothing: ")
    add_body_p(
        doc,
        "How ResearchNexus AI Does RAG Differently:\n"
        "1. Strict Chunk Key Attribution: The LLM prompt enforces that every assertive statement must reference the exact assigned chunk token [chunk_id].\n"
        "2. Temperature Calibration: We run Gemini 2.5 Flash at temperature=0.2 with nucleus sampling to suppress imaginative variance.\n"
        "3. Post-Generation Claim Extraction: The synthesis is not presented immediately. It is split into individual declarative claims and "
        "routed through our two-stage verification engine.\n"
        "4. Cache Preservation: When a user performs a search in Research Explorer and clicks 'Ask AI', the exact reranked chunk context is passed "
        "in the client/session state, completely bypassing redundant re-retrieval."
    )

    # SECTION 9: RESEARCH GAP & MOTIVATION
    add_header_styled(doc, "9. Research Gap & Motivation: What Existing Literature Platforms Lack", level=1)
    add_body_p(
        doc,
        "To clearly establish our academic contribution, we mapped existing state-of-the-art tools against ResearchNexus AI:"
    )

    headers_comp = ["Capability / Feature", "Google Scholar / Semantic Scholar", "Consensus / Elicit", "ResearchNexus AI"]
    rows_comp = [
        ["Search Modality", "Keyword + Citation Graph", "Dense Semantic Search", "Hybrid BM25 + BGE Dense + Cross-Encoder"],
        ["Verification Engine", "None (Manual reading)", "Simple snippet extraction", "Two-Stage Audit (Token Overlap + NLI)"],
        ["Audit Transparency", "Link to paper only", "Snippet quotation", "Interactive Proof Drawer with Rerank Scores & SHA-256"],
        ["Multi-Paper Comparison", "None", "Summary table (generic)", "10-Dimension Matrix with Isolated Paper-Cells"],
        ["Document-Only Mode", "None", "PDF upload (often blended)", "Dedicated Collection with Zero-Leakage Guarantee"],
        ["Workflow Continuity", "Isolated tabs", "Separate search vs chat", "Unified Explorer -> Assistant -> Compare -> Library Pipeline"]
    ]
    add_table_styled(doc, headers_comp, rows_comp, [Inches(1.8), Inches(1.6), Inches(1.6), Inches(1.8)])

    return doc
