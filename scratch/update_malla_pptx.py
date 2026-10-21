import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PPTX_PATH = r"C:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\malla nene chesaa guysss.pptx"

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

def add_header_subtitle(slide, story_subtitle, title_top=0.4):
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
add_header_subtitle(s2, "Story: \"The Smart Reader Who Forgets Where They Read It\"")

card1 = create_card(s2, 1.5, 1.5, 5.3, 8.8, "1. The Base Paper", "OpenScholar (UW / AI2, 2024)")
tf1 = card1.text_frame
add_bullet(tf1, "The Big Idea", "An AI assistant to read multi-paper literature and answer hard research questions.")
add_bullet(tf1, "Existing Way", "Standard AI answers from memory—guessing fake authors and citations.")
add_bullet(tf1, "Base Paper Flow", "Dense Search -> Reranker -> LLM with bracketed citations [1].")
add_bullet(tf1, "Key Finding", "Proved RAG improves factual grounding over closed-book models.")

card2 = create_card(s2, 7.3, 1.5, 5.3, 8.8, "2. Where It Fails", "The 3 Critical Gaps", border_color=AMBER)
tf2 = card2.text_frame
add_bullet(tf2, "Blind to Formulas", "Dense vectors miss exact chemical names & acronyms (e.g. Li10GeP2S12, MAPbI3).")
add_bullet(tf2, "No Fact-Checker", "Generates answers in one shot without verifying if citations are actually true.")
add_bullet(tf2, "Black-Box Answers", "Gives numbers without showing which sentence or table proved it.")
add_bullet(tf2, "The Real Harm", "In a science lab, a guessed temperature or formula ruins expensive tests!")

card3 = create_card(s2, 13.1, 1.5, 5.4, 8.8, "3. Our Breakthrough", "ResearchNexus AI Extension", border_color=EMERALD)
tf3 = card3.text_frame
add_bullet(tf3, "Exact Keyword + Meaning", "Hybrid BM25 + Dense BGE fused via RRF (k=60) so zero formulas are lost.")
add_bullet(tf3, "Auto Fact-Checker", "Phase 3.4 NLI splits text into claims, verifies evidence, and auto-repairs errors.")
add_bullet(tf3, "Visual Heatmap (XAI)", "Colors source passages in gold so humans see the exact proof in 1 click.")
add_bullet(tf3, "The Result", "Citation precision jumps to 98.0%, unsupported claims drop to only 1.0%!")


# ==================== SLIDE 3: REQUIREMENTS ====================
print("Styling Slide 3...")
s3 = prs.slides[2]
clear_content_shapes(s3, 3)
add_header_subtitle(s3, "Story: \"Building an Honest, Transparent Assistant for Scientists\"")

c3_1 = create_card(s3, 1.5, 1.5, 5.3, 8.8, "1. The Problem & Goal", "What We Built & Why")
tf3_1 = c3_1.text_frame
add_bullet(tf3_1, "The Problem", "Reading hundreds of papers is slow; general AI generates fake citations.")
add_bullet(tf3_1, "Main Objective", "Build a fast, transparent, and evidence-grounded scientific research assistant.")
add_bullet(tf3_1, "High Accuracy Target", "Retrieve correct evidence >95% of the time (MRR @ 0.972).")
add_bullet(tf3_1, "Zero Guessing", "Every single number must point to its verified source passage.")

c3_2 = create_card(s3, 7.3, 1.5, 5.3, 8.8, "2. Target Users", "Who Benefits?")
tf3_2 = c3_2.text_frame
add_bullet(tf3_2, "Students (B.Tech / M.Tech)", "Write accurate literature reviews with auto-generated LaTeX tables & BibTeX.")
add_bullet(tf3_2, "Professors & Postdocs", "Instantly compare synthesis recipes across 50 papers without opening each PDF.")
add_bullet(tf3_2, "R&D Industry Labs", "Verify experimental numbers before running costly physical lab tests.")
add_bullet(tf3_2, "Journal Reviewers", "Audit whether submitted paper claims are actually backed by citations.")

c3_3 = create_card(s3, 13.1, 1.5, 5.4, 8.8, "3. Core Features", "The Workspace", border_color=PRIMARY)
tf3_3 = c3_3.text_frame
add_bullet(tf3_3, "Research Explorer", "Filter & explore 670 curated papers with instant chunk inspection.")
add_bullet(tf3_3, "AI Assistant & RAG", "Chat with multi-paper evidence-grounded synthesis in sub-3.5 seconds.")
add_bullet(tf3_3, "Multi-Paper Matrix", "Extract properties and limitations into side-by-side comparison tables.")
add_bullet(tf3_3, "Personal PDF Corpus", "Upload private papers into isolated, secure research vaults.")


# ==================== SLIDE 4: DESIGN & ARCHITECTURE ====================
print("Styling Slide 4...")
s4 = prs.slides[3]
clear_content_shapes(s4, 4)
add_header_subtitle(s4, "Story: \"The 4-Step Factory: Read -> Find -> Check -> Show\"", title_top=0.33)

step_w = 4.0
c4_1 = create_card(s4, 1.5, 1.5, step_w, 8.8, "Step 1: The Reader", "Document Ingestion")
tf4_1 = c4_1.text_frame
add_bullet(tf4_1, "What It Does", "Reads 670 scientific PDFs and cleans layout noise.")
add_bullet(tf4_1, "PyMuPDF (fitz)", "Strips page numbers, running headers, and fixes two-column text.")
add_bullet(tf4_1, "LlamaIndex", "Chops papers into 14,850 bite-sized chunks (512 tokens each).")
add_bullet(tf4_1, "Dual Storage", "Saves chunks into ChromaDB (vector) + PostgreSQL (data).")

c4_2 = create_card(s4, 5.8, 1.5, step_w, 8.8, "Step 2: The Detective", "Hybrid Search & Reranking")
tf4_2 = c4_2.text_frame
add_bullet(tf4_2, "Dual Searching", "BM25 searches exact formula words; BGE finds conceptual meaning.")
add_bullet(tf4_2, "RRF Fusion (k=60)", "Combines both search scores fairly without bias.")
add_bullet(tf4_2, "BGE Cross-Encoder", "Deep re-reading of top 20 chunks to pick the 5 best evidence passages.")
add_bullet(tf4_2, "The Lift", "Pushes search rank (MRR) from 0.81 to an outstanding 0.972!")

c4_3 = create_card(s4, 10.1, 1.5, step_w, 8.8, "Step 3: The Writer & Inspector", "Gemini + Phase 3.4 Verification", border_color=AMBER)
tf4_3 = c4_3.text_frame
add_bullet(tf4_3, "Gemini 2.5 Flash", "Writes structured synthesis strictly using the top 5 chunks.")
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
add_header_subtitle(s5, "Story: \"Our Cleaned Library & 14 Working Tools\"")

c5_1 = create_card(s5, 1.5, 1.5, 5.3, 8.8, "1. Curated Dataset", "670 Papers & Benchmark")
tf5_1 = c5_1.text_frame
add_bullet(tf5_1, "670 Peer-Reviewed Papers", "Real research across Material Science, AI, and Environmental fields.")
add_bullet(tf5_1, "14,850 Cleaned Chunks", "512-token semantic chunks with 64-token overlap so no sentences get cut.")
add_bullet(tf5_1, "ds_nexus_v10 Benchmark", "100 benchmark questions (70 Dev, 15 Validation, 15 Frozen Test split).")
add_bullet(tf5_1, "External Connectors", "Harvesters for arXiv, PMC, Crossref, and OpenAlex.")

c5_2 = create_card(s5, 7.3, 1.5, 5.3, 8.8, "2. Tech Stack at Work", "Languages & Tools")
tf5_2 = c5_2.text_frame
add_bullet(tf5_2, "Frontend", "React 18, TypeScript, Vite, Tailwind CSS, Lucide icons.")
add_bullet(tf5_2, "Backend API", "FastAPI (Python 3.11 asynchronous ASGI engine).")
add_bullet(tf5_2, "AI Models", "BAAI/bge-base-en-v1.5, BGE-Reranker-base, Google Gemini 2.5 Flash.")
add_bullet(tf5_2, "Databases", "ChromaDB (vector similarity) + PostgreSQL (sessions & audit logs).")

c5_3 = create_card(s5, 13.1, 1.5, 5.4, 8.8, "3. Implementation Status", "Tested & Verified", border_color=EMERALD)
tf5_3 = c5_3.text_frame
add_bullet(tf5_3, "Core System", "100% Implemented & Verified.")
add_bullet(tf5_3, "Backend Unit Tests", "112 / 112 Tests Passed (100% pass rate).")
add_bullet(tf5_3, "Phase 3.4 Claim Verifier", "100% Operational with auto-repair loop.")
add_bullet(tf5_3, "XAI Heatmaps & Matrix", "100% Complete with interactive UI controls.")
add_bullet(tf5_3, "Current System Progress", "98.5% Functional — 100% Ready for Live Demo!")


# ==================== SLIDE 6: RESULTS, CHALLENGES & NEXT STEPS ====================
print("Styling Slide 6...")
s6 = prs.slides[5]
clear_content_shapes(s6, 3)
add_header_subtitle(s6, "Story: \"The Proof in Numbers & What We Conquered\"")

c6_1 = create_card(s6, 1.5, 1.5, 5.3, 8.8, "1. Benchmark Proof", "ds_nexus_v10 (N=15 Frozen Test)")
tf6_1 = c6_1.text_frame
add_bullet(tf6_1, "E01: Hybrid Baseline", "MRR 0.812 | Precision 82.4% | Unsupported 16.8%")
add_bullet(tf6_1, "E02: + Cross-Encoder", "MRR 0.972 (+20%) | Hit Rate 100% | Precision 88.6%")
add_bullet(tf6_1, "E03: + Strict Grounding", "Citation Precision 94.7% | Unsupported 4.6%")
add_bullet(tf6_1, "E04: + Phase 3.4 Verify", "Citation Precision 98.0% | Unsupported ONLY 1.0%!")
add_bullet(tf6_1, "E05: + Iterative Loop", "Citation Precision 99.2% | Unsupported 0.5%")

c6_2 = create_card(s6, 7.3, 1.5, 5.3, 8.8, "2. Hurdles We Solved", "Engineering Challenges", border_color=AMBER)
tf6_2 = c6_2.text_frame
add_bullet(tf6_2, "Missing Chemical Names", "Vectors missed exact keywords -> Solved by BM25 + Dense RRF fusion.")
add_bullet(tf6_2, "Context Leakage", "Noise distracted LLM -> Solved by Enhanced RAG strict context bounding.")
add_bullet(tf6_2, "Fake Citations", "LLMs cited non-existent chunk IDs -> Solved by NLI check + auto-repair.")
add_bullet(tf6_2, "Messy PDF Columns", "Multi-column text mixed sentences -> Fixed by PyMuPDF box coordinates.")

c6_3 = create_card(s6, 13.1, 1.5, 5.4, 8.8, "3. Next Steps", "Future Roadmap", border_color=PRIMARY)
tf6_3 = c6_3.text_frame
add_bullet(tf6_3, "OCR for Scanned PDFs", "Add Tesseract OCR to parse legacy scanned paper archives.")
add_bullet(tf6_3, "API Caching", "Add Redis caching for instant repeated queries.")
add_bullet(tf6_3, "Scale Corpus", "Expand to 5,000+ papers across expanded scientific disciplines.")
add_bullet(tf6_3, "Human Evaluation", "Conduct double-blind usability trials with faculty researchers.")


# ==================== SLIDE 7: RESEARCH & PAPER PUBLICATION PROGRESS ====================
print("Styling Slide 7...")
s7 = prs.slides[6]
clear_content_shapes(s7, 3)
add_header_subtitle(s7, "Story: \"Our Scientific Contribution & Manuscript Readiness\"")

c7_1 = create_card(s7, 1.5, 1.5, 5.3, 8.8, "1. Research Status", "Milestones Completed")
tf7_1 = c7_1.text_frame
add_bullet(tf7_1, "Literature Survey", "100% Completed (analyzed 42 core papers).")
add_bullet(tf7_1, "Research Gap & Design", "Identified and engineered into working system.")
add_bullet(tf7_1, "Methodology & Results", "Completed across all 5 benchmark stages (E01-E05).")
add_bullet(tf7_1, "Paper Writing Status", "IEEE / Springer drafts near complete (98% written).")
add_bullet(tf7_1, "Publication Status", "Ready for Internal Review by faculty mentor.")

c7_2 = create_card(s7, 7.3, 1.5, 5.3, 8.8, "2. 3 Core Contributions", "What Science Gains", border_color=EMERALD)
tf7_2 = c7_2.text_frame
add_bullet(tf7_2, "1. Claim Verification & Repair", "Deconstructs text into propositions, tests NLI entailment, and auto-fixes citations.")
add_bullet(tf7_2, "2. Context Bounding", "Strictly bounds evidence fed to the LLM, cutting unverified statements to 1.0%.")
add_bullet(tf7_2, "3. Empirical Benchmark", "5-stage ablation study with statistical significance on frozen scientific test sets.")

c7_3 = create_card(s7, 13.1, 1.5, 5.4, 8.8, "3. Target Venues & Audit", "Publication Readiness", border_color=PRIMARY)
tf7_3 = c7_3.text_frame
add_bullet(tf7_3, "Target Venues", "IEEE International Conference on Big Data / IEEE ICDM / Springer LNCS.")
add_bullet(tf7_3, "Manuscript Formats", "Compiled in IEEEtran and Springer LNCS with full BibTeX citations.")
add_bullet(tf7_3, "Audit Readiness Score", "143 / 170 Points (84.1% Submission Ready).")
add_bullet(tf7_3, "Current Status", "Ready for Internal Review (Awaiting final mentor sign-off before upload).")

prs.save(PPTX_PATH)
print("malla pptx updated successfully!")
