import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PPTX_PATH = r"C:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\PPT.pptx"

prs = Presentation(PPTX_PATH)

NAVY = RGBColor(15, 23, 42)        # Slate 900
DARK_BLUE = RGBColor(30, 58, 138)   # Blue 900
PRIMARY = RGBColor(37, 99, 235)     # Royal Blue 600
TEXT_DARK = RGBColor(30, 41, 59)    # Slate 800
TEXT_MUTED = RGBColor(100, 116, 139)# Slate 500
WHITE = RGBColor(255, 255, 255)
CARD_BG = RGBColor(248, 250, 252)   # Slate 50
CARD_BORDER = RGBColor(226, 232, 240)
EMERALD = RGBColor(16, 185, 129)
AMBER = RGBColor(245, 158, 11)
PURPLE = RGBColor(147, 51, 234)

def clear_content_shapes(slide, title_id):
    to_remove = []
    for shape in slide.shapes:
        if shape.shape_id not in [2, title_id]:
            to_remove.append(shape)
    for shape in to_remove:
        sp = shape._element
        sp.getparent().remove(sp)

def add_header_subtitle(slide, title_text, story_subtitle, title_top=0.4, title_h=0.6):
    tb = slide.shapes.add_textbox(Inches(1.5), Inches(title_top + 0.55), Inches(17.0), Inches(0.45))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = story_subtitle
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.font.name = "Segoe UI"

def create_card(slide, left, top, width, height, title, subtitle="", border_color=CARD_BORDER, bg_color=WHITE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.22)
    tf.margin_bottom = Inches(0.2)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.font.name = "Segoe UI"
    
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = PRIMARY
        p2.font.name = "Segoe UI"
        p2.space_after = Pt(6)
    
    return shape

def add_bullet(tf, bold_label, text, pt_size=13, text_color=TEXT_DARK, bullet_char="• "):
    p = tf.add_paragraph()
    p.space_after = Pt(6)
    p.line_spacing = 1.15
    run1 = p.add_run()
    run1.text = f"{bullet_char}{bold_label}: " if bold_label else bullet_char
    run1.font.bold = True
    run1.font.size = Pt(pt_size)
    run1.font.color.rgb = DARK_BLUE
    run1.font.name = "Segoe UI"
    
    run2 = p.add_run()
    run2.text = text
    run2.font.bold = False
    run2.font.size = Pt(pt_size)
    run2.font.color.rgb = text_color
    run2.font.name = "Segoe UI"

# ==================== SLIDE 2: BASE PAPER & RESEARCH GAP ====================
print("Styling Slide 2...")
s2 = prs.slides[1]
clear_content_shapes(s2, 3)
add_header_subtitle(s2, "BASE PAPER & RESEARCH GAP", "Story: \"The Smart Reader Who Forgets Where They Read It\"")

card1 = create_card(s2, 1.5, 1.5, 5.3, 8.8, "1. The Base Paper", "OpenScholar (UW / AI2, 2024)")
tf1 = card1.text_frame
add_bullet(tf1, "The Big Idea", "An AI made to read scientific papers and answer hard research questions.")
add_bullet(tf1, "Existing Way", "Vanilla AI answers from memory—often guessing fake authors and dates.")
add_bullet(tf1, "How Base Paper Works", "Searches open papers first, then writes an answer with bracketed citations.")
add_bullet(tf1, "Key Findings", "Reached ~75% citation accuracy, proving open-source AI can assist researchers.")

card2 = create_card(s2, 7.3, 1.5, 5.3, 8.8, "2. Where It Fails", "The 3 Critical Gaps", border_color=AMBER)
tf2 = card2.text_frame
add_bullet(tf2, "Blind to Formulas", "Dense AI vectors miss exact chemical names like Li10GeP2S12 or MAPbI3.")
add_bullet(tf2, "No Fact-Checker", "Generates answers in one shot without verifying if citations are actually true.")
add_bullet(tf2, "Black-Box Answers", "Gives numbers without showing which sentence or table proved it.")
add_bullet(tf2, "The Real Harm", "In a science lab, a guessed temperature or formula ruins expensive tests!")

card3 = create_card(s2, 13.1, 1.5, 5.4, 8.8, "3. Our Breakthrough", "What ResearchMind Solves", border_color=EMERALD)
tf3 = card3.text_frame
add_bullet(tf3, "Exact Keyword + Meaning", "Fuses BM25 (word matches) + BGE (concepts) so zero formulas are lost.")
add_bullet(tf3, "Auto Fact-Checker (Phase 3.4)", "Breaks text into small claims and tests if the paper proves it. If not, it fixes it!")
add_bullet(tf3, "Visual Heatmap (XAI)", "Colors the source paper in gold so humans see the exact proof in 1 click.")
add_bullet(tf3, "The Result", "Citation precision jumps from 82% to 98%, hallucinations drop to 1%!")


# ==================== SLIDE 3: REQUIREMENTS ====================
print("Styling Slide 3...")
s3 = prs.slides[2]
clear_content_shapes(s3, 3)
add_header_subtitle(s3, "Project Objectives & System Requirements", "Story: \"Building an Honest, Transparent Assistant for Scientists\"")

c3_1 = create_card(s3, 1.5, 1.5, 5.3, 8.8, "1. The Vision & Goal", "What We Built & Why")
tf3_1 = c3_1.text_frame
add_bullet(tf3_1, "The Project", "An Explainable Scientific Research OS for Material Science literature.")
add_bullet(tf3_1, "Core Objective", "Make literature search 10x faster with 0% unverified statements.")
add_bullet(tf3_1, "High Accuracy Target", "Retrieve the right paper >95% of the time (MRR @ 0.972).")
add_bullet(tf3_1, "Zero Guessing", "Every single number must point to its exact source chunk.")

c3_2 = create_card(s3, 7.3, 1.5, 5.3, 8.8, "2. Who Uses It?", "3 Key Stakeholders")
tf3_2 = c3_2.text_frame
add_bullet(tf3_2, "Professors & Postdocs", "Instantly compare synthesis recipes across 50 papers without opening each PDF.")
add_bullet(tf3_2, "B.Tech & Ph.D. Students", "Write accurate literature reviews with auto-generated LaTeX tables & BibTeX.")
add_bullet(tf3_2, "R&D Battery / Solar Labs", "Verify experimental numbers before running costly physical experiments.")
add_bullet(tf3_2, "Journal Reviewers", "Audit whether submitted paper claims are actually backed by citations.")

c3_3 = create_card(s3, 13.1, 1.5, 5.4, 8.8, "3. System Requirements", "Key Specs & Use Cases", border_color=PRIMARY)
tf3_3 = c3_3.text_frame
add_bullet(tf3_3, "Speed", "Search over 14,800 chunks in under 650 ms; full verified synthesis in 3.2 sec.")
add_bullet(tf3_3, "Precision", ">95% verified citations; <2% unsupported claims.")
add_bullet(tf3_3, "Multi-Paper Matrix", "Extract ionic conductivity, stability, and limits into side-by-side tables.")
add_bullet(tf3_3, "LaTeX Export", "One-click export to IEEEtran & Springer LNCS manuscripts.")


# ==================== SLIDE 4: DESIGN & ARCHITECTURE ====================
print("Styling Slide 4...")
s4 = prs.slides[3]
clear_content_shapes(s4, 4)
add_header_subtitle(s4, "DESIGN & ARCHITECTURE", "Story: \"The 4-Step Factory: Read -> Find -> Check -> Show\"", title_top=0.33)

step_w = 4.0
c4_1 = create_card(s4, 1.5, 1.5, step_w, 8.8, "Step 1: The Reader", "Document Ingestion")
tf4_1 = c4_1.text_frame
add_bullet(tf4_1, "What It Does", "Reads 670 scientific PDFs and cleans layout noise.")
add_bullet(tf4_1, "PyMuPDF (fitz)", "Strips page numbers, headers, and fixes two-column text.")
add_bullet(tf4_1, "LlamaIndex", "Chops papers into 14,850 bite-sized chunks (512 tokens each).")
add_bullet(tf4_1, "Storage", "Saves chunks into ChromaDB (vector) + PostgreSQL (data).")

c4_2 = create_card(s4, 5.8, 1.5, step_w, 8.8, "Step 2: The Detective", "Hybrid Search & Reranking")
tf4_2 = c4_2.text_frame
add_bullet(tf4_2, "Dual Searching", "BM25 searches exact formula words; BGE finds conceptual meaning.")
add_bullet(tf4_2, "RRF Fusion (k=60)", "Combines both search scores fairly without bias.")
add_bullet(tf4_2, "BGE Cross-Encoder", "Deep re-reading of top 20 chunks to pick the 5 best evidence passages.")
add_bullet(tf4_2, "The Lift", "Pushes search rank (MRR) from 0.81 to an outstanding 0.972!")

c4_3 = create_card(s4, 10.1, 1.5, step_w, 8.8, "Step 3: The Writer & Inspector", "Gemini + Phase 3.4 Verification", border_color=AMBER)
tf4_3 = c4_3.text_frame
add_bullet(tf4_3, "Gemini 2.5 Flash", "Writes a structured synthesis strictly using the top 5 chunks.")
add_bullet(tf4_3, "Claim Slicer", "Splits the answer into sentence-level atomic claims.")
add_bullet(tf4_3, "NLI Inspector", "Tests if each claim is Entailed (proved) or Neutral (guessing).")
add_bullet(tf4_3, "Auto-Repair Loop", "Surgically rewrites or cuts unproven claims automatically!")

c4_4 = create_card(s4, 14.4, 1.5, step_w, 8.8, "Step 4: The Presentation", "Interactive Frontend & XAI", border_color=EMERALD)
tf4_4 = c4_4.text_frame
add_bullet(tf4_4, "React 18 + Vite", "Fast, modern user interface with 14 modular tabs.")
add_bullet(tf4_4, "XAI Heatmaps", "Visual color highlights on source text so students can verify proof.")
add_bullet(tf4_4, "Matrix Builder", "Auto-builds side-by-side comparison tables across papers.")
add_bullet(tf4_4, "LaTeX Compiler", "Exports ready-to-compile IEEE manuscripts in seconds.")


# ==================== SLIDE 5: DATASET & IMPLEMENTATION ====================
print("Styling Slide 5...")
s5 = prs.slides[4]
clear_content_shapes(s5, 3)
add_header_subtitle(s5, "DATASET & IMPLEMENTATION", "Story: \"Our Cleaned Library & 14 Working Tools\"")

c5_1 = create_card(s5, 1.5, 1.5, 5.3, 8.8, "1. The Curated Library", "Material Science Corpus")
tf5_1 = c5_1.text_frame
add_bullet(tf5_1, "670 Peer-Reviewed Papers", "Real research from Nature Materials, Advanced Energy Materials, arXiv.")
add_bullet(tf5_1, "Key Sub-Fields", "Perovskite solar cells, solid-state batteries (Li10GeP2S12), 2D MXenes, MOFs.")
add_bullet(tf5_1, "14,850 Cleaned Chunks", "Chunked at 512 tokens with 64-token overlap so no sentences get cut.")
add_bullet(tf5_1, "Frozen Benchmark", "ds_nexus_v10 suite (15 gold-standard test queries with human-labeled answers).")

c5_2 = create_card(s5, 7.3, 1.5, 5.3, 8.8, "2. Tech Stack at Work", "Tools & Frameworks")
tf5_2 = c5_2.text_frame
add_bullet(tf5_2, "Frontend", "React 18, TypeScript, Tailwind CSS, Lucide icons, Vite.")
add_bullet(tf5_2, "Backend API", "FastAPI (Python 3.11 asynchronous ASGI engine).")
add_bullet(tf5_2, "AI Models", "BAAI/bge-base-en-v1.5, BGE-Reranker-base, Google Gemini 2.5 Flash.")
add_bullet(tf5_2, "Databases", "ChromaDB (vector similarity) + PostgreSQL (sessions & audit logs).")

c5_3 = create_card(s5, 13.1, 1.5, 5.4, 8.8, "3. Implementation Status", "14 Implemented Modules", border_color=EMERALD)
tf5_3 = c5_3.text_frame
add_bullet(tf5_3, "Paper Explorer & Navigator", "100% Complete (browse & filter 670 papers)")
add_bullet(tf5_3, "Hybrid Search + Reranker", "100% Complete (fuses BM25 + dense vectors)")
add_bullet(tf5_3, "Phase 3.4 Claim Verifier", "100% Complete (NLI entailment + auto-repair)")
add_bullet(tf5_3, "XAI Attribution Heatmaps", "100% Complete (token visual evidence)")
add_bullet(tf5_3, "Comparison Matrix & LaTeX", "100% Complete (table synthesis & IEEE export)")
add_bullet(tf5_3, "Current System Progress", "98.5% Functional — 100% Ready for Live Demo!")


# ==================== SLIDE 6: RESULTS, CHALLENGES & NEXT STEPS ====================
print("Styling Slide 6...")
s6 = prs.slides[5]
clear_content_shapes(s6, 3)
add_header_subtitle(s6, "RESULTS, CHALLENGES & NEXT STEPS", "Story: \"The Proof in Numbers & What We Conquered\"")

c6_1 = create_card(s6, 1.5, 1.5, 5.3, 8.8, "1. The Benchmark Proof", "ds_nexus_v10 (N=15 Frozen Test)")
tf6_1 = c6_1.text_frame
add_bullet(tf6_1, "E01: Hybrid Baseline", "MRR 0.812 | Precision 82.4% | Unsupported 16.8%")
add_bullet(tf6_1, "E02: + Cross-Encoder", "MRR 0.972 (+20%) | Hit Rate 100% | Precision 88.6%")
add_bullet(tf6_1, "E03: + Strict Grounding", "Citation Precision 94.7% | Unsupported 4.6%")
add_bullet(tf6_1, "E04: + Phase 3.4 Verify", "Citation Precision 98.0% | Unsupported ONLY 1.0%!")
add_bullet(tf6_1, "E05: + Iterative Loop", "Citation Precision 99.2% | Unsupported 0.5%")

c6_2 = create_card(s6, 7.3, 1.5, 5.3, 8.8, "2. Hurdles We Solved", "Engineering Challenges", border_color=AMBER)
tf6_2 = c6_2.text_frame
add_bullet(tf6_2, "Missing Chemical Names", "Vectors mixed up similar formulas -> Fixed by adding BM25 exact match.")
add_bullet(tf6_2, "Slow Reranking Speed", "Cross-encoders took 4.5s -> Fixed by funneling only top-20 chunks (480ms).")
add_bullet(tf6_2, "Made-Up Citations", "LLMs cited non-existent chunk IDs -> Fixed by schema validators cutting fake IDs.")
add_bullet(tf6_2, "Messy PDF Columns", "Multi-column text mixed sentences -> Fixed by PyMuPDF box coordinates.")

c6_3 = create_card(s6, 13.1, 1.5, 5.4, 8.8, "3. What's Next?", "Future Roadmap", border_color=PRIMARY)
tf6_3 = c6_3.text_frame
add_bullet(tf6_3, "Knowledge Graphs", "Connect materials, temperatures, and properties via Neo4j Graph RAG.")
add_bullet(tf6_3, "XRD Chart Reader", "Read 2D diffraction curves and lab graphs using multimodal vision AI.")
add_bullet(tf6_3, "Local Offline AI", "Run 100% on private local GPUs (Llama 3 8B) for proprietary industry labs.")


# ==================== SLIDE 7: RESEARCH & PAPER PUBLICATION PROGRESS ====================
print("Styling Slide 7...")
s7 = prs.slides[6]
clear_content_shapes(s7, 3)
add_header_subtitle(s7, "RESEARCH & PAPER PUBLICATION PROGRESS", "Story: \"Our Scientific Contribution & Manuscript Readiness\"")

c7_1 = create_card(s7, 1.5, 1.5, 5.3, 8.8, "1. Target Venues & Title", "Where We Are Submitting")
tf7_1 = c7_1.text_frame
add_bullet(tf7_1, "Paper Final Title", "\"ResearchMind: An Explainable, Attributed, and Self-Refining Scientific Research Operating System for Material Science Literature\"")
add_bullet(tf7_1, "Target Conference", "IEEE International Conference on Big Data / IEEE ICDM / Springer LNCS.")
add_bullet(tf7_1, "Domain Track", "Applied AI, Natural Language Processing, and Information Retrieval.")

c7_2 = create_card(s7, 7.3, 1.5, 5.3, 8.8, "2. 3 Core Contributions", "What Science Gains")
tf7_2 = c7_2.text_frame
add_bullet(tf7_2, "1. Hybrid Scientific RRF", "Proved BM25 + Dense RRF boosts chemical formula retrieval MRR to 0.972.")
add_bullet(tf7_2, "2. Phase 3.4 Auto-Repair", "First post-gen claim-level NLI repair reducing scientific RAG errors to 1.0%.")
add_bullet(tf7_2, "3. Transparent Research OS", "End-to-end open architecture with interactive token XAI heatmaps and LaTeX output.")

c7_3 = create_card(s7, 13.1, 1.5, 5.4, 8.8, "3. Writing & Audit Status", "Publication Readiness", border_color=EMERALD)
tf7_3 = c7_3.text_frame
add_bullet(tf7_3, "Sections Completed", "Abstract, Intro, Related Work, Architecture, Math, Benchmark, Results (98% Done).")
add_bullet(tf7_3, "LaTeX Compilations", "Compiled in IEEEtran and Springer LNCS formats with 42 verified citations.")
add_bullet(tf7_3, "Audit Readiness Score", "143 / 170 Points (84.1% Submission Ready).")
add_bullet(tf7_3, "Current Status", "Ready for Internal Review (Awaiting final mentor sign-off before upload).")

prs.save(PPTX_PATH)
print("PPT updated successfully!")
