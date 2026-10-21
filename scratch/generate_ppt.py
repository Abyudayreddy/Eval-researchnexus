import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Set 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette: Academic Navy Theme
    COLOR_BG = RGBColor(248, 249, 250)         # Soft off-white background
    COLOR_PRIMARY = RGBColor(15, 23, 42)       # Dark Slate / Navy
    COLOR_ACCENT = RGBColor(37, 99, 235)       # Cobalt Blue
    COLOR_TEXT = RGBColor(51, 65, 85)         # Slate text
    COLOR_CARD_BG = RGBColor(255, 255, 255)    # Card background
    COLOR_BORDER = RGBColor(226, 232, 240)     # Subtle card border
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_LIGHT_BLUE = RGBColor(239, 246, 255)

    def set_slide_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG

    def add_header(slide, slide_num, title_text, subtitle_text):
        # Header Container
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Title
        p_title = tf.paragraphs[0]
        p_title.text = f"SLIDE {slide_num}: {title_text}"
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_PRIMARY
        p_title.space_after = Pt(4)

        # Subtitle
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = COLOR_ACCENT

    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: BASE PAPER & RESEARCH GAP
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide1)
    add_header(slide1, 1, "BASE PAPER & RESEARCH GAP", "Reference Literature: OpenScholar (Asai et al., 2024) vs. Proposed ResearchNexus Architecture")

    # Card 1: Base Paper Summary
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(3.64), Inches(5.3))
    card1.fill.solid()
    card1.fill.fore_color.rgb = COLOR_CARD_BG
    card1.line.color.rgb = COLOR_BORDER
    tf1 = card1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = Inches(0.25)
    
    p = tf1.paragraphs[0]
    p.text = "1. Base Paper Summary"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(10)
    
    items1 = [
        "Title: OpenScholar: Synthesizing Scientific Literature with Open Datastores and Language Models (Asai et al., 2024).",
        "Core Focus: Multi-paper literature synthesis over open datastores (OSDS: ~45M open papers).",
        "Base Setup: Dense retrieval (Bi-Encoder) -> Cross-Encoder Reranker -> Fine-tuned LLM (Llama-3/Mistral).",
        "Finding: Open-access RAG outperforms proprietary black-box LLMs in factual grounding."
    ]
    for it in items1:
        p = tf1.add_paragraph()
        p.text = f"- {it}"
        p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(8)

    # Card 2: Base Paper Limitations
    card2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.84), Inches(1.6), Inches(3.64), Inches(5.3))
    card2.fill.solid()
    card2.fill.fore_color.rgb = COLOR_CARD_BG
    card2.line.color.rgb = COLOR_BORDER
    tf2 = card2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = Inches(0.25)

    p = tf2.paragraphs[0]
    p.text = "2. Base Paper Limitations"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(10)

    items2 = [
        "Dense Retrieval Misses Keywords: Fails to capture exact acronyms, model names ('ds_nexus_v10'), or formulas.",
        "Black-Box Blackhole: Zero transparency/XAI into why papers were selected or how reranking altered order.",
        "Passive Citation Hallucination: RAG treats citations as text decor; model memory causes 15-25% unsupported rate.",
        "No Citation Repair: Lacks automated NLI verification to detect and fix invalid inline citation tags."
    ]
    for it in items2:
        p = tf2.add_paragraph()
        p.text = f"- {it}"
        p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(8)

    # Card 3: Research Gap & Extension
    card3 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.88), Inches(1.6), Inches(3.64), Inches(5.3))
    card3.fill.solid()
    card3.fill.fore_color.rgb = COLOR_LIGHT_BLUE
    card3.line.color.rgb = COLOR_ACCENT
    tf3 = card3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = Inches(0.25)

    p = tf3.paragraphs[0]
    p.text = "3. Research Gap & Our Extension"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT; p.space_after = Pt(10)

    items3 = [
        "Research Gap: Absence of explainable RAG unifying hybrid search with post-hoc NLI citation repair without model fine-tuning.",
        "Hybrid Search: Fuses BM25 + ChromaDB (BGE-v1.5) via RRF (k=60).",
        "BGE Reranking: Evaluates query-snippet cross-attention via bge-reranker-base.",
        "XAI Trace Modal: Exposes exact BM25, vector distance, and RRF scores.",
        "NLI Claim Repair: Sentence-level NLI entailment auto-re-links invalid citations."
    ]
    for it in items3:
        p = tf3.add_paragraph()
        p.text = f"- {it}"
        p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(8)

    # ==========================================
    # SLIDE 2: REQUIREMENTS
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide2)
    add_header(slide2, 2, "PROJECT REQUIREMENTS", "Problem Formalization, Objectives, Stakeholders, and Core Feature Inventory")

    box_w = Inches(5.66)
    box_h = Inches(2.5)

    # Box 1: Problem & Motivation
    b1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), box_w, box_h)
    b1.fill.solid(); b1.fill.fore_color.rgb = COLOR_CARD_BG; b1.line.color.rgb = COLOR_BORDER
    t1 = b1.text_frame; t1.word_wrap = True; t1.margin_left = t1.margin_right = t1.margin_top = t1.margin_bottom = Inches(0.2)
    p = t1.paragraphs[0]; p.text = "1. Problem Statement & Motivation"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(6)
    t1_items = [
        "Problem: Manual literature review across 100s of PDFs takes days; commercial chatbots hallucinate non-existent DOIs and misquote findings.",
        "Motivation: Deliver a fast, auditable scientific assistant guaranteeing >95% Citation Precision and eliminating ungrounded claim hallucinations."
    ]
    for it in t1_items:
        p = t1.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(4)

    # Box 2: System Objectives
    b2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.86), Inches(1.6), box_w, box_h)
    b2.fill.solid(); b2.fill.fore_color.rgb = COLOR_CARD_BG; b2.line.color.rgb = COLOR_BORDER
    t2 = b2.text_frame; t2.word_wrap = True; t2.margin_left = t2.margin_right = t2.margin_top = t2.margin_bottom = Inches(0.2)
    p = t2.paragraphs[0]; p.text = "2. System Objectives"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(6)
    t2_items = [
        "Primary Objective: Build an end-to-end scientific research OS with verifiable citation attribution and sub-second retrieval performance.",
        "Specific Objectives: (1) RRF Hybrid Search (k=60), (2) BGE Cross-Encoder Reranking, (3) Enhanced RAG Context Bounding, (4) Phase 3.4 NLI Claim Verification & Repair, (5) Interactive XAI Traces."
    ]
    for it in t2_items:
        p = t2.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(4)

    # Box 3: Stakeholders
    b3 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), box_w, box_h)
    b3.fill.solid(); b3.fill.fore_color.rgb = COLOR_CARD_BG; b3.line.color.rgb = COLOR_BORDER
    t3 = b3.text_frame; t3.word_wrap = True; t3.margin_left = t3.margin_right = t3.margin_top = t3.margin_bottom = Inches(0.2)
    p = t3.paragraphs[0]; p.text = "3. Target Stakeholders"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(6)
    t3_items = [
        "Undergraduate Students: Rapid literature search and domain exploration.",
        "Postgraduate Scholars & Faculty: Conducting multi-paper synthesis and identifying open research gaps for thesis proposals.",
        "Domain Scientists & R&D Teams: Extracting specific quantitative findings with 100% evidence traceability."
    ]
    for it in t3_items:
        p = t3.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(4)

    # Box 4: Core Features
    b4 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.86), Inches(4.3), box_w, box_h)
    b4.fill.solid(); b4.fill.fore_color.rgb = COLOR_LIGHT_BLUE; b4.line.color.rgb = COLOR_ACCENT
    t4 = b4.text_frame; t4.word_wrap = True; t4.margin_left = t4.margin_right = t4.margin_top = t4.margin_bottom = Inches(0.2)
    p = t4.paragraphs[0]; p.text = "4. Core Feature Inventory"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT; p.space_after = Pt(6)
    t4_items = [
        "Research Explorer: Hybrid search across local KB and 6 external academic APIs.",
        "AI Assistant: Grounded chat with prompt context scope dropdowns.",
        "Multi-Paper Comparison Matrix: 10-dimension comparison across 2-5 papers.",
        "Personal Corpus: PDF upload, PyMuPDF extraction, and user_id vector isolation.",
        "Research Sessions: SQLite state persistence saving queries, chats, and evidence."
    ]
    for it in t4_items:
        p = t4.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(11); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(4)

    # ==========================================
    # SLIDE 3: DESIGN AND ARCHITECTURE
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide3)
    add_header(slide3, 3, "DESIGN AND ARCHITECTURE", "Technology Stack, Dual-Database Engine, and System Architecture Flow")

    # Left Column: Tech Stack Summary
    c_left = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.3))
    c_left.fill.solid(); c_left.fill.fore_color.rgb = COLOR_CARD_BG; c_left.line.color.rgb = COLOR_BORDER
    tl = c_left.text_frame; tl.word_wrap = True; tl.margin_left = tl.margin_right = tl.margin_top = tl.margin_bottom = Inches(0.25)
    p = tl.paragraphs[0]; p.text = "1. Complete Technology Stack"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(8)
    stack_items = [
        "Frontend: React 18, TypeScript 5, Vite 5 (13.04s build), Tailwind CSS, Zustand.",
        "Backend: FastAPI (Python 3.13) async ASGI, Pydantic validation, SQLAlchemy.",
        "Relational DB: SQLite / PostgreSQL for metadata, accounts, session history, logs.",
        "Vector DB: ChromaDB storing 14,850 768-dim vectors via HNSW ANN indexing.",
        "Document Parsing: PyMuPDF (fitz) extraction + LlamaIndex (512/64 sliding window).",
        "Embeddings: BAAI/bge-base-en-v1.5 (768-dimensional bi-encoder).",
        "Reranker: BAAI/bge-reranker-base (Cross-Encoder joint self-attention).",
        "LLM Engine: Gemini 2.5 Flash (temp=0.0) for context-bound RAG synthesis."
    ]
    for it in stack_items:
        p = tl.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(10.5); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(5)

    # Right Column: Architecture Flow
    c_right = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.5), Inches(1.6), Inches(7.033), Inches(5.3))
    c_right.fill.solid(); c_right.fill.fore_color.rgb = COLOR_CARD_BG; c_right.line.color.rgb = COLOR_BORDER
    tr = c_right.text_frame; tr.word_wrap = True; tr.margin_left = tr.margin_right = tr.margin_top = tr.margin_bottom = Inches(0.25)
    p = tr.paragraphs[0]; p.text = "2. Architecture Workflow & Module Pipelines"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(8)
    
    arch_steps = [
        "1. User Query -> FastAPI REST Backend (/api/search)",
        "2. Parallel Retrieval: BM25 Sparse Search + ChromaDB Vector Search (BGE-v1.5)",
        "3. Rank Fusion: Reciprocal Rank Fusion (S_RRF = sum 1 / (60 + rank))",
        "4. Reranking: BGE Cross-Encoder joint self-attention (Top 20 candidates -> Top 5)",
        "5. Enhanced RAG: Strict Context Bounding Prompting (Forbids parametric memory)",
        "6. LLM Synthesis: Gemini 2.5 Flash generates draft response with inline citations",
        "7. Claim Verification: Stage A Regex Claim Extraction -> Stage B Gemini NLI Check",
        "8. Citation Repair: Re-links invalid citation tags to entailing corpus chunks",
        "9. Output Render: Verified research answer + Interactive XAI Trace Modal"
    ]
    for st in arch_steps:
        p = tr.add_paragraph(); p.text = st; p.font.size = Pt(10.5); p.font.bold = True if "->" in st else False; p.font.color.rgb = COLOR_ACCENT if "Verification" in st or "Fusion" in st else COLOR_TEXT; p.space_after = Pt(5)

    # ==========================================
    # SLIDE 4: DATASET AND IMPLEMENTATION
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide4)
    add_header(slide4, 4, "DATASET AND IMPLEMENTATION", "Implementation Status (100% Core System Verified), Dataset Pipeline, and Demo Script")

    col_w = Inches(3.64)
    col_h = Inches(5.3)

    # Col 1: Implementation Status
    s1 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), col_w, col_h)
    s1.fill.solid(); s1.fill.fore_color.rgb = COLOR_CARD_BG; s1.line.color.rgb = COLOR_BORDER
    ts1 = s1.text_frame; ts1.word_wrap = True; ts1.margin_left = ts1.margin_right = ts1.margin_top = ts1.margin_bottom = Inches(0.25)
    p = ts1.paragraphs[0]; p.text = "1. Implementation Status"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(8)
    s1_items = [
        "Core System Status: 100% Implemented, Tested & Verified.",
        "Backend Test Suite: 112 / 112 pytest cases passing cleanly (100%).",
        "Frontend Validation: 8 / 8 UI layout assertions passing.",
        "Platform Roadmap Progress: 92% complete.",
        "Publication Scorecard: 143 / 170 Points (84.1% - SUBMISSION READY)."
    ]
    for it in s1_items:
        p = ts1.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(10.5); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(6)

    # Col 2: Dataset & Preprocessing
    s2 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.84), Inches(1.6), col_w, col_h)
    s2.fill.solid(); s2.fill.fore_color.rgb = COLOR_CARD_BG; s2.line.color.rgb = COLOR_BORDER
    ts2 = s2.text_frame; ts2.word_wrap = True; ts2.margin_left = ts2.margin_right = ts2.margin_top = ts2.margin_bottom = Inches(0.25)
    p = ts2.paragraphs[0]; p.text = "2. Dataset & Preprocessing"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(8)
    s2_items = [
        "Local Pre-Built KB: 670 full-text papers (14,850 semantic chunks).",
        "Production Domains: Artificial Intelligence (300), Environmental Science (190), Interdisciplinary (180), Material Science (Active).",
        "External Dynamic APIs (6): arXiv, PMC, AGRIS, NASA ADS, OpenAlex, Crossref.",
        "Benchmark (ds_nexus_v10): 100 gold queries (70 DEV / 15 VAL / 15 FROZEN TEST).",
        "Pipeline: PyMuPDF extraction -> Regex cleaning -> 512/64 chunking -> BGE embeddings -> ChromaDB."
    ]
    for it in s2_items:
        p = ts2.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(10.5); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(6)

    # Col 3: Demo Script Sequence
    s3 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.88), Inches(1.6), col_w, col_h)
    s3.fill.solid(); s3.fill.fore_color.rgb = COLOR_LIGHT_BLUE; s3.line.color.rgb = COLOR_ACCENT
    ts3 = s3.text_frame; ts3.word_wrap = True; ts3.margin_left = ts3.margin_right = ts3.margin_top = ts3.margin_bottom = Inches(0.25)
    p = ts3.paragraphs[0]; p.text = "3. Demo Script Sequence"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT; p.space_after = Pt(8)
    s3_items = [
        "Step 1: Open Explorer, select domain Material Science, enter research query.",
        "Step 2: Watch live execution stepper animate through RRF and BGE reranking.",
        "Step 3: Click Inspect XAI Trace to expose BM25, vector distance, and rank deltas.",
        "Step 4: Synthesize answer in AI Assistant using Phase 3.3 context bounding.",
        "Step 5: Open Claim Verifier drawer to inspect Stage A/B NLI badges (VERIFIED, REPAIRED).",
        "Step 6: Show multi-paper comparison matrix and SQLite session resumption."
    ]
    for it in s3_items:
        p = ts3.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(10.5); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(5)

    # ==========================================
    # SLIDE 5: RESULTS, CHALLENGES AND NEXT STEPS
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide5)
    add_header(slide5, 5, "RESULTS, CHALLENGES AND NEXT STEPS", "Empirical Benchmark Evaluation (E01-E05), Resolved Engineering Challenges, and Future Roadmap")

    # Table / Metrics Block (Top)
    r_top = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(2.7))
    r_top.fill.solid(); r_top.fill.fore_color.rgb = COLOR_CARD_BG; r_top.line.color.rgb = COLOR_BORDER
    tt = r_top.text_frame; tt.word_wrap = True; tt.margin_left = tt.margin_right = tt.margin_top = tt.margin_bottom = Inches(0.2)
    p = tt.paragraphs[0]; p.text = "1. Canonical Empirical Benchmark Results (ds_nexus_v10 Frozen TEST Split N=15)"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(6)

    res_items = [
        "E01 (Retrieval): Hybrid RRF (k=60) MRR 0.812 vs 0.650 Dense Only (+0.162 gain, Wilcoxon p=0.0002).",
        "E02 (Reranking): BGE Cross-Encoder TEST MRR 0.972 (+0.072 gain, p=0.0381, 0 rank regressions).",
        "E03 (Enhanced RAG): Context Bounding Citation Precision 94.7% vs 73.3% Conv RAG (p=0.0120).",
        "E04 (Claim Verifier): Citation Precision 98.0%, Unsupported Rate 1.0% (15 citations repaired, p=0.0080).",
        "E05 (Refinement): Multi-cycle refinement achieved 99.2% Citation Precision (+753.3 ms P50 overhead)."
    ]
    for it in res_items:
        p = tt.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(10.5); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(3)

    # Bottom Left: Resolved Challenges
    r_bl = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.5), Inches(5.66), Inches(2.4))
    r_bl.fill.solid(); r_bl.fill.fore_color.rgb = COLOR_CARD_BG; r_bl.line.color.rgb = COLOR_BORDER
    tbl = r_bl.text_frame; tbl.word_wrap = True; tbl.margin_left = tbl.margin_right = tbl.margin_top = tbl.margin_bottom = Inches(0.2)
    p = tbl.paragraphs[0]; p.text = "2. Resolved Engineering Challenges"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(4)
    c_items = [
        "Bi-Encoder Keyword Misses: Vector search missed exact acronyms -> Solved via RRF (k=60) sparse-dense fusion & BGE reranking.",
        "Parametric Context Leakage: LLM inserted unverified outside facts -> Solved via Phase 3.3 Enhanced RAG context bounding.",
        "Invalid Citation Tag Association: LLM attached decorative tags -> Solved via Phase 3.4 NLI Claim Verification & Citation Repair."
    ]
    for it in c_items:
        p = tbl.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(3)

    # Bottom Right: Next Steps
    r_br = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.86), Inches(4.5), Inches(5.66), Inches(2.4))
    r_br.fill.solid(); r_br.fill.fore_color.rgb = COLOR_LIGHT_BLUE; r_br.line.color.rgb = COLOR_ACCENT
    tbr = r_br.text_frame; tbr.word_wrap = True; tbr.margin_left = tbr.margin_right = tbr.margin_top = tbr.margin_bottom = Inches(0.2)
    p = tbr.paragraphs[0]; p.text = "3. Future Roadmap & Next Steps"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT; p.space_after = Pt(4)
    n_items = [
        "Immediate Fixes: Integrate OCR layer (Tesseract/Surya) for scanned PDFs; add local API caching.",
        "Short-Term Engineering: Scale local KB to 5,000+ papers; implement adaptive RRF k parameter tuning.",
        "Research Extensions: Expand frozen TEST split to N=100 items; conduct double-blind human evaluation trial."
    ]
    for it in n_items:
        p = tbr.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(3)

    # ==========================================
    # SLIDE 6: RESEARCH & PAPER PUBLICATION PROGRESS
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide6)
    add_header(slide6, 6, "RESEARCH & PAPER PUBLICATION PROGRESS", "Publication Readiness Parameters, Target Venues, Manuscript Status, and Defending Research Novelty")

    # Left Column: Publication Checklist
    p_left = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.66), Inches(5.3))
    p_left.fill.solid(); p_left.fill.fore_color.rgb = COLOR_CARD_BG; p_left.line.color.rgb = COLOR_BORDER
    tpl = p_left.text_frame; tpl.word_wrap = True; tpl.margin_left = tpl.margin_right = tpl.margin_top = tpl.margin_bottom = Inches(0.25)
    p = tpl.paragraphs[0]; p.text = "1. Honest Publication Readiness Parameters"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_PRIMARY; p.space_after = Pt(8)

    pub_items = [
        "Target Venues: ACL/EMNLP System Demos, CIKM Applied Track, IEEE Access.",
        "Final Paper Title: Title Under Finalization ('ResearchNexus: A Multi-Stage Verified Retrieval-Augmented Generation Architecture for Scientific Literature Synthesis').",
        "Literature Survey: COMPLETED (28 formal academic references analyzed).",
        "Research Gap: COMPLETED (Identified lack of verified RAG with post-hoc citation repair).",
        "Methodology & Architecture: COMPLETED (5-stage isolated pipeline locked).",
        "Results & Analysis: COMPLETED (E01-E05 benchmark tables & Wilcoxon tests compiled).",
        "Paper Writing Status: NEAR COMPLETE (IEEEtran & LNCS drafts compiled; Score 143/170).",
        "Publication Status: READY FOR INTERNAL REVIEW (Ready for advisor sign-off prior to submission)."
    ]
    for it in pub_items:
        p = tpl.add_paragraph(); p.text = f"- {it}"; p.font.size = Pt(10); p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(5)

    # Right Column: Research Novelty Defense
    p_right = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.86), Inches(1.6), Inches(5.66), Inches(5.3))
    p_right.fill.solid(); p_right.fill.fore_color.rgb = COLOR_LIGHT_BLUE; p_right.line.color.rgb = COLOR_ACCENT
    tpr = p_right.text_frame; tpr.word_wrap = True; tpr.margin_left = tpr.margin_right = tpr.margin_top = tpr.margin_bottom = Inches(0.25)
    p = tpr.paragraphs[0]; p.text = "2. Defending Research Novelty vs Software Engineering"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = COLOR_ACCENT; p.space_after = Pt(8)

    nov_items = [
        "What is NOT the contribution: Calling pre-trained APIs like Gemini 2.5 Flash or BGE embeddings is software integration, not primary research novelty.",
        "What IS the Research Contribution:",
        "  1. Phase 3.4 Stage A/B Claim Verification & Citation Repair Algorithm: Automated 2-stage NLI entailment workflow that detects hallucinated references and re-links claims to entailing corpus chunks.",
        "  2. Phase 3.3 Enhanced RAG Context Bounding: Deterministic prompt boundary design eliminating parametric memory context leakage.",
        "  3. Empirical Benchmark Protocol (ds_nexus_v10): Statistically proving (p < 0.05) across 5 isolated stages that unsupported claim rates can be reduced from 18.0% to 1.0% without model fine-tuning.",
        "Summary Defense Statement: ResearchNexus proves that combining hybrid RRF retrieval, cross-encoder reranking, and post-hoc NLI claim verification reduces scientific RAG citation hallucinations to 1.0% with 99.2% citation precision, offering an auditable framework for scientific synthesis."
    ]
    for it in nov_items:
        p = tpr.add_paragraph(); p.text = it if it.startswith("Summary") else f"- {it}"; p.font.size = Pt(10); p.font.bold = True if "IS the Research Contribution" in it or "Summary" in it else False; p.font.color.rgb = COLOR_TEXT; p.space_after = Pt(5)

    # Save presentation
    output_path = r"c:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\SDC_II_Review_Presentation.pptx"
    prs.save(output_path)
    print(f"Successfully created presentation at: {output_path}")

if __name__ == "__main__":
    create_presentation()
