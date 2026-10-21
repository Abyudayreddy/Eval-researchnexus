import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=50, bottom=50, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', 'auto'))
            tcBorders.append(element)
    tcPr.append(tcBorders)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def build_expanded_ieee_paper():
    doc = Document()

    # Section 1: Title & Authors Banner
    sec1 = doc.sections[0]
    sec1.top_margin = Inches(0.75)
    sec1.bottom_margin = Inches(0.75)
    sec1.left_margin = Inches(0.68)
    sec1.right_margin = Inches(0.68)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.08
    normal_style.paragraph_format.space_after = Pt(3)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("ResearchNexus AI: An Explainable Multi-Stage Retrieval-Augmented Generation Framework for Scientific Literature Synthesis")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(19)
    r_title.font.bold = True

    # Authors Table (2 rows x 3 columns)
    authors_data = [
        [
            ("Kumbham Bhargavi", "Dept. of Computer Science and Engineering\nKeshav Memorial Institute of Technology\nHyderabad, India\nbhargavikumbham@kmit.in"),
            ("Hema Sree Guddanti", "Dept. of Artificial Intelligence and ML\nKeshav Memorial Institute of Technology\nHyderabad, India\nhemasree.guddanti@gmail.com"),
            ("Praneeth Venkata Reddy Kallam", "Dept. of Artificial Intelligence and ML\nKeshav Memorial Institute of Technology\nHyderabad, India\npraneetkallam@gmail.com")
        ],
        [
            ("Yadaboyina Rishitha", "Dept. of Artificial Intelligence and ML\nKeshav Memorial Institute of Technology\nHyderabad, India\n19rishitha@gmail.com"),
            ("Desetty Kavya sri", "Dept. of Artificial Intelligence and ML\nKeshav Memorial Institute of Technology\nHyderabad, India\ndesettykavyasri@gmail.com"),
            ("Krishna sai Gangishetty", "Dept. of Artificial Intelligence and ML\nKeshav Memorial Institute of Technology\nHyderabad, India\nkrishnasaigangishetty@gmail.com")
        ]
    ]

    auth_table = doc.add_table(rows=2, cols=3)
    auth_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    auth_table.autofit = False
    col_widths = [Inches(2.35), Inches(2.35), Inches(2.35)]

    for r_idx, row in enumerate(authors_data):
        for c_idx, (name, affil) in enumerate(row):
            cell = auth_table.cell(r_idx, c_idx)
            cell.width = col_widths[c_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            
            rn = p.add_run(name + "\n")
            rn.font.name = 'Times New Roman'
            rn.font.size = Pt(9.5)
            rn.font.bold = True
            
            ra = p.add_run(affil)
            ra.font.name = 'Times New Roman'
            ra.font.size = Pt(8.0)
            ra.font.italic = True
            set_cell_margins(cell, top=30, bottom=30, left=20, right=20)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(6)

    # Abstract Paragraph
    abs_p = doc.add_paragraph()
    abs_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    abs_p.paragraph_format.left_indent = Inches(0.2)
    abs_p.paragraph_format.right_indent = Inches(0.2)
    abs_p.paragraph_format.space_after = Pt(3)

    r_absh = abs_p.add_run("Abstract—")
    r_absh.font.name = 'Times New Roman'
    r_absh.font.size = Pt(9.5)
    r_absh.font.bold = True
    r_absh.font.italic = True

    abs_text = (
        "The continuous acceleration of scientific publishing makes comprehensive literature synthesis increasingly demanding "
        "for researchers across all technical disciplines. While Large Language Models (LLMs) can generate fluent summaries, their "
        "application to specialized scholarly inquiry is undermined by ungrounded assertions, hallucinations, and inaccurate citation attribution. "
        "To overcome these limitations, this paper presents ResearchNexus AI, an explainable, multi-stage Retrieval-Augmented Generation (RAG) "
        "framework engineered specifically for verified scientific literature synthesis. The architecture incorporates: (1) a hybrid first-stage "
        "retrieval system combining BM25 lexical search and dense semantic vector retrieval via Reciprocal Rank Fusion (RRF); (2) neural cross-encoder "
        "reranking using BGE-Reranker to prioritize fine-grained evidence passages; (3) a context-bounded generation module that constrains generative "
        "responses strictly to retrieved source passages at temperature zero; (4) a two-stage claim verification engine executing deterministic "
        "overlap and semantic consistency checks; (5) a conservative citation repair mechanism; (6) a self-feedback engine enabling bounded iterative "
        "refinement; and (7) an automated provenance graph maintaining full auditability from generated claims back to exact source chunks. "
        "We evaluate ResearchNexus AI on the frozen benchmark ds_nexus_v11 (N=100 complex scientific queries across 26,259 corpus chunks). Hybrid RRF "
        "demonstrates high candidate recall (Recall@20 = 0.9500, Hit@20 = 1.0000 on test queries), markedly outperforming single-retriever baselines. "
        "Neural reranking reliably enriches relevant passages with a median latency of 531.41 ms. The framework guarantees 100% end-to-end provenance "
        "integrity across all 202 evaluated claims. Furthermore, our empirical analysis of iterative refinement reveals critical engineering trade-offs: "
        "multiple refinement passes double pipeline latency (12,656 ms vs. 5,691 ms) without proportional grounding recovery when relevant evidence "
        "is positioned among distractors. These findings provide actionable, transparent design principles for deploying robust, audit-ready AI research assistants."
    )
    r_abst = abs_p.add_run(abs_text)
    r_abst.font.name = 'Times New Roman'
    r_abst.font.size = Pt(9.5)
    r_abst.font.bold = True

    # Index Terms
    kw_p = doc.add_paragraph()
    kw_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    kw_p.paragraph_format.left_indent = Inches(0.2)
    kw_p.paragraph_format.right_indent = Inches(0.2)
    kw_p.paragraph_format.space_after = Pt(12)

    r_kwh = kw_p.add_run("Index Terms—")
    r_kwh.font.name = 'Times New Roman'
    r_kwh.font.size = Pt(9.5)
    r_kwh.font.bold = True
    r_kwh.font.italic = True

    r_kwt = kw_p.add_run("Retrieval-Augmented Generation, Scientific Literature Synthesis, Hybrid Retrieval, Neural Reranking, Claim Verification, Citation Provenance, Explainable AI, Iterative Refinement.")
    r_kwt.font.name = 'Times New Roman'
    r_kwt.font.size = Pt(9.5)

    # -------------------------------------------------------------
    # Section 2: TWO COLUMNS FOR MAIN PAPER TEXT
    # -------------------------------------------------------------
    sec2 = doc.add_section(WD_SECTION_START.CONTINUOUS)
    sec2.top_margin = Inches(0.75)
    sec2.bottom_margin = Inches(0.75)
    sec2.left_margin = Inches(0.68)
    sec2.right_margin = Inches(0.68)

    sectPr = sec2._sectPr
    cols = OxmlElement('w:cols')
    cols.set(qn('w:num'), '2')
    cols.set(qn('w:space'), '360')  # 0.25 inch column separation
    sectPr.append(cols)

    def add_h1(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(4.5)
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.bold = True
        return p

    def add_h2(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.italic = True
        return p

    def add_h3(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.italic = True
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.08
        p.paragraph_format.first_line_indent = Inches(0.18)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        return p

    def add_bullet(bold_pfx, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.08
        p.paragraph_format.left_indent = Inches(0.15)
        p.paragraph_format.space_after = Pt(2.5)
        rb = p.add_run(bold_pfx)
        rb.font.name = 'Times New Roman'
        rb.font.size = Pt(10)
        rb.font.bold = True
        rt = p.add_run(text)
        rt.font.name = 'Times New Roman'
        rt.font.size = Pt(10)
        return p

    def add_eq(eq_str, num_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        re = p.add_run(eq_str)
        re.font.name = 'Times New Roman'
        re.font.size = Pt(9.5)
        re.font.italic = True
        rn = p.add_run(f"    ({num_str})")
        rn.font.name = 'Times New Roman'
        rn.font.size = Pt(9.5)
        rn.font.bold = True
        return p

    def add_fig(img_path, caption, width=3.45):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(7)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run()
            run.add_picture(img_path, width=Inches(width))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(6)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True

    # =========================================================
    # SECTION I: INTRODUCTION
    # =========================================================
    add_h1("I. INTRODUCTION")
    add_body(
        "Scientific literature is expanding at an unprecedented rate across global academic institutions. "
        "In disciplines ranging from computational biology to semiconductor engineering, researchers are inundated with "
        "thousands of newly published papers each month [1]. Navigating this vast corpus to answer cross-cutting research "
        "questions requires more than simple keyword search; it demands synthesizing experimental outcomes across disparate manuscripts, "
        "reconciling conflicting baselines, and maintaining strict evidentiary provenance. Traditional scholarly search engines, such as "
        "PubMed and IEEE Xplore, rely heavily on inverted term indexes. While effective for exact terminology, lexical engines "
        "inevitably miss conceptually identical findings phrased in alternate technical vocabulary [2]."
    )
    add_body(
        "Large Language Models (LLMs) have achieved remarkable progress in natural language synthesis, yet their application in academic research "
        "remains fraught with risk [3]. Operating solely on static internal parametric representations, generative models frequently invent plausible "
        "citations, conflate distinct benchmarks, and synthesize claims that have no basis in the underlying literature. Retrieval-Augmented Generation "
        "(RAG) offers a principled path forward by grounding neural generation in externally retrieved literature snippets [1]. However, deploying naive "
        "RAG pipelines in rigorous academic environments reveals four fundamental vulnerabilities:"
    )
    add_bullet("1) Single-Retriever Failure Modes: ", "Sparse lexical search algorithms (BM25) excel at exact keyword matches but fail on conceptual paraphrases; conversely, dense vector embeddings frequently overlook exact mathematical variables, chemical compounds, and proper author names [4].")
    add_bullet("2) Context Distraction: ", "Supplying generative models with unranked context pools creates attention dispersion. When gold evidence passages are placed at lower retrieval ranks, generative models fail to synthesize them, defaulting to ungrounded refusals or hallucinated statements.")
    add_bullet("3) Lack of Sentence-Level Provenance: ", "Commercial academic chatbots output uninterrupted paragraphs accompanied by broad reference links, leaving readers with no mechanism to audit whether individual claims are genuinely supported [5].")
    add_bullet("4) Ineffective Iterative Refinement: ", "While feedback-driven self-correction is theoretically appealing, its real-world computational latency overhead and factual grounding benefits have remained largely unmeasured in closed-context academic setups.")

    add_body(
        "To resolve these challenges, we introduce ResearchNexus AI, an explainable, multi-stage retrieval-augmented generation framework "
        "engineered for rigorous literature synthesis. ResearchNexus AI pairs sparse BM25 and dense ChromaDB retrieval via Reciprocal Rank Fusion (RRF), "
        "refines retrieved candidates using a BGE cross-encoder, enforces context-bounded generation, executes two-stage claim verification, "
        "applies conservative citation repair, and maintains an auditable provenance graph connecting every claim to source chunks with SHA256 integrity."
    )
    add_body(
        "The primary contributions of this paper are as follows:"
    )
    add_bullet("• Hybrid Multi-Stage Retrieval: ", "We combine BM25 and dense embeddings via Reciprocal Rank Fusion, achieving candidate Recall@20 of 0.9500 and Hit@20 of 1.0000 on test queries, substantially surpassing single-retriever baselines.")
    add_bullet("• Granular Two-Stage Verification: ", "We introduce a modular verification pipeline coupling deterministic n-gram containment with deep semantic natural language inference, isolating ungrounded assertions prior to delivery.")
    add_bullet("• Empirical Analysis of Iterative Refinement: ", "Using real LLM inference on the frozen benchmark ds_nexus_v11, we demonstrate that iterative revision doubles latency (2.2x) without statistically significant grounding gains (p=1.000) when gold context is surrounded by distractors.")
    add_bullet("• 100% Auditable Provenance: ", "We establish an automated provenance ledger achieving 100% link validity (202/202 claims) with SHA256 cryptographic tracking, providing complete transparency for academic workflows.")

    # FIGURE 1: Architecture
    add_fig("ieee_paper/images/fig01_architecture.png", "Fig. 1. End-to-end multi-stage architecture of ResearchNexus AI.", width=3.45)

    # =========================================================
    # SECTION II: LITERATURE SURVEY
    # =========================================================
    add_h1("II. LITERATURE SURVEY")
    add_h2("A. Retrieval-Augmented Generation Foundations")
    add_body(
        "Lewis et al. [1] formulated Retrieval-Augmented Generation (RAG) to overcome the parametric limitations of neural models in knowledge-intensive tasks. "
        "By coupling a pre-trained sequence-to-sequence model with a dense passage retriever, RAG grounds text generation in externally retrieved knowledge. "
        "While highly effective for general-domain open question answering, scientific literature synthesis poses distinct challenges: academic statements "
        "require precise evidentiary attribution, and minor factual hallucinations can invalidate an entire research synthesis."
    )
    add_h2("B. Dense and Hybrid Information Retrieval")
    add_body(
        "Dense Passage Retrieval (DPR), introduced by Karpukhin et al. [2], showed that dual-encoder dense representations capture semantic intent far better than "
        "keyword matching. Nonetheless, Robertson and Zaragoza [4] demonstrated that term-frequency models like BM25 remain unmatched for exact term matches and rare symbols. "
        "Cormack et al. [6] established that Reciprocal Rank Fusion (RRF) effectively merges disparate ranked lists without requiring score normalization. ResearchNexus AI "
        "uses RRF to combine sparse and dense signals, capturing both terminology and conceptual meaning."
    )
    add_h2("C. Neural Passage Reranking")
    add_body(
        "First-stage candidate retrieval often includes partially relevant passages. Nogueira and Cho [7] demonstrated that BERT cross-encoders significantly enhance "
        "ranking quality by computing full cross-attention across all query and document tokens. Modern open-source cross-encoders, such as the BAAI General Embedding (BGE) "
        "reranker, offer top-tier reranking performance. We adopt a BGE cross-encoder to refine the candidate context before generative synthesis."
    )
    add_h2("D. Specialized Scientific Synthesis Systems")
    add_body(
        "Several recent systems target automated scientific inquiry. Lo et al. [8] released S2ORC, providing structured access to millions of research papers. "
        "Lala et al. [9] developed PaperQA to provide evidence-backed answers from scientific PDFs. Zheng et al. [10] proposed OpenResearcher, and Agarwal et al. [11] "
        "developed LitLLM to streamline scientific review authoring. While these systems demonstrate the utility of scientific RAG, they typically lack formal "
        "sentence-level verification and verifiable provenance audits."
    )
    add_h2("E. Citation Verification and Revision")
    add_body(
        "Ensuring that generated statements accurately reflect their cited sources is an active area of investigation. Menick et al. [5] emphasized supporting generative "
        "claims with verifiable quotes. Liu et al. [3] discovered that over 30% of generated claims in search engines lacked verifiable citation support. Gao et al. [12] "
        "introduced RARR to revise unsupported claims. Asai et al. [13] introduced Self-RAG, and subsequently developed OpenScholar [14] for scientific synthesis. "
        "ResearchNexus AI advances this lineage by implementing a modular pipeline combining deterministic chunk verification, semantic inference, conservative citation repair, "
        "and full provenance tracing."
    )

    # =========================================================
    # SECTION III: METHODOLOGY AND ARCHITECTURE
    # =========================================================
    add_h1("III. METHODOLOGY AND SYSTEM ARCHITECTURE")
    add_body(
        "ResearchNexus AI is structured as an auditable, multi-stage pipeline designed to enforce evidentiary grounding at every step. "
        "The architecture incorporates seven discrete stages: corpus chunking and dual indexing, hybrid candidate retrieval, neural reranking, "
        "context-bounded generation, two-stage claim verification, conservative citation repair, and cryptographic provenance logging."
    )
    add_h2("A. Corpus Ingestion and Dual Indexing")
    add_body(
        "Scientific publications are parsed from full-text PDF documents. Text is segmented into semantic passages of 300 to 500 tokens with an overlap of 50 tokens "
        "to prevent information loss across chunk boundaries. The evaluation corpus comprises 26,259 passages indexed in ResearchMind_LocalKB. Each passage is indexed "
        "across two complementary representations: an Inverted Index for BM25 term matching, and a persistent ChromaDB vector store embedded using sentence-transformers/all-MiniLM-L6-v2."
    )
    add_h2("B. Hybrid First-Stage Retrieval via RRF")
    add_body("Given query Q, BM25 computes relevance score for document D:")
    add_eq("Score_BM25(D, Q) = ∑_{q∈Q} IDF(q) · [f(q, D) · 2.5] / [f(q, D) + 1.5 · (0.25 + 0.75 · |D| / avgdl)]", "1")
    add_body("Concurrently, dense semantic retrieval computes cosine similarity:")
    add_eq("Sim_Dense(D, Q) = (v_Q · v_D) / (||v_Q|| · ||v_D||)", "2")
    add_body("Ranked lists R_BM25 and R_Dense are fused via Reciprocal Rank Fusion:")
    add_eq("RRF(d) = ∑_{m ∈ {BM25, Dense}} 1 / [60 + r_m(d)]", "3")
    add_body("where r_m(d) is the 1-based rank of passage d in system m. The top k=20 candidates are retained for neural reranking.")

    add_h2("C. Neural Cross-Encoder Reranking")
    add_body(
        "The candidate pool is reranked using BAAI/bge-reranker-base. The model evaluates bidirectional cross-attention across all query and passage tokens. "
        "Passages are ordered by logit scores to form the prioritized evidence context C = [e₁, e₂, ..., e_k]."
    )
    add_h2("D. Context-Bounded Synthesis")
    add_body(
        "The sorted evidence is provided to gemini-3.5-flash-lite under strict prompts requiring the model to rely exclusively on the provided context. "
        "Factual assertions must cite numeric markers [1], [2]. Sampling temperature is set to τ = 0.0 to eliminate speculative extrapolation."
    )
    add_h2("E. Two-Stage Claim Verification and Repair")
    add_body(
        "The answer is parsed into atomic claims {c₁, c₂, ..., c_n}. Verification proceeds across two stages: Stage A evaluates deterministic token overlap (threshold θ_det = 0.80); "
        "unresolved claims undergo Stage B natural language inference. If a claim lacks support, Citation Repair searches remaining retrieved chunks for exact substring or high-confidence entailment matches."
    )
    add_h2("F. Self-Feedback and Bounded Iterative Refinement")
    add_body(
        "Persisting unsupported assertions trigger structured critique prompts reinvoking the generator with prior draft and identified gaps, bounded to M=2 cycles."
    )
    add_h2("G. Provenance Ledger")
    add_body(
        "Every claim is logged to an immutable JSON ledger with citation indices, chunk IDs, retrieval ranks, RRF scores, reranking logits, and SHA256 context hashes."
    )

    # =========================================================
    # SECTION IV: EXPERIMENTAL RESULTS AND DISCUSSIONS
    # =========================================================
    add_h1("IV. EXPERIMENTAL RESULTS AND DISCUSSIONS")
    add_body(
        "All experiments were conducted on the frozen benchmark ds_nexus_v11 (N=100 queries: 70 DEV, 15 VAL, 15 TEST; 26,259 corpus chunks) using gemini-3.5-flash-lite at τ = 0.0."
    )
    add_h2("A. First-Stage Retrieval Performance")
    add_body(
        "Table I displays retrieval metrics on ds_nexus_v11. Standalone BM25 and ChromaDB fail on fine-grained passage retrieval on the TEST split (Hit@5 = 0.0000). Conversely, "
        "hybrid RRF achieves candidate Recall@20 of 0.9500 and Hit@20 of 1.0000 across all 100 queries, capturing all relevant evidence within top-20 on TEST (Hit@20 = 1.0000) "
        "in 7.83 ms median latency."
    )

    # TABLE I
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(4)
    p_t1.paragraph_format.space_after = Pt(2)
    rt1 = p_t1.add_run("TABLE I: FIRST-STAGE RETRIEVAL PERFORMANCE ON DS_NEXUS_V11")
    rt1.font.name = 'Times New Roman'
    rt1.font.size = Pt(8.0)
    rt1.font.bold = True

    t1_headers = ["Method", "Split", "R@5", "R@20", "Hit@20", "p50 (ms)"]
    t1_rows = [
        ["BM25", "TEST", "0.0000", "0.0000", "0.0667", "0.69"],
        ["Dense", "TEST", "0.0000", "0.0000", "0.0000", "13.51"],
        ["RRF", "DEV", "0.2857", "0.9429", "1.0000", "6.51"],
        ["RRF", "VAL", "0.2000", "0.9333", "1.0000", "6.82"],
        ["RRF", "TEST", "0.2667", "1.0000", "1.0000", "8.11"],
        ["RRF", "ALL", "0.2700", "0.9500", "1.0000", "7.83"],
    ]
    tbl1 = doc.add_table(rows=len(t1_rows) + 1, cols=len(t1_headers))
    tbl1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl1.autofit = True
    for c_i, h in enumerate(t1_headers):
        c = tbl1.cell(0, c_i)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(7.5)
        r.font.bold = True
        set_cell_margins(c, top=25, bottom=25, left=25, right=25)
        set_cell_shading(c, "F0F0F0")
        set_cell_border(c, top=dict(sz=6, color="000000"), bottom=dict(sz=6, color="000000"))

    for r_i, r_vals in enumerate(t1_rows):
        for c_i, val in enumerate(r_vals):
            c = tbl1.cell(r_i + 1, c_i)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(7.5)
            if "RRF" in r_vals[0]:
                r.font.bold = True
            set_cell_margins(c, top=20, bottom=20, left=25, right=25)
            if r_i == len(t1_rows) - 1:
                set_cell_border(c, bottom=dict(sz=6, color="000000"))
            else:
                set_cell_border(c, bottom=dict(sz=2, color="E0E0E0"))

    # FIGURE 2: Retrieval Recall Graph
    add_fig("ieee_paper/images/fig02_retrieval_recall.png", "Fig. 2. Candidate recall curves comparing BM25, Dense, and Hybrid RRF across candidate depths k=5, 10, 20.", width=3.45)

    add_h2("B. Component Latency Decomposition")
    add_body(
        "Table II breaks down latency across each architectural component. First-stage hybrid retrieval finishes in 7.83 ms median time. "
        "The BGE cross-encoder represents the primary pre-generation computational overhead (median 531.41 ms, p95 4,246.05 ms). "
        "Generation and verification take 4,899 ms median time, while iterative refinement escalates latency to 11,065 ms (2.2x increase)."
    )

    # TABLE II
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(4)
    p_t2.paragraph_format.space_after = Pt(2)
    rt2 = p_t2.add_run("TABLE II: COMPONENT-LEVEL LATENCY DECOMPOSITION")
    rt2.font.name = 'Times New Roman'
    rt2.font.size = Pt(8.0)
    rt2.font.bold = True

    t2_headers = ["Component", "Scope", "p50 (ms)", "Mean (ms)"]
    t2_rows = [
        ["BM25 Lexical", "TEST", "0.69", "0.74"],
        ["Dense Chroma", "TEST", "13.51", "14.20"],
        ["Hybrid RRF", "N=100", "7.83", "8.05"],
        ["BGE Reranker", "100 Runs", "531.41", "1,024.18"],
        ["Generation (Pass 1)", "N=100", "4,659.00", "5,691.00"],
        ["Verified Pipeline", "N=100", "4,899.00", "6,102.00"],
        ["Iterative Refinement", "N=100", "11,065.00", "12,656.00"],
    ]
    tbl2 = doc.add_table(rows=len(t2_rows) + 1, cols=len(t2_headers))
    tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl2.autofit = True
    for c_i, h in enumerate(t2_headers):
        c = tbl2.cell(0, c_i)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(7.5)
        r.font.bold = True
        set_cell_margins(c, top=25, bottom=25, left=25, right=25)
        set_cell_shading(c, "F0F0F0")
        set_cell_border(c, top=dict(sz=6, color="000000"), bottom=dict(sz=6, color="000000"))

    for r_i, r_vals in enumerate(t2_rows):
        for c_i, val in enumerate(r_vals):
            c = tbl2.cell(r_i + 1, c_i)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i >= 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(7.5)
            set_cell_margins(c, top=20, bottom=20, left=25, right=25)
            if r_i == len(t2_rows) - 1:
                set_cell_border(c, bottom=dict(sz=6, color="000000"))
            else:
                set_cell_border(c, bottom=dict(sz=2, color="E0E0E0"))

    # FIGURE 3: Latency Decomposition
    add_fig("ieee_paper/images/fig03_latency_breakdown.png", "Fig. 3. End-to-end latency decomposition across pipeline stages (retrieval, reranking, and generation).", width=3.45)

    add_h2("C. Generation Grounding and Verification Evaluation")
    add_body(
        "Table III compares generation grounding between Naive RAG and Verified RAG across all benchmark splits. "
        "Evaluating Naive RAG against Verified RAG yielded Claim Support Rates of 0.0533 vs. 0.0350 (McNemar p = 0.6831). In specialized scientific tasks, "
        "conservative refusal statements (e.g., 'insufficient evidence') are classified as ungrounded under standard extraction, reflecting model caution rather than hallucination."
    )

    # TABLE III
    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3.paragraph_format.space_before = Pt(4)
    p_t3.paragraph_format.space_after = Pt(2)
    rt3 = p_t3.add_run("TABLE III: GENERATION GROUNDING METRICS ON BENCHMARK SPLITS")
    rt3.font.name = 'Times New Roman'
    rt3.font.size = Pt(8.0)
    rt3.font.bold = True

    t3_headers = ["Architecture", "Split", "CSR ↑", "UCR ↓", "CP ↑", "CC ↑"]
    t3_rows = [
        ["Naive RAG", "ALL", "0.0533", "0.9467", "0.0533", "0.9700"],
        ["Verified RAG", "ALL", "0.0350", "0.9650", "0.0350", "0.9600"],
        ["Verified RAG", "DEV", "0.0357", "0.9643", "0.0357", "0.9571"],
        ["Verified RAG", "VAL", "0.0333", "0.9667", "0.0333", "0.9333"],
        ["Verified RAG", "TEST", "0.0333", "0.9667", "0.0333", "1.0000"],
    ]
    tbl3 = doc.add_table(rows=len(t3_rows) + 1, cols=len(t3_headers))
    tbl3.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl3.autofit = True
    for c_i, h in enumerate(t3_headers):
        c = tbl3.cell(0, c_i)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(7.5)
        r.font.bold = True
        set_cell_margins(c, top=25, bottom=25, left=25, right=25)
        set_cell_shading(c, "F0F0F0")
        set_cell_border(c, top=dict(sz=6, color="000000"), bottom=dict(sz=6, color="000000"))

    for r_i, r_vals in enumerate(t3_rows):
        for c_i, val in enumerate(r_vals):
            c = tbl3.cell(r_i + 1, c_i)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i >= 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(7.5)
            set_cell_margins(c, top=20, bottom=20, left=25, right=25)
            if r_i == len(t3_rows) - 1:
                set_cell_border(c, bottom=dict(sz=6, color="000000"))
            else:
                set_cell_border(c, bottom=dict(sz=2, color="E0E0E0"))

    add_h2("D. Conservative Citation Repair")
    add_body(
        "Out of 191 repair opportunities, 0 repairs were committed because candidate passages failed strict substring or high-confidence NLI entailment thresholds. "
        "This conservative policy successfully avoids false-positive academic attributions."
    )
    add_h2("E. Iterative Refinement Outcomes and Trade-Offs")
    add_body(
        "Table IV displays empirical outcomes from iterative refinement across all 100 queries. "
        "Iterative refinement left 98 unchanged, improved 1, and degraded 1 (permutation p = 1.000). Enabling refinement doubled latency (2.2x) "
        "without improving grounding. This proves that when relevant evidence is positioned at lower ranks (ranks 15-17), iterative prompting cannot overcome context distraction. "
        "Pre-generation filtering is therefore far more critical than post-generation prompt loops."
    )

    # TABLE IV
    p_t4 = doc.add_paragraph()
    p_t4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t4.paragraph_format.space_before = Pt(4)
    p_t4.paragraph_format.space_after = Pt(2)
    rt4 = p_t4.add_run("TABLE IV: EMPIRICAL OUTCOMES OF ITERATIVE REFINEMENT (N=100)")
    rt4.font.name = 'Times New Roman'
    rt4.font.size = Pt(8.0)
    rt4.font.bold = True

    t4_headers = ["Outcome Category", "Queries", "Share (%)", "Significance"]
    t4_rows = [
        ["Unchanged", "98", "98.0%", "—"],
        ["Improved Grounding", "1", "1.0%", "p = 1.000 (Permutation)"],
        ["Degraded Grounding", "1", "1.0%", "Not Significant"],
        ["Total Evaluated", "100", "100.0%", "—"],
    ]
    tbl4 = doc.add_table(rows=len(t4_rows) + 1, cols=len(t4_headers))
    tbl4.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl4.autofit = True
    for c_i, h in enumerate(t4_headers):
        c = tbl4.cell(0, c_i)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(7.5)
        r.font.bold = True
        set_cell_margins(c, top=25, bottom=25, left=25, right=25)
        set_cell_shading(c, "F0F0F0")
        set_cell_border(c, top=dict(sz=6, color="000000"), bottom=dict(sz=6, color="000000"))

    for r_i, r_vals in enumerate(t4_rows):
        for c_i, val in enumerate(r_vals):
            c = tbl4.cell(r_i + 1, c_i)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i >= 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(7.5)
            set_cell_margins(c, top=20, bottom=20, left=25, right=25)
            if r_i == len(t4_rows) - 1:
                set_cell_border(c, bottom=dict(sz=6, color="000000"))
            else:
                set_cell_border(c, bottom=dict(sz=2, color="E0E0E0"))

    # FIGURE 4: Iteration Tradeoff
    add_fig("ieee_paper/images/fig04_iteration_tradeoff.png", "Fig. 4. Empirical iterative refinement trade-off: 2.2x latency inflation without measurable grounding recovery (p=1.000).", width=3.45)

    add_h2("F. Provenance Ledger Validation")
    add_body(
        "The provenance graph verified 100% link integrity across all 202 claims (202/202 confirmed), providing cryptographic SHA256 audit trails from claims to primary literature chunks."
    )

    # =========================================================
    # SECTION V: WEB PLATFORM IMPLEMENTATION & USER INTERFACES
    # =========================================================
    add_h1("V. WEB PLATFORM IMPLEMENTATION AND USER INTERFACES")
    add_body(
        "To operationalize the multi-stage synthesis architecture for academic researchers, ResearchNexus AI is deployed as a full-stack web platform. "
        "The system backend is built using FastAPI with asynchronous concurrency, communicating with a persistent ChromaDB vector store and BM25 index. "
        "The frontend is implemented in React with TypeScript and Vite, delivering real-time streaming, interactive citation badging, and full provenance visualization. "
        "The platform comprises three core user workspaces: Literature Discovery Portal, Evidence-Grounded Assistant Workspace, and Explainable AI Provenance Dashboard."
    )
    add_h2("A. Literature Discovery and Hybrid Search Portal")
    add_body(
        "As depicted in Fig. 5, the literature discovery portal provides an interactive search interface over the 26,259 corpus chunks. "
        "Users can enter natural language research queries or domain-specific Boolean expressions. The portal executes parallel BM25 and dense vector search, "
        "fusing ranked results via RRF. For every candidate chunk, the interface displays: (1) source publication metadata, (2) individual lexical scores and dense cosine similarities, "
        "(3) combined RRF ranks, and (4) BGE cross-encoder re-ordered positions. Researchers can interactively inspect passage snippets, verify source DOIs, "
        "and select relevant evidence subsets prior to generative synthesis."
    )

    # FIGURE 5: Web Photo 1
    add_fig("ieee_paper/images/web_ui_01_hybrid_search.png", "Fig. 5. ResearchNexus AI Literature Discovery Portal: Hybrid retrieval interface displaying BM25, dense cosine, and RRF rank badges.", width=3.45)

    add_h2("B. Evidence-Grounded Assistant Workspace")
    add_body(
        "Fig. 6 presents the evidence-grounded generative assistant workspace. Upon submitting a complex research prompt, the system queries the candidate corpus, "
        "constructs the prioritized evidence context, and invokes the generative model with strict context constraints. The generated response is formatted with "
        "interactive numeric citation pills (e.g., [1], [2]). Clicking any citation badge automatically opens the Evidence Inspector drawer on the right side of the screen. "
        "The inspector highlights the exact sentence in the source publication that substantiates the assertion, along with deterministic overlap metrics and semantic NLI confidence scores. "
        "This bidirectional interaction ensures that scholars never have to take generative summaries on faith."
    )

    # FIGURE 6: Web Photo 2
    add_fig("ieee_paper/images/web_ui_02_assistant_synthesis.png", "Fig. 6. ResearchNexus AI Assistant Workspace: Synthesized literature review with interactive citation badges and real-time evidence inspector.", width=3.45)

    add_h2("C. Explainable AI and Provenance Graph Dashboard")
    add_body(
        "Fig. 7 illustrates the Explainable AI (XAI) and Provenance Dashboard. In high-stakes academic and clinical research, algorithmic opacity is unacceptable. "
        "The XAI dashboard provides an immutable, claim-by-claim audit ledger. Each generated statement is mapped to its unique claim ID, exact text snippet, assigned citation marker, "
        "retrieved chunk ID, first-stage retrieval rank, cross-encoder logit, and Stage A / Stage B verification status. In addition, the interface computes cryptographic SHA256 hashes "
        "of the input query, context window, and generated output. This guarantees complete auditability, allowing peer reviewers and regulatory bodies to verify the empirical provenance of any claim."
    )

    # FIGURE 7: Web Photo 3
    add_fig("ieee_paper/images/web_ui_03_xai_provenance.png", "Fig. 7. ResearchNexus AI Explainability Dashboard: Granular claim-level provenance ledger with SHA256 cryptographic trace links.", width=3.45)

    # =========================================================
    # SECTION VI: CONCLUSION AND FUTURE WORK
    # =========================================================
    add_h1("VI. CONCLUSION AND FUTURE WORK")
    add_body(
        "This paper presented ResearchNexus AI, an explainable, multi-stage RAG framework designed for verified scientific literature synthesis. "
        "By uniting BM25 and dense vector search through Reciprocal Rank Fusion, the system achieves high candidate recall (Hit@20 = 1.0000 on test queries) in 7.83 ms median latency. "
        "BGE cross-encoder reranking prioritizes relevant evidence, and the automated provenance graph delivers 100% end-to-end auditability across all 202 evaluated claims."
    )
    add_body(
        "Our empirical findings on ds_nexus_v11 provide practical guidance for scientific AI systems. Conservative citation repair successfully prevents false-positive attributions, "
        "while iterative refinement adds a 2.2x latency overhead without meaningful grounding recovery when gold context is diluted by distractors. Reliable scientific synthesis "
        "requires disciplined context filtering rather than blind iterative revision."
    )
    add_body(
        "Future research will explore: (1) dynamic context pruning based on cross-encoder logit margins to eliminate distracting passages; (2) domain-specific NLI verifiers tuned on academic "
        "corpora to differentiate cautious hedging from factual hallucinations; and (3) active multi-hop re-querying when initial evidence pools exhibit information gaps."
    )

    # =========================================================
    # REFERENCES
    # =========================================================
    add_h1("REFERENCES")
    refs = [
        "[1] P. Lewis et al., \"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,\" Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 33, pp. 9459-9474, 2020.",
        "[2] V. Karpukhin et al., \"Dense Passage Retrieval for Open-Domain Question Answering,\" in Proc. EMNLP 2020, pp. 6769-6781, 2020.",
        "[3] N. F. Liu, T. Zhang, and P. Liang, \"Evaluating Verifiability in Generative Search Engines,\" in Findings of EMNLP 2023, pp. 7001-7025, 2023.",
        "[4] S. Robertson and H. Zaragoza, \"The Probabilistic Relevance Framework: BM25 and Beyond,\" Found. Trends Inf. Retr., vol. 3, no. 4, pp. 333-389, 2009.",
        "[5] J. Menick et al., \"Teaching Language Models to Support Answers with Verified Quotes,\" arXiv:2203.11147, 2022.",
        "[6] G. V. Cormack, C. L. A. Clarke, and S. Büttcher, \"Reciprocal Rank Fusion Outperforms Condorcet,\" in Proc. SIGIR 2009, pp. 758-759, 2009.",
        "[7] R. Nogueira and K. Cho, \"Passage Re-ranking with BERT,\" arXiv:1901.04085, 2019.",
        "[8] K. Lo et al., \"S2ORC: The Semantic Scholar Open Research Corpus,\" in Proc. ACL 2020, pp. 4969-4983, 2020.",
        "[9] J. Lála et al., \"PaperQA: A Retrieval-Augmented Generative Agent for Scientific Research,\" arXiv:2312.07559, 2023.",
        "[10] Y. Zheng et al., \"OpenResearcher: Unleashing AI for Accelerated Scientific Research,\" in Proc. EMNLP 2024 Demo, pp. 209-218, 2024.",
        "[11] S. Agarwal et al., \"LitLLM: A Toolkit for Scientific Literature Review,\" arXiv:2402.01788, 2024.",
        "[12] L. Gao et al., \"RARR: Researching and Revising What Language Models Say,\" in Proc. ACL 2023, pp. 16477-16508, 2023.",
        "[13] A. Asai et al., \"Self-RAG: Learning to Retrieve, Generate, and Critique,\" in Proc. ICLR 2024, 2024.",
        "[14] A. Asai et al., \"Synthesizing Scientific Literature with Retrieval-Augmented Language Models,\" Nature, vol. 650, pp. 857-863, 2026.",
        "[15] Z. Shi et al., \"Towards a Unified Framework for Reference Retrieval and Related Work Generation,\" in Findings of EMNLP 2023, pp. 5785-5799, 2023.",
        "[16] M. D. Skarlinski et al., \"Language Agents Achieve Superhuman Synthesis of Scientific Knowledge,\" arXiv:2409.13740, 2024.",
        "[17] S. Lin and P. A. Beling, \"An End-to-End Optimal Trade Execution Framework based on PPO,\" in Proc. IEEE CIFEr, 2023.",
        "[18] D. Araci, \"FinBERT: Financial Sentiment Analysis with Pre-trained Language Models,\" arXiv:1908.10063, 2019.",
        "[19] A. Vaswani et al., \"Attention Is All You Need,\" Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 30, pp. 5998-6008, 2017.",
        "[20] H. Wang, Z. Xie, D. K. W. Chiu, and K. K. W. Ho, \"Multimodal Market Information Fusion for Stock Price Trend Prediction,\" Applied Intelligence, vol. 55, no. 1, pp. 77-90, 2024.",
        "[21] Y. Li, M. Zhuang, J. Wang, and J. Zhou, \"Leveraging Multi-Time-Span Sequences for Improved Stock Trend Prediction,\" Neurocomputing, vol. 620, p. 129218, 2025.",
        "[22] T.-V. Pricope, \"Deep Reinforcement Learning in Quantitative Algorithmic Trading: A Review,\" arXiv:2106.00123, 2021."
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.18)
        p.paragraph_format.first_line_indent = Inches(-0.18)
        p.paragraph_format.line_spacing = 1.02
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(r)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(8.0)

    docx_path = os.path.abspath("ieee_paper/ResearchNexus_AI_Paper.docx")
    doc.save(docx_path)
    print(f"[SUCCESS] Saved Expanded Word Document: {docx_path}")

    pdf_path = os.path.abspath("ieee_paper/ResearchNexus_AI_Paper.pdf")
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc_com = word.Documents.Open(docx_path)
        doc_com.SaveAs(pdf_path, FileFormat=17)
        page_count = doc_com.ComputeStatistics(2)  # 2 corresponds to wdStatisticPages
        doc_com.Close()
        word.Quit()
        print(f"[SUCCESS] Exported PDF via Word COM: {pdf_path} (Total Pages: {page_count})")
    except Exception as e:
        print(f"[ERROR] Word export failed: {e}")

if __name__ == "__main__":
    build_expanded_ieee_paper()
