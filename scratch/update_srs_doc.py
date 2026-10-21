import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

SOURCE_SRS = r"C:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\SRS_V1_ (2).docx"
BACKUP_SRS = r"C:\Users\Abyureddy\OneDrive\Desktop\SDC2\SDC Review 1\SRS_V1_BACKUP_ORIGINAL.docx"

if not os.path.exists(BACKUP_SRS):
    shutil.copyfile(SOURCE_SRS, BACKUP_SRS)
    print("Created backup of original SRS.")

doc = Document(SOURCE_SRS)

# Define clean styles and colors
NAVY = RGBColor(15, 23, 42)
BLUE = RGBColor(37, 99, 235)
MUTED = RGBColor(100, 116, 139)

def style_heading(p, level):
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    for r in p.runs:
        r.font.name = "Calibri"
        if level == 1:
            r.font.size = Pt(18)
            r.font.bold = True
            r.font.color.rgb = NAVY
        elif level == 2:
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = BLUE
        elif level == 3:
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = NAVY

def set_para_clean(p, size=11, bold=False, italic=False, color=None, space_after=4):
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    for r in p.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        if color:
            r.font.color.rgb = color

# Clean up broken characters across all paragraphs
for p in doc.paragraphs:
    if "" in p.text:
        for r in p.runs:
            r.text = r.text.replace("", "–").replace("  ", " ")

print(f"Total paragraphs in document: {len(doc.paragraphs)}")

# Humanize Chapter 1
# Locate 1.1 Purpose
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if txt == "1.1 Purpose":
        if i+1 < len(doc.paragraphs):
            doc.paragraphs[i+1].text = (
                "The purpose of this Software Requirements Specification (SRS) is to describe the complete "
                "functionality, architecture, and quality standards for ResearchNexusAI. "
                "In simple words, this document explains what problem ResearchNexusAI solves, how it works under the hood, "
                "and how each feature—from paper search to claim verification—is designed so that engineers, reviewers, "
                "and academic evaluators can clearly understand and assess the project."
            )
            set_para_clean(doc.paragraphs[i+1])
    elif txt == "1.2 Scope":
        if i+1 < len(doc.paragraphs):
            doc.paragraphs[i+1].text = (
                "ResearchNexusAI is an intelligent, web-based scientific research assistant. "
                "When researchers and students study complex scientific topics, they often have to read hundreds of PDFs, "
                "compare contradictory numbers, and worry about whether general AI tools are hallucinating fake citations. "
                "ResearchNexusAI solves this by reading scientific papers, indexing both exact chemical keywords and deep concepts, "
                "and generating answers where every single sentence is checked against the original paper before being shown to the user."
            )
            set_para_clean(doc.paragraphs[i+1])
        if i+2 < len(doc.paragraphs):
            doc.paragraphs[i+2].text = (
                "Key capabilities include: (1) Hybrid Search combining BM25 exact matching and BGE vector similarity; "
                "(2) Phase 3.4 Claim Verification that tests whether citations actually prove what the AI claims; "
                "(3) Explainable AI (XAI) heatmaps that highlight proof in the source paper; and "
                "(4) Multi-paper comparison matrices with one-click export to IEEE and Springer LaTeX formats."
            )
            set_para_clean(doc.paragraphs[i+2])

# Humanize Chapter 2
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if txt == "2.1 Product Perspective":
        if i+1 < len(doc.paragraphs):
            doc.paragraphs[i+1].text = (
                "ResearchNexusAI is designed as an independent, full-stack Scientific Research Operating System. "
                "Unlike a generic chatbot that answers from memory, ResearchNexusAI acts like a dedicated research assistant "
                "with access to a curated local library of 670 peer-reviewed papers and 14,850 semantic chunks. "
                "It connects a modern React web interface to a high-speed Python FastAPI backend, supported by ChromaDB for "
                "instant vector search and PostgreSQL for audit trails and research memory."
            )
            set_para_clean(doc.paragraphs[i+1])
    elif txt == "2.2 Product Functions":
        if i+1 < len(doc.paragraphs):
            doc.paragraphs[i+1].text = (
                "The primary functions of ResearchNexusAI are organized into five clear steps: "
                "\n1. Ingestion: Reads academic PDFs, removes page numbers and headers, and breaks them into clean 512-token chunks."
                "\n2. Hybrid Search: Uses both BM25 for exact chemical formulas and BGE embeddings for conceptual meaning, fused via RRF (k=60)."
                "\n3. Cross-Encoder Reranking: Re-evaluates top candidate passages to pick the 5 best evidence chunks (MRR 0.972)."
                "\n4. Grounded Synthesis: Gemini 2.5 Flash writes answers strictly using the top evidence."
                "\n5. Claim Verification & Repair: Checks every sentence with Natural Language Inference (NLI); if a claim is unsupported, it rewrites it automatically."
            )
            set_para_clean(doc.paragraphs[i+1])
    elif txt == "2.3 User Classes and Characteristics":
        if i+1 < len(doc.paragraphs):
            doc.paragraphs[i+1].text = (
                "ResearchNexusAI is built for four main groups of users:"
                "\n• Undergraduate & Graduate Students: Need quick, reliable summaries for assignments and literature surveys without fear of fake citations."
                "\n• Academic Researchers & Faculty: Need to compare experimental numbers, synthesis methods, and limitations across 20+ papers simultaneously."
                "\n• R&D Industry Scientists: Work on materials, batteries, and solar cells where an incorrect synthesis temperature or formula can cause laboratory failure."
                "\n• Peer Reviewers & Editors: Want to audit whether claims in submitted manuscripts are genuinely supported by cited references."
            )
            set_para_clean(doc.paragraphs[i+1])

# Humanize Chapter 4 Features
feature_human_text = {
    "4.1 User Authentication": (
        "Provides secure, frictionless login and session management so that each researcher's notes, "
        "uploaded personal PDFs, and search histories remain private and strictly isolated."
    ),
    "4.2 Dashboard": (
        "The central control hub where researchers can view recent searches, open paper vaults, "
        "track verification stats, and resume saved research sessions with one click."
    ),
    "4.3 Research Domain Management": (
        "Allows researchers to switch between scientific domains (such as Material Science, Energy Storage, and AI) "
        "to ensure search models prioritize domain-specific terminology and metrics."
    ),
    "4.4 Hybrid Search & Retrieval": (
        "Combines the best of two search worlds: Okapi BM25 finds exact alphanumeric chemical formulas (like Li10GeP2S12), "
        "while BGE dense vectors understand semantic concepts. Reciprocal Rank Fusion (k=60) merges them, and a Cross-Encoder "
        "picks the top 5 most relevant evidence passages."
    ),
    "4.5 Dynamic Data Ingestion": (
        "A fast document pipeline using PyMuPDF that reads multi-column PDFs, removes header/footer clutter, "
        "and splits text into 512-token chunks using LlamaIndex without cutting sentences in half."
    ),
    "4.6 AI Research Assistant": (
        "An interactive chat workspace powered by Gemini 2.5 Flash that provides multi-turn scientific reasoning, "
        "mathematical derivations (rendered in KaTeX), and inline citations linked to source chunks."
    ),
    "4.7 Explainable AI": (
        "Demystifies AI answers by showing visual token heatmaps on source passages. "
        "Users can click any sentence in the answer and instantly see the exact lines in the original PDF that prove it."
    ),
    "4.8 Research Workspace": (
        "A focused distraction-free study environment where users can read extracted chunks, take notes, "
        "and pin verified facts directly into their active workspace."
    ),
    "4.9 Literature Review Builder": (
        "Automatically organizes multi-paper insights into structured literature review sections "
        "(Background, Methods, Findings, Open Gaps) with formatted citations."
    ),
    "4.10 Notebook": (
        "An integrated digital lab notebook where researchers can store verified claims, synthesis steps, "
        "and custom annotations alongside source document links."
    ),
    "4.11 Project Management": (
        "Organizes papers, notes, queries, and synthesis drafts into distinct research projects or dissertation chapters."
    ),
    "4.12 Paper Library": (
        "An interactive digital bookshelf of 670 indexed papers with instant search, author filters, and DOI outbound links."
    ),
    "4.13 Analytics": (
        "Provides visual telemetry on retrieval precision, latency (average 3.2s end-to-end), "
        "and claim entailment rates across the user's research sessions."
    ),
    "4.14 Notifications": (
        "Alerts researchers when batch PDF indexing finishes or when automated claim verification flags an ungrounded statement."
    ),
    "4.15 Global Search": (
        "A universal spotlight search bar across all papers, saved notes, verified claims, and past query sessions."
    )
}

for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if txt in feature_human_text:
        # Check if next paragraph is 'Description'
        if i+2 < len(doc.paragraphs) and doc.paragraphs[i+1].text.strip() == "Description":
            doc.paragraphs[i+2].text = feature_human_text[txt]
            set_para_clean(doc.paragraphs[i+2])

# Humanize Chapter 5 Non-Functional Requirements
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if txt == "5.1 Performance Requirements":
        if i+1 < len(doc.paragraphs):
            doc.paragraphs[i+1].text = (
                "The system is built for speed and responsiveness: "
                "\n• Search Speed: Hybrid retrieval across 14,850 chunks finishes in under 650 ms."
                "\n• Reranking: BGE Cross-Encoder reranking over top-20 candidates completes in ~480 ms."
                "\n• Full Answer Generation: Complete synthesis, NLI claim verification, and citation linking take under 3.5 seconds."
                "\n• User Interface: 60 FPS smooth rendering with zero lag during live text streaming."
            )
            set_para_clean(doc.paragraphs[i+1])
    elif txt == "5.3 Security Requirements":
        if i+1 < len(doc.paragraphs):
            doc.paragraphs[i+1].text = (
                "User data protection is strictly enforced: "
                "\n• Passwords are encrypted using modern industry standards (bcrypt hashing)."
                "\n• Personal PDF uploads and private notes are strictly isolated per user account."
                "\n• All communications between the browser and the FastAPI backend use secure HTTPS/WSS channels."
            )
            set_para_clean(doc.paragraphs[i+1])

# Humanize Appendix B Analysis Models Text
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if txt == "B.1 System Workflow Diagram":
        if i+1 < len(doc.paragraphs):
            doc.paragraphs[i+1].text = (
                "How Data Moves Through ResearchNexusAI (Story Flow):\n"
                "1. Preparation: 670 scientific PDFs are cleaned, split into 14,850 chunks, and saved in vector & text indexes.\n"
                "2. User Question: The user asks a technical question with chemical formulas.\n"
                "3. Hybrid Search: BM25 finds exact formula words, BGE finds conceptual meaning, and RRF (k=60) merges them.\n"
                "4. Cross-Encoder: Reranks top 20 candidates to select the 5 most reliable evidence chunks.\n"
                "5. Grounded Synthesis: Gemini 2.5 Flash writes the answer using only the selected evidence.\n"
                "6. Phase 3.4 Verification: Every claim is tested using NLI. If a claim lacks proof, it is automatically repaired.\n"
                "7. Explainable Output: The user sees the verified answer, clickable citations, and gold XAI heatmaps."
            )
            set_para_clean(doc.paragraphs[i+1])

doc.save(SOURCE_SRS)
print("Updated SRS successfully!")
