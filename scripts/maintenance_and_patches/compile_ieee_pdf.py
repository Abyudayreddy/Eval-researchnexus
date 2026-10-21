import os, sys
import reportlab.pdfgen.canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, Image as RLImage
)
import pypdf

OUTPUT_DIR = 'evaluation/publication_audit_v2/final_manuscript'
PDF_PATH = os.path.join(OUTPUT_DIR, 'ResearchNexusAI_IEEE_Final_Max6Pages.pdf')

class NumberedCanvas(reportlab.pdfgen.canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 8)
        page_text = f"{self._pageNumber}"
        self.drawRightString(8.5 * 72 - 36, 25, page_text)
        self.drawString(36, 8.5 * 72 + 2 * 72 - 30, "IEEE CONFERENCE PROCEEDINGS - SUBMISSION DRAFT")
        self.restoreState()

def build_pdf():
    # Page setup: Letter (8.5 x 11 inches)
    MARGIN_LEFT = 36
    MARGIN_BOTTOM = 36
    COL_WIDTH = 260
    COL_HEIGHT = 716
    GUTTER = 20

    frame1 = Frame(MARGIN_LEFT, MARGIN_BOTTOM, COL_WIDTH, COL_HEIGHT, id='col1', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    frame2 = Frame(MARGIN_LEFT + COL_WIDTH + GUTTER, MARGIN_BOTTOM, COL_WIDTH, COL_HEIGHT, id='col2', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)

    doc = BaseDocTemplate(PDF_PATH, pagesize=letter, leftMargin=MARGIN_LEFT, rightMargin=MARGIN_LEFT, topMargin=36, bottomMargin=36)
    template = PageTemplate(id='two_col', frames=[frame1, frame2])
    doc.addPageTemplates([template])

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'IEEETitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=17,
        leading=20,
        alignment=1,
        spaceAfter=10
    )

    author_style = ParagraphStyle(
        'IEEEAuthor',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=12,
        alignment=1,
        spaceAfter=12
    )

    abstract_text = ParagraphStyle(
        'IEEEAbstractText',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11,
        alignment=4,
        spaceAfter=8
    )

    keywords_style = ParagraphStyle(
        'IEEEKeywords',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'IEEEH1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        alignment=1,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'IEEEH2',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        leading=11.5,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'IEEEBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        alignment=4,
        spaceAfter=4,
        firstLineIndent=10
    )

    body_no_indent = ParagraphStyle(
        'IEEEBodyNoIndent',
        parent=body_style,
        firstLineIndent=0
    )

    caption_style = ParagraphStyle(
        'IEEECaption',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7.5,
        leading=9.5,
        alignment=1,
        spaceBefore=4,
        spaceAfter=5
    )

    table_cell = ParagraphStyle(
        'IEEETableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7,
        leading=8.5,
        alignment=1
    )

    table_cell_left = ParagraphStyle(
        'IEEETableCellLeft',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7,
        leading=8.5,
        alignment=0
    )

    ref_style = ParagraphStyle(
        'IEEERef',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7.5,
        leading=9.5,
        alignment=4,
        leftIndent=14,
        firstLineIndent=-14,
        spaceAfter=3
    )

    story = []

    # Title & Author
    story.append(Paragraph("ResearchNexusAI: An Explainable Multi-Stage RAG Framework for Scientific Literature Synthesis", title_style))
    story.append(Paragraph("Anonymous Authors<br/><i>Department of Computer Science and Engineering, Academic Institution</i><br/>{author1, author2}@institution.edu", author_style))

    # Abstract
    story.append(Paragraph("<b><i>Abstract</i></b>—Automated scientific literature synthesis demands stringent factual precision, robust evidence grounding, and traceable provenance. Standard retrieval-augmented generation (RAG) pipelines often suffer from semantic drift, hallucinated claims, and ambiguous bracketed citations. We present ResearchNexusAI, a modular, multi-stage RAG framework designed for scientific synthesis. The architecture integrates hybrid first-stage retrieval combining lexical BM25 and dense BGE-Base embeddings via Reciprocal Rank Fusion ($k=60$), cross-encoder neural reranking, post-generation Natural Language Inference (NLI) claim verification, ambiguity-sensitive citation repair, and traceable provenance tracking. We evaluate the framework against the controlled <i>ds_nexus_v11</i> scientific benchmark ($N=100$, with 15 held-out test queries comprising 10 answerable and 5 unanswerable items). On answerable test queries, hybrid retrieval achieves 10/10 Recall@20 (Hit@20 = 0.6667 across all 15 test items). Neural cross-encoder reranking produces a modest improvement in early-rank precision, increasing paper-level Mean Reciprocal Rank (MRR) from 0.0431 to 0.0480. In post-generation verification, automated NLI achieves 100% precision across evaluated positive factual assertions (4/4 naive, 3/3 verified), and the system correctly refuses 100% (5/5) of unanswerable queries. However, controlled experiments reveal critical negative findings: citation repair achieved 0 applied repairs (0.0% gain) because candidate matches exhibited pervasive multi-chunk ambiguity, while iterative refinement introduced a 106.3% stage latency increase without factual recovery (1 improved, 98 unchanged, 1 degraded query). Because external double-blind human annotations were not collected, human-judged claim validity remains unmeasured. Our findings demonstrate that multi-stage RAG provides transparent provenance and cautious abstention, but automated repair and iterative regeneration offer diminishing returns without richer, disambiguated passage semantics.", abstract_text))

    story.append(Paragraph("<b><i>Index Terms</i></b>—Retrieval-Augmented Generation, Scientific Literature Synthesis, Natural Language Inference, Citation Verification, Explainable AI.", keywords_style))

    # I. INTRODUCTION
    story.append(Paragraph("I. INTRODUCTION", h1_style))
    story.append(Paragraph("Scientific discovery relies heavily on synthesizing prior literature to identify experimental constraints, chemical formulations, and empirical trade-offs [1]. As publication velocity accelerates, human researchers face significant overhead navigating massive corpora to reconcile conflicting reports and extract exact numerical constants. Large language models (LLMs) offer promising synthesis capabilities but frequently generate fluent yet factually baseless claims, hallucinatory paper citations, and corrupted numeric metrics [2].", body_style))
    story.append(Paragraph("While standard Retrieval-Augmented Generation (RAG) conditions language synthesis on external text passages, single-stage bi-encoder dense retrievers struggle to distinguish precise alphanumeric terminology—such as stoichiometric ratios or chemical formulas—from semantically adjacent distractors [3], [4]. Furthermore, naive RAG models heuristic citations directly from LLM generation without verifying whether cited chunks mathematically entail the statements.", body_style))
    story.append(Paragraph("Recent benchmarks such as OpenScholar [1] explore scientific literature synthesis but rely predominantly on single-pass prompting without post-generation NLI audits. To investigate these challenges, we evaluate ResearchNexusAI, a multi-stage framework separating evidence exploration from grounded answer generation.", body_style))
    story.append(Paragraph("Rather than reporting unverified improvements, this work presents a forensically audited evaluation on the <i>ds_nexus_v11</i> benchmark ($N=100$). Our contributions are:", body_style))
    story.append(Paragraph("1) We implement an end-to-end multi-stage architecture integrating lexical BM25, dense BGE-Base embeddings, reciprocal rank fusion ($k=60$), neural cross-encoder reranking, and fine-grained chunk-level provenance tracing.", body_no_indent))
    story.append(Paragraph("2) We evaluate claim grounding using a decoupled epistemic taxonomy separating factual assertions from epistemic abstentions, demonstrating 100% refusal accuracy on unanswerable queries.", body_no_indent))
    story.append(Paragraph("3) We rigorously document empirical negative findings: neural reranking yields modest MRR gains (0.0431 to 0.0480), citation repair is blocked by multi-chunk candidate ambiguity (0 applied repairs), and iterative refinement roughly doubles generation latency without factual recovery.", body_no_indent))

    # II. RELATED WORK
    story.append(Paragraph("II. RELATED WORK", h1_style))
    story.append(Paragraph("<i>A. Scientific Literature Synthesis</i>", h2_style))
    story.append(Paragraph("Retrieval-augmented models condition generation on non-parametric document indices [2]. In scientific domains, general-domain bi-encoders trained on web text often suffer vocabulary mismatch on domain-specific acronyms. OpenScholar [1] established open-source retrieval augmentation over scientific papers, demonstrating that retrieval improves factual coverage over closed-book models. However, OpenScholar operates as a single-pass system without external claim-level NLI verification.", body_style))

    story.append(Paragraph("<i>B. Hybrid Retrieval and Cross-Encoders</i>", h2_style))
    story.append(Paragraph("Sparse lexical search via Okapi BM25 [3] ensures exact token matching, which is vital for alphanumeric entity identification. Dense embeddings such as BGE-Base [5] capture conceptual semantic similarity. Reciprocal Rank Fusion (RRF) [4] effectively merges rank distributions across disparate retrieval spaces without requiring score calibration. Subsequent neural cross-encoders [6] model deep query-document cross-attention to promote relevant candidates into early rank positions.", body_style))

    story.append(Paragraph("<i>C. Verification and Citation Repair</i>", h2_style))
    story.append(Paragraph("Natural Language Inference (NLI) frameworks evaluate premise-hypothesis entailment [7]. In synthesis pipelines, decomposing text into atomic propositions enables granular factuality checking. Automated citation repair attempts to align uncited statements with retrieved evidence; however, enforcing strict ambiguity thresholds is necessary to prevent spurious provenance attribution.", body_style))

    # III. SYSTEM ARCHITECTURE
    story.append(Paragraph("III. SYSTEM ARCHITECTURE AND METHODOLOGY", h1_style))
    story.append(Paragraph("The ResearchNexusAI architecture separates inquiry into candidate evidence exploration (<i>Research Explorer</i>) and evidence-bounded synthesis (<i>Ask AI</i>), as illustrated in Fig. 1.", body_style))

    # Embedded High-Resolution Architecture Graphic
    img_path = 'evaluation/publication_audit_v2/final_manuscript/fig01_researchnexus_architecture.png'
    arch_img = RLImage(img_path, width=258, height=158.4)
    story.append(Spacer(1, 3))
    story.append(arch_img)
    story.append(Paragraph("Fig. 1. Pipeline architecture showing multi-stage retrieval, bounded synthesis, NLI claim verification, and provenance logging.", caption_style))

    story.append(Paragraph("<i>A. Multi-Stage Evidence Retrieval</i>", h2_style))
    story.append(Paragraph("For query $q$, the retrieval pipeline executes sparse BM25 and dense BGE-Base searches over segmented passage collection C. Cosine similarity scores dense candidates, merged with BM25 rankings via Reciprocal Rank Fusion:", body_style))
    story.append(Paragraph("<font size=7.5>RRF(c) = [60 + r_BM25(c)]^(-1) + [60 + r_dense(c)]^(-1)</font>", ParagraphStyle('Eq', parent=styles['Normal'], alignment=1, spaceAfter=4)))
    story.append(Paragraph("The top-40 fused candidates are scored by the BAAI/bge-reranker-base cross-encoder over concatenated pairs [q; c] to yield final context pool K truncated at k=20.", body_style))

    story.append(Paragraph("<i>B. Epistemic Decoupling and Bounded Synthesis</i>", h2_style))
    story.append(Paragraph("Retrieved passages are injected into generation prompts with bracketed markers. To evaluate scientific outputs accurately, we adopt an explicit epistemic taxonomy:", body_style))
    story.append(Paragraph("• <b>Factual Assertions</b>: Positive propositions asserting scientific findings, mechanisms, or numerical performance metrics.", body_no_indent))
    story.append(Paragraph("• <b>Epistemic Abstentions</b>: Statements explicitly declining to answer when queried concepts are absent from context.", body_no_indent))
    story.append(Paragraph("• <b>Negative Evidence Findings</b>: Statements documenting that context does not contain the queried metric.", body_no_indent))
    story.append(Paragraph("Decoupling factual claims from abstentions prevents penalizing cautious models that correctly decline unanswerable queries.", body_style))

    story.append(Paragraph("<i>C. Verification, Repair, and Provenance</i>", h2_style))
    story.append(Paragraph("Generated text is parsed into atomic claims. Each factual assertion is paired with referenced context passages and evaluated using multi-premise NLI. Uncited statements are evaluated by CitationRepair, which enforces a strict ambiguity filter: if a statement matches multiple chunks equally well, repair is aborted to prevent spurious attribution. An explainability ledger records deterministic chunk-to-claim provenance.", body_style))

    # IV. EXPERIMENTAL RESULTS
    story.append(Paragraph("IV. EXPERIMENTAL RESULTS AND DISCUSSION", h1_style))
    story.append(Paragraph("<i>A. Benchmark & Evaluation Protocol</i>", h2_style))
    story.append(Paragraph("Evaluation is conducted on ds_nexus_v11 (N=100: DEV=70, VAL=15, TEST=15). The held-out TEST split consists of 10 answerable queries (`item_v11_086`–`095`, including 5 multi-paper synthesis and 5 adversarial queries) and 5 unanswerable queries (`item_v11_096`–`100`) containing zero relevant corpus papers. All metrics are derived from the canonical V4 reconciliation package.", body_style))

    story.append(Paragraph("<i>B. Retrieval Performance Comparison</i>", h2_style))
    story.append(Paragraph("Table I reports comparative retrieval metrics across baselines and neural reranking on the 15 held-out test queries.", body_style))

    # Table I: Retrieval
    t1_data = [
        [Paragraph("<b>Configuration</b>", table_cell_left), Paragraph("<b>Hit@5</b>", table_cell), Paragraph("<b>Hit@10</b>", table_cell), Paragraph("<b>Hit@20</b>", table_cell), Paragraph("<b>Rec@20*</b>", table_cell), Paragraph("<b>MRR_all</b>", table_cell), Paragraph("<b>MRR_ans</b>", table_cell)],
        [Paragraph("B1: BM25 Lexical", table_cell_left), Paragraph("0.0000", table_cell), Paragraph("0.6667", table_cell), Paragraph("0.6667", table_cell), Paragraph("<b>1.0000</b>", table_cell), Paragraph("0.0759", table_cell), Paragraph("0.1139", table_cell)],
        [Paragraph("B2: Dense Chroma", table_cell_left), Paragraph("0.0000", table_cell), Paragraph("0.0000", table_cell), Paragraph("0.0000", table_cell), Paragraph("0.0000", table_cell), Paragraph("0.0000", table_cell), Paragraph("0.0000", table_cell)],
        [Paragraph("B3: Hybrid RRF ($k=60$)", table_cell_left), Paragraph("0.0000", table_cell), Paragraph("0.0000", table_cell), Paragraph("0.6667", table_cell), Paragraph("<b>1.0000</b>", table_cell), Paragraph("0.0431", table_cell), Paragraph("0.0647", table_cell)],
        [Paragraph("B4: BGE Reranked", table_cell_left), Paragraph("0.0000", table_cell), Paragraph("0.0000", table_cell), Paragraph("0.6667", table_cell), Paragraph("<b>1.0000</b>", table_cell), Paragraph("0.0480", table_cell), Paragraph("0.0720", table_cell)],
    ]
    t1 = Table(t1_data, colWidths=[65, 30, 32, 32, 36, 32, 33])
    t1.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Paragraph("TABLE I. RETRIEVAL PERFORMANCE ON TEST SPLIT ($N=15$). *Recall@20 evaluated on the 10 answerable queries. MRR_all ($n=15$), MRR_ans ($n=10$).", caption_style))

    story.append(Paragraph("In BM25 retrieval, all 10 answerable test items place relevant papers at ranks 8 or 9 (reciprocal ranks 1/8=0.125 or 1/9=0.1111). Hit@5 is strictly 0.0, while Hit@10 and Hit@20 reach 10/15 (0.6667), achieving 10/10 (1.0000) Recall@20 on answerable items. Dense Chroma retrieval on this specific test set achieved zero hits in top-20.", body_style))
    story.append(Paragraph("Hybrid RRF successfully retains all 10 answerable candidates in the top-20 pool. Cross-encoder reranking yields a modest rank promotion, increasing MRR from 0.0431 to 0.0480 across all 15 items (and 0.0647 to 0.0720 across answerable items). Earlier preliminary reports claiming MRR=0.5444 (+47.7% gain) were ungrounded script artifacts and are formally superseded.", body_style))

    story.append(Paragraph("<i>C. Claim Grounding and Abstention Behavior</i>", h2_style))
    story.append(Paragraph("Table II details claim-level factuality and query-level abstention across 56 extracted sentences from naive and verified responses.", body_style))

    # Table II: Grounding
    t2_data = [
        [Paragraph("<b>Metric / Category</b>", table_cell_left), Paragraph("<b>Naive RAG</b>", table_cell), Paragraph("<b>Verified RAG</b>", table_cell)],
        [Paragraph("Total Extracted Candidate Sentences", table_cell_left), Paragraph("28", table_cell), Paragraph("28", table_cell)],
        [Paragraph("-- Appropriate Abstentions", table_cell_left), Paragraph("15", table_cell), Paragraph("15", table_cell)],
        [Paragraph("-- Insufficient Evidence Findings", table_cell_left), Paragraph("9", table_cell), Paragraph("10", table_cell)],
        [Paragraph("-- Factual Assertions Asserted", table_cell_left), Paragraph("4", table_cell), Paragraph("3", table_cell)],
        [Paragraph("Supported Factual Claims (Automated NLI)", table_cell_left), Paragraph("4 / 4", table_cell), Paragraph("3 / 3", table_cell)],
        [Paragraph("Unsupported Factual Claims", table_cell_left), Paragraph("0", table_cell), Paragraph("0", table_cell)],
        [Paragraph("Automated Factual Precision", table_cell_left), Paragraph("<b>1.0000</b>", table_cell), Paragraph("<b>1.0000</b>", table_cell)],
        [Paragraph("Unanswerable Query Abstention Rate", table_cell_left), Paragraph("<b>5 / 5 (100%)</b>", table_cell), Paragraph("<b>5 / 5 (100%)</b>", table_cell)],
        [Paragraph("Human Ground-Truth Agreement", table_cell_left), Paragraph("<i>Not Measured</i>", table_cell), Paragraph("<i>Not Measured</i>", table_cell)]
    ]
    t2 = Table(t2_data, colWidths=[130, 65, 65])
    t2.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t2)
    story.append(Paragraph("TABLE II. CLAIM GROUNDING AND EPISTEMIC ABSTENTION ON TEST SPLIT.", caption_style))

    story.append(Paragraph("Of 56 evaluated sentences, 49 represent epistemic abstentions or evidence-bounded negative findings. Factual assertions represent a small fraction (4 in naive, 3 in verified). Automated NLI scores all evaluated factual assertions as fully supported (100% precision). On all 5 unanswerable queries, both systems correctly declined to answer (100% abstention). However, because external double-blind human annotations were not collected, these automated scores cannot be generalized as proof of human-verified grounding.", body_style))

    story.append(Paragraph("<i>D. Citation Repair and Refinement Evaluation</i>", h2_style))
    story.append(Paragraph("Table III documents the empirical performance of citation repair and iterative synthesis refinement.", body_style))

    # Table III: Repair & Refinement
    t3_data = [
        [Paragraph("<b>Evaluation Dimension</b>", table_cell_left), Paragraph("<b>Observed Metric</b>", table_cell), Paragraph("<b>Scientific Finding</b>", table_cell_left)],
        [Paragraph("Eligible Factual Claims", table_cell_left), Paragraph("5", table_cell), Paragraph("Target for citation validation", table_cell_left)],
        [Paragraph("Baseline Valid Citation Rate", table_cell_left), Paragraph("1 / 5 (20.0%)", table_cell), Paragraph("Low initial citation density", table_cell_left)],
        [Paragraph("Candidate Repairs Attempted", table_cell_left), Paragraph("4", table_cell), Paragraph("Detected in item_v11_092", table_cell_left)],
        [Paragraph("Repairs Rejected (Ambiguity)", table_cell_left), Paragraph("4 / 4 (100%)", table_cell), Paragraph("Matched 10 chunks equally", table_cell_left)],
        [Paragraph("Safely Applied Repairs", table_cell_left), Paragraph("0", table_cell), Paragraph("<b>Repair Effect: Not Demonstrated</b>", table_cell_left)],
        [Paragraph("Post-Repair Citation Coverage", table_cell_left), Paragraph("1 / 5 (20.0%)", table_cell), Paragraph("<b>Coverage Gain: Not Observed</b>", table_cell_left)],
        [Paragraph("Successful-Repair Safety", table_cell_left), Paragraph("0 / 0", table_cell), Paragraph("<b>Safety: Not Estimable</b>", table_cell_left)],
        [Paragraph("Refinement Improved Queries", table_cell_left), Paragraph("1 / 100 (1.0%)", table_cell), Paragraph("Negligible factual recovery", table_cell_left)],
        [Paragraph("Refinement Unchanged Queries", table_cell_left), Paragraph("98 / 100 (98%)", table_cell), Paragraph("Identical verification state", table_cell_left)],
        [Paragraph("Refinement Degraded Queries", table_cell_left), Paragraph("1 / 100 (1.0%)", table_cell), Paragraph("Minor wording regression", table_cell_left)],
        [Paragraph("Refinement Net Gain (p=1.000)", table_cell_left), Paragraph("0.0%", table_cell), Paragraph("<b>No Significant Gain</b>", table_cell_left)],
    ]
    t3 = Table(t3_data, colWidths=[85, 55, 120])
    t3.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('PADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t3)
    story.append(Paragraph("TABLE III. CITATION REPAIR AND ITERATIVE REFINEMENT EVALUATION.", caption_style))

    story.append(Paragraph("In query `item_v11_092`, 4 uncited factual statements were flagged. While the repair engine located candidate matches in context, each statement matched 10 chunks simultaneously. To avoid false provenance, all 4 were rejected. Coverage remained 20.0%, and repair safety is mathematically not estimable.", body_style))
    story.append(Paragraph("On the 100-query refinement ablation (E07/E07.1), regeneration yielded 1 improved, 98 unchanged, and 1 degraded query ($p=1.000$, permutation test).", body_style))

    story.append(Paragraph("<i>E. Latency and Provenance Accounting</i>", h2_style))
    story.append(Paragraph("Table IV presents disaggregated stage latencies against complete request execution times.", body_style))

    # Table IV: Latency
    t4_data = [
        [Paragraph("<b>Measurement Scope</b>", table_cell_left), Paragraph("<b>Operation</b>", table_cell_left), Paragraph("<b>p50 (ms)</b>", table_cell), Paragraph("<b>p95 (ms)</b>", table_cell), Paragraph("<b>Mean (ms)</b>", table_cell)],
        [Paragraph("Component: Lexical", table_cell_left), Paragraph("BM25 Search", table_cell_left), Paragraph("0.69", table_cell), Paragraph("2.47", table_cell), Paragraph("0.98", table_cell)],
        [Paragraph("Component: Dense", table_cell_left), Paragraph("Chroma ANN", table_cell_left), Paragraph("13.51", table_cell), Paragraph("78.78", table_cell), Paragraph("16.84", table_cell)],
        [Paragraph("Component: Fusion", table_cell_left), Paragraph("Hybrid RRF ($k=60$)", table_cell_left), Paragraph("6.56", table_cell), Paragraph("19.12", table_cell), Paragraph("8.24", table_cell)],
        [Paragraph("Component: Neural Rerank", table_cell_left), Paragraph("BGE Cross-Encoder", table_cell_left), Paragraph("531.41", table_cell), Paragraph("4,246.05", table_cell), Paragraph("780.12", table_cell)],
        [Paragraph("Stage: Combined Retrieval", table_cell_left), Paragraph("Hybrid + BGE Rerank", table_cell_left), Paragraph("535.06", table_cell), Paragraph("4,251.51", table_cell), Paragraph("788.36", table_cell)],
        [Paragraph("Stage: Initial Synthesis", table_cell_left), Paragraph("LLM Generation", table_cell_left), Paragraph("1,420.00", table_cell), Paragraph("2,150.00", table_cell), Paragraph("1,650.00", table_cell)],
        [Paragraph("Stage: Refinement Pass", table_cell_left), Paragraph("Secondary LLM Pass", table_cell_left), Paragraph("2,930.00", table_cell), Paragraph("4,120.00", table_cell), Paragraph("3,210.00", table_cell)],
        [Paragraph("Complete Request (No Iter)", table_cell_left), Paragraph("Full Pipeline", table_cell_left), Paragraph("4,899.07", table_cell), Paragraph("8,514.65", table_cell), Paragraph("5,691.35", table_cell)],
        [Paragraph("Complete Request (With Iter)", table_cell_left), Paragraph("Full Pipeline", table_cell_left), Paragraph("11,064.67", table_cell), Paragraph("18,509.97", table_cell), Paragraph("12,655.70", table_cell)],
    ]
    t4 = Table(t4_data, colWidths=[70, 75, 36, 40, 39])
    t4.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
        ('PADDING', (0,0), (-1,-1), 2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t4)
    story.append(Paragraph("TABLE IV. DISAGGREGATED LATENCY PROFILES ACROSS PIPELINE BOUNDARIES.", caption_style))

    story.append(Paragraph("First-stage retrieval executes in under 15 ms. Cross-encoder reranking introduces a measurable latency cost (p50 = 531.41 ms), comprising the bulk of retrieval time. Secondary iterative refinement increases generation stage latency by 106.3% (1,420 ms to 2,930 ms) and complete request mean latency by 122.4% (5.69 s to 12.66 s).", body_style))
    story.append(Paragraph("In provenance audits across 202 claims in historical E08 records, automated claim-to-evidence and citation-to-evidence tracking achieved 100% completeness, establishing deterministic chunk traceability.", body_style))

    # V. LIMITATIONS
    story.append(Paragraph("V. LIMITATIONS AND THREATS TO VALIDITY", h1_style))
    story.append(Paragraph("Our empirical evaluation is subject to several key limitations:", body_style))
    story.append(Paragraph("1) <i>Small Test Sample Size</i>: The held-out test split contains 15 queries (10 answerable, 5 unanswerable). While sufficient for detailed qualitative inspection, larger test splits are required for high statistical power.", body_no_indent))
    story.append(Paragraph("2) <i>Sparse Factual Claims</i>: Only 7 positive factual assertions were generated across the 15 test responses, as cautious prompting led the generator to produce predominantly epistemic abstentions.", body_no_indent))
    story.append(Paragraph("3) <i>Absence of Human Annotations</i>: Human ground-truth validation is formally blocked and not measured. Automated NLI models cannot detect subtle domain-specific factual contradictions.", body_no_indent))
    story.append(Paragraph("4) <i>Model Version Divergence</i>: Historical E04 evaluated `gemini-2.5-flash`, while authoritative E04.1 evaluated `gemini-3.5-flash-lite`, and the production backend targets `gemini-2.5-flash`. While greedy decoding ($T=0.0$) was held constant, model outputs across different versions cannot be pooled directly.", body_no_indent))
    story.append(Paragraph("5) <i>Conservative Citation Repair</i>: The ambiguity filter rejects multi-chunk matches, preventing repair when literature exhibits high semantic redundancy.", body_no_indent))
    story.append(Paragraph("6) <i>Refinement Inefficiency</i>: Iterative regeneration roughly doubled complete request latency without recovering factual grounding.", body_no_indent))

    # VI. CONCLUSION
    story.append(Paragraph("VI. CONCLUSION", h1_style))
    story.append(Paragraph("This paper presented an audited evaluation of ResearchNexusAI for scientific literature synthesis. On the <i>ds_nexus_v11</i> benchmark, hybrid lexical-dense retrieval achieved 10/10 recall on answerable queries, and neural reranking provided modest rank promotions (MRR 0.0431 to 0.0480). Decoupled epistemic evaluation demonstrated 100% abstention accuracy on unanswerable queries and 100% automated NLI precision on evaluated factual claims.", body_style))
    story.append(Paragraph("Crucially, our evaluation exposed key negative results: citation repair failed to improve coverage due to multi-chunk ambiguity, and iterative refinement introduced substantial latency overhead without factual recovery. Future research should prioritize double-blind expert human annotation, disambiguation heuristics for citation repair, and selective rather than unconditional refinement triggering.", body_style))

    # REFERENCES
    story.append(Paragraph("REFERENCES", h1_style))
    story.append(Paragraph("[1] A. Asai <i>et al.</i>, ``OpenScholar: Synthesizing scientific literature with retrieval-augmented language models,'' <i>arXiv preprint arXiv:2411.14199</i>, 2024.", ref_style))
    story.append(Paragraph("[2] P. Lewis <i>et al.</i>, ``Retrieval-augmented generation for knowledge-intensive NLP tasks,'' in <i>Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)</i>, vol. 33, 2020, pp. 9459--9474.", ref_style))
    story.append(Paragraph("[3] S. E. Robertson and H. Zaragoza, ``The probabilistic relevance framework: BM25 and beyond,'' <i>Found. Trends Inf. Retr.</i>, vol. 3, no. 4, pp. 333--389, 2009.", ref_style))
    story.append(Paragraph("[4] G. V. Cormack, C. L. Clarke, and S. Buettcher, ``Reciprocal rank fusion outperforms condorcet and individual rank learning methods,'' in <i>Proc. 32nd Int. ACM SIGIR Conf. Res. Dev. Inf. Retr.</i>, 2009, pp. 758--759.", ref_style))
    story.append(Paragraph("[5] S. Xiao <i>et al.</i>, ``C-Pack: Packaged resources to advance general Chinese embedding,'' <i>BAAI Technical Report, arXiv:2309.07597</i>, 2023.", ref_style))
    story.append(Paragraph("[6] N. Reimers and I. Gurevych, ``Sentence-BERT: Sentence embeddings using Siamese BERT-networks,'' in <i>Proc. Conf. Empirical Methods Nat. Lang. Process. (EMNLP)</i>, 2019, pp. 3982--3992.", ref_style))
    story.append(Paragraph("[7] A. Williams, N. Nangia, and S. R. Bowman, ``A broad-coverage challenge corpus for sentence understanding through inference,'' in <i>Proc. Conf. N. Am. Chapter Assoc. Comput. Linguistics: Hum. Lang. Technol. (NAACL-HLT)</i>, 2018, pp. 1112--1122.", ref_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Built PDF at {PDF_PATH}")

    # Inspect page count
    reader = pypdf.PdfReader(PDF_PATH)
    page_count = len(reader.pages)
    print(f"Total compiled PDF page count: {page_count} pages.")
    assert page_count <= 6, f"Page limit exceeded: {page_count} > 6"
    print("PAGE LIMIT STRICTLY ENFORCED AND SATISFIED (<= 6 PAGES).")

if __name__ == '__main__':
    build_pdf()
