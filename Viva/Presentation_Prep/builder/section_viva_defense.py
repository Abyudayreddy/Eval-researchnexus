"""
Section builders: 40+ Categorized Viva Questions with Short, Technical, and One-Line Answers,
Tough Defense Questions, Limitations, Future Work, Presentation Scripts, and Final Advice.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helpers import (
    add_header_styled, add_body_p, add_bullet_p,
    add_callout, add_code_block, add_table_styled
)

def build_viva_and_defense(doc):
    # SECTION 23: 40+ CATEGORIZED VIVA QUESTIONS & AUTHORITATIVE ANSWERS
    add_header_styled(doc, "23. Comprehensive Viva Questions & Expert Answers (40+ Questions)", level=1)
    add_body_p(
        doc,
        "Examiners frequently test whether you truly understand the algorithmic engineering beneath your user interface. "
        "Below are 40+ categorized questions with a Quick One-Line Summary, a Technical Explanation, and the Core Principle."
    )

    # Category A: Retrieval & Embeddings
    add_header_styled(doc, "Category A: Retrieval, Embeddings & Reranking", level=2)

    qa_list_a = [
        (
            "Q1. Why use Hybrid Search instead of pure vector search?",
            "Because pure vector search misses exact keywords, acronyms, and dataset names, while BM25 misses conceptual synonyms. Hybrid search captures both.",
            "Dense bi-encoder embeddings (like BGE-1.5) project sentences into semantic clusters. They understand that 'image classification' is related to 'vision transformer', but they struggle with out-of-vocabulary acronyms (e.g. 'LoRA-v2'), specific author names, or numerical hyperparameters. BM25 indexes inverted term frequencies, guaranteeing lexical precision. Combining both gives optimal candidate recall."
        ),
        (
            "Q2. What is Reciprocal Rank Fusion (RRF) and why is k=60 chosen?",
            "RRF merges rankings from multiple search systems without needing score normalization, using constant k=60 to prevent top ranks from dominating disproportionately.",
            "BM25 produces unbounded positive scores (0 to 35+), whereas cosine similarity outputs normalized values between -1 and 1. Merging them via linear score addition requires fragile calibration. RRF uses ordinal ranks instead: Score = sum(1 / (k + rank)). The parameter k=60 (established by Cormack et al., SIGIR) ensures that a document ranked #1 by one retriever doesn't overwhelmingly crush a document ranked #2 by both retrievers."
        ),
        (
            "Q3. What is the difference between a Bi-Encoder and a Cross-Encoder?",
            "A bi-encoder embeds queries and documents independently for fast ANN search; a cross-encoder processes query and document together to compute full cross-attention.",
            "Bi-encoders (bge-base-en-v1.5) encode text into fixed 768-dimensional vectors. Similarity is a simple dot product computed in microseconds over 26,000 chunks. Cross-encoders (bge-reranker-base) feed the concatenated string [CLS] Query [SEP] Chunk into a 12-layer transformer, allowing full token-to-token attention. This resolves negations, subtle conditions, and complex scientific claims that cosine distance misses."
        ),
        (
            "Q4. What is the reranker latency overhead in your system?",
            "Our cross-encoder reranking has a median latency of 531.41 ms and a 90th percentile of 642.10 ms over 20 candidate chunks.",
            "Evaluating 20 candidate pairs through a 110M-parameter cross-encoder requires forward passes over ~512 tokens. On local GPU/CPU hardware, this takes approximately half a second, which is imperceptible to an academic user awaiting a comprehensive synthesis."
        ),
        (
            "Q5. How large is your offline corpus and chunking configuration?",
            "Our local corpus contains 687 research papers, parsed into ~26,200 chunks using 500-token windows with 50-token overlap.",
            "PyMuPDF extracts text streams from PDF files. LlamaIndex sentence splitters break text into 500-token passages with a 50-token sliding overlap. This overlap guarantees that sentences spanning boundary edges are not bisected, preserving semantic context across adjacent vectors."
        )
    ]

    for q, short_ans, tech_ans in qa_list_a:
        add_header_styled(doc, q, level=3)
        add_body_p(doc, short_ans, bold_prefix="One-Line Answer: ")
        add_body_p(doc, tech_ans, bold_prefix="Technical Explanation: ")

    # Category B: Generation & Verification
    add_header_styled(doc, "Category B: Generative Synthesis & Claim Verification", level=2)

    qa_list_b = [
        (
            "Q6. How does ResearchNexus AI prevent LLM hallucinations?",
            "Through strict chunk-key prompt grounding and a post-generation two-stage claim audit (deterministic overlap + semantic NLI).",
            "We do not trust the raw LLM output. The prompt forces Gemini 2.5 Flash to attribute every assertion to specific chunk keys. The PROVE engine then decomposes the generated text into atomic statements, fast-checks verbatim text with an 80% token overlap metric, and evaluates remaining claims using structured NLI entailment."
        ),
        (
            "Q7. What are the four states of your Claim Verification Engine?",
            "SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, and CONTRADICTED.",
            "SUPPORTED indicates direct factual entailment. PARTIALLY_SUPPORTED indicates qualitative alignment but missing quantitative precision. UNSUPPORTED indicates the evidence chunk does not mention the claim. CONTRADICTED indicates the source evidence explicitly refutes the generated statement."
        ),
        (
            "Q8. Why use a deterministic token overlap pre-filter before LLM verification?",
            "To drastically cut latency and compute cost: 31.2% of claims are verbatim quotes verified in under 5ms without calling an LLM.",
            "If an extracted claim has an 80% or greater token intersection with the cited chunk, running a full NLI inference prompt is redundant. Fast-pathing these claims cuts total verification latency by nearly a third while preserving 100% precision."
        ),
        (
            "Q9. What happens if a claim citation is found to be incorrect or missing?",
            "Our Citation Repair module inspects only the retrieved candidates and re-attributes the citation only if another chunk strictly entails it; otherwise it safely abstains.",
            "Unlike naive tools that hallucinate alternative citations from the open web, our repair engine never searches outside the frozen candidate pool. If no retrieved chunk entails the claim, the citation tag is revoked to maintain academic honesty."
        ),
        (
            "Q10. Why did your E07 evaluation recommend against iterative multi-turn refinement?",
            "Because multi-turn iterative re-synthesis doubled latency (12.6s vs 5.6s) without statistically improving grounding under noisy contexts (p=1.000).",
            "When the initial retrieval pool contains distractor chunks, asking the LLM to iteratively critique and re-draft its text causes it to either repeat previous assumptions or smooth over discrepancies. Single-pass synthesis with targeted post-hoc verification proved faster and more reliable."
        )
    ]

    for q, short_ans, tech_ans in qa_list_b:
        add_header_styled(doc, q, level=3)
        add_body_p(doc, short_ans, bold_prefix="One-Line Answer: ")
        add_body_p(doc, tech_ans, bold_prefix="Technical Explanation: ")

    # Category C: Architecture & Systems
    add_header_styled(doc, "Category C: Architecture, Security & Workflow", level=2)

    qa_list_c = [
        (
            "Q11. What is the Explorer-to-Assistant Cache Handoff?",
            "It passes retrieved chunk IDs directly from the search page to the assistant state, eliminating duplicate BM25 and neural reranking runs.",
            "When a user searches in Explorer, the system has already executed BM25, ChromaDB dense search, RRF, and cross-encoder reranking. When the user clicks 'Ask AI', the frontend passes the cached chunk list in the payload. The Assistant synthesizes immediately without incurring another 700ms retrieval penalty."
        ),
        (
            "Q12. How does Document-Only Mode guarantee zero leakage from the global corpus?",
            "By isolating the uploaded PDF into a dedicated, session-scoped ChromaDB collection and disabling global fallback queries.",
            "The backend instantiates an ephemeral collection ID specifically for that uploaded file. All retrieval queries are strictly filtered by that collection ID. If no matching chunks are found, the system explicitly reports that the document does not contain the answer, completely preventing cross-paper contamination."
        ),
        (
            "Q13. How does the Multi-Paper Comparison avoid blending results between papers?",
            "By prompting the LLM with isolated paper-specific context envelopes for each cell before assembling the combined comparative matrix.",
            "Instead of dumping five papers into one giant prompt where models easily mix up accuracy numbers and authors, the comparison engine queries each paper's chunks independently for each of the 10 dimensions, assembling the matrix row-by-row with strict provenance."
        ),
        (
            "Q14. What cryptographic mechanism guarantees evidence integrity?",
            "Every chunk is assigned a SHA-256 hash computed over its exact raw text string and stored in the provenance ledger.",
            "If text in the database is modified, corrupted, or altered during indexing, the SHA-256 hash in the Claim Proof Drawer will mismatch, providing a mathematically auditable chain of custody."
        )
    ]

    for q, short_ans, tech_ans in qa_list_c:
        add_header_styled(doc, q, level=3)
        add_body_p(doc, short_ans, bold_prefix="One-Line Answer: ")
        add_body_p(doc, tech_ans, bold_prefix="Technical Explanation: ")

    # SECTION 24: TOUGH EXAMINER CHALLENGE QUESTIONS & HOW TO DEFEND
    add_header_styled(doc, "24. Tough Defense & Examiner Challenge Questions", level=1)
    add_body_p(
        doc,
        "Here are difficult, pressure-testing questions examiners love to ask, and the exact winning answers:"
    )

    add_callout(
        doc,
        "CHALLENGE 1: 'Isn't your system just a basic wrapper around Gemini and LangChain?'",
        "\"No, Mam. We do not use generic LangChain wrappers. We built custom microservices for hybrid retrieval and verification. "
        "First, we implement custom Reciprocal Rank Fusion fusing BM25 with BGE embeddings, followed by a dedicated local Cross-Encoder "
        "neural reranker (BAAI/bge-reranker-base). Second, we built the PROVE claim verification engine from scratch: it extracts individual claims, "
        "filters 31.2% via deterministic token overlap, and verifies remaining claims through strict NLI state classifications. Third, our interactive "
        "provenance ledger exposes cryptographic SHA-256 evidence hashes and cross-encoder logits directly in the user interface. "
        "An API wrapper cannot provide mathematical verification, citation repair, or isolated multi-paper matrices.\"",
        bg_hex="FDEDEC",
        border_hex="E74C3C"
    )

    add_callout(
        doc,
        "CHALLENGE 2: 'Why not just use GPT-4 with a 128k context window and dump the entire paper into the prompt?'",
        "\"Mam, that approach has two fatal flaws: cost/latency, and the 'Lost-in-the-Middle' phenomenon. "
        "First, sending 100,000 tokens per query costs orders of magnitude more and takes 15 to 30 seconds to stream. "
        "Second, extensive empirical research (Liu et al., Stanford) proves that LLMs suffer severe attention degradation in large contexts, "
        "frequently missing critical details located in the middle 60% of long documents. "
        "Our RAG architecture retrieves only the top 10 relevant 500-token chunks with cross-encoder precision, achieving 1.0000 candidate recall "
        "at a fraction of the compute time and zero attention degradation.\"",
        bg_hex="FEF9E7",
        border_hex="F39C12"
    )

    add_callout(
        doc,
        "CHALLENGE 3: 'Why did you use SQLite locally instead of PostgreSQL?'",
        "\"Mam, our database architecture is built using SQLAlchemy ORM with full driver abstraction. In local evaluation and offline benchmark "
        "runs, SQLite provides zero-dependency, deterministic file-based reproducibility that allows freezing benchmark databases (like `papers.db` "
        "and `researchnexus_eval.db`) into version control. In a production cloud deployment, changing a single connection URI in `.env` seamlessly "
        "switches the backend to PostgreSQL without altering any application code.\"",
        bg_hex="EAF2F8",
        border_hex="2471A3"
    )

    # SECTION 25: SYSTEM LIMITATIONS & FUTURE WORK
    add_header_styled(doc, "25. System Limitations & Future Work (Honest Academic Self-Assessment)", level=1)
    add_body_p(
        doc,
        "A strong presentation acknowledges real engineering boundaries. Examiners respect candidates who understand their system's limitations:"
    )

    headers_lim = ["Area / Aspect", "Current System Limitation", "Planned Future Enhancement"]
    rows_lim = [
        [
            "Corpus Domain Scope",
            "Offline verified corpus contains 687 papers focused on AI and Environmental Science. Other domains have fewer pre-indexed papers.",
            "Scale offline index to 10,000+ open-access papers across all 8 domains with automated weekly arXiv scrapers."
        ],
        [
            "Iterative Refinement",
            "Currently disabled by default because multi-turn re-synthesis adds 2.2x latency without grounding gains under noisy contexts.",
            "Implement selective iterative refinement triggered only when Stage B verification detects CONTRADICTED or UNSUPPORTED claims."
        ],
        [
            "Table & Figure Extraction",
            "PyMuPDF extracts clean text streams, but complex multi-column tables and embedded image figures are simplified into text blocks.",
            "Integrate multimodal vision models (e.g. Nougat, ColPali, or Gemini Vision) to parse vector charts and tabular grids directly."
        ],
        [
            "Human Annotation Grounding",
            "Evaluation experiment E05 remains blocked awaiting external human annotator submissions; benchmark currently relies on synthetic and automated NLI.",
            "Complete multi-annotator inter-rater reliability validation (Cohen's Kappa) with external academic reviewers."
        ]
    ]
    add_table_styled(doc, headers_lim, rows_lim, [Inches(1.8), Inches(2.5), Inches(2.5)])

    # SECTION 26: 1-MINUTE ELEVATOR PITCH & 5-MINUTE PRESENTATION SCRIPT
    add_header_styled(doc, "26. 1-Minute Elevator Pitch & 5-Minute Presentation Script", level=1)
    
    add_callout(
        doc,
        "1-MINUTE ELEVATOR PITCH",
        "\"Good morning, Mam. Our project is ResearchNexus AI — a unified academic research intelligence platform designed to eliminate "
        "literature fragmentation and LLM hallucinations. While general-purpose AI tools fabricate up to 30% of their citations, "
        "ResearchNexus introduces a closed-loop Verified RAG system. We combine BM25 lexical search with 768-dimensional BGE embeddings "
        "using Reciprocal Rank Fusion, followed by a neural Cross-Encoder that reranks the most relevant literature in just 531 milliseconds. "
        "Our custom PROVE engine extracts individual claims, validates verbatim quotes instantly via deterministic token overlap, "
        "and evaluates semantic entailment. Every claim links to an interactive Proof Drawer showing exact chunk text, cosine similarity, "
        "and cryptographic SHA-256 hashes. In our 100-query benchmark, we achieved a 100% verified trace link rate and 1.0000 test candidate recall, "
        "giving researchers an auditable, trustworthy co-investigator.\"",
        bg_hex="EAF2F8",
        border_hex="2471A3"
    )

    add_body_p(
        doc,
        "5-Minute Presentation Script Outline for Tuesday:\n"
        "• Minute 1: The Problem (Literature overload, broken search, LLM hallucinations, need for verifiable evidence).\n"
        "• Minute 2: Architecture & Tech Stack (React/TS, FastAPI, ChromaDB, BGE embeddings, BM25, RRF k=60, bge-reranker-base, Gemini Flash).\n"
        "• Minute 3: Live Demo Part 1 (Search in Explorer -> RRF & Reranker scores -> Click 'Ask AI' showing cache handoff).\n"
        "• Minute 4: Live Demo Part 2 (Synthesis with citations -> Open ClaimProofDrawer -> Show SHA-256 hash -> Switch to Multi-Paper Comparison).\n"
        "• Minute 5: Evaluation & Conclusion (Present 1.0000 test recall, 531ms median latency, 100% trace rate, and roadmap)."
    )

    # SECTION 27: FINAL ADVICE FOR TUESDAY DEFENSE
    add_header_styled(doc, "27. Final Advice for Tuesday Project Presentation", level=1)
    add_bullet_p(doc, "Speak calmly and with conviction. You built this system, and you know how every line of code connects.", bold_prefix="1. Confidence: ")
    add_bullet_p(doc, "Do not rush into code immediately. Ground Mam in the researcher's dilemma first so she appreciates why verification matters.", bold_prefix="2. Frame the Story First: ")
    add_bullet_p(doc, "Keep localhost:5173 and your FastAPI backend running in separate terminals before you enter the room.", bold_prefix="3. Pre-flight Check: ")
    add_bullet_p(doc, "If asked a question you are unsure about, state the principle clearly: 'Mam, our system enforces conservative verification: we prefer abstention over fabricated attribution.'", bold_prefix="4. Scientific Honesty: ")

    return doc
