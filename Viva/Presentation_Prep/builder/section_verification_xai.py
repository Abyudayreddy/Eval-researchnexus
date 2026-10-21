"""
Section builders: Document-Only Mode, Dynamic Ingestion, Claim Verification Engine,
Citation Integrity & Repair, and Explainable AI (XAI) Provenance Ledger.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helpers import (
    add_header_styled, add_body_p, add_bullet_p,
    add_callout, add_code_block, add_table_styled
)

def build_verification_and_xai(doc):
    # SECTION 10: UPLOADED PAPER / DOCUMENT-ONLY MODE
    add_header_styled(doc, "10. Uploaded Paper / Document-Only Mode: Zero-Leakage Architecture", level=1)
    add_body_p(
        doc,
        "A critical feature in ResearchNexus AI is the Document-Only Analysis Mode. When a researcher uploads an unpublished "
        "manuscript or a confidential preprint (PDF), they need answers strictly derived from that single paper."
    )
    add_body_p(
        doc,
        "The Engineering Danger: In many naive RAG systems, if an uploaded document is short or doesn't mention a specific background concept, "
        "the retrieval engine silently falls back to the global knowledge base or the LLM's parametric memory. This can lead to disastrous "
        "confidentiality breaches or cross-contamination where findings from external papers are attributed to the uploaded draft."
    )
    add_callout(
        doc,
        "HOW WE GUARANTEE ZERO LEAKAGE IN CODE",
        "In `backend/app/services/document_service.py` and `enhanced_rag.py`:\n"
        "1. When a PDF is uploaded, PyMuPDF parses the text streams into chunks and stores them into an ephemeral or user-scoped ChromaDB collection (e.g. `doc_user_session_xyz`).\n"
        "2. The RAG controller checks the active mode flag: `doc_only_mode = True`.\n"
        "3. All retrieval queries are strictly targeted to the document collection ID.\n"
        "4. If the retrieved chunks have zero relevance to the user's question, the system outputs: 'The uploaded document does not provide evidence to answer this question' "
        "rather than falling back to the 687-paper global library.",
        bg_hex="FDEDEC",
        border_hex="E74C3C"
    )

    # SECTION 11: DYNAMIC RESEARCH PAPER INGESTION PIPELINE
    add_header_styled(doc, "11. Dynamic Research Paper Ingestion Pipeline", level=1)
    add_body_p(
        doc,
        "When a user drops a PDF into the ResearchNexus interface, it undergoes an asynchronous multi-stage ingestion state machine:"
    )

    ingest_flow = (
        "1. UPLOAD RECEIVED  -> Validates PDF headers, checks mime-type, saves to secure temp storage.\n"
        "2. PARSING (fitz)   -> PyMuPDF extracts continuous text blocks, stripping headers/footers/page numbers.\n"
        "3. CHUNKING         -> LlamaIndex sentence splitter creates ~500-token chunks with 50-token overlaps.\n"
        "4. EMBEDDING        -> BAAI/bge-base-en-v1.5 generates 768-dim vectors in batches on GPU/CPU.\n"
        "5. INDEXING         -> Vectors and chunk metadata (page, section, hash) are committed to ChromaDB.\n"
        "6. BM25 UPDATING    -> Inverted token index is refreshed for the document session.\n"
        "7. READY STATE      -> Status changes to READY; instant exploration and Q&A unlocked in UI."
    )
    add_code_block(doc, ingest_flow, caption="Asynchronous Ingestion Pipeline Stages")

    # SECTION 12: TWO-STAGE CLAIM VERIFICATION (PROVE ENGINE)
    add_header_styled(doc, "12. Two-Stage Claim Verification: The PROVE Engine", level=1)
    add_body_p(
        doc,
        "The intellectual crown jewel of ResearchNexus AI is our Claim Verification Engine (`backend/app/services/assistant/claim_verifier.py`). "
        "Instead of treating the generated synthesis as an unmodifiable block of prose, our system deconstructs it into atomic declarative claims "
        "and subjects each claim to an evidentiary tribunal."
    )

    add_body_p(
        doc,
        "Stage A: Fast Deterministic Token Overlap\n"
        "We first evaluate the direct lexical overlap between the extracted claim C and the cited evidence chunk E. "
        "We compute the symmetric token intersection ratio over non-stopword stems:\n"
        "Overlap(C, E) = |Tokens(C) ∩ Tokens(E)| / |Tokens(C)|\n"
        "If Overlap >= 0.80, the claim is a direct verbatim quote or highly strict paraphrase. It is instantaneously verified in under 5ms, "
        "saving expensive LLM inference cycles."
    )
    add_body_p(
        doc,
        "Stage B: Natural Language Inference (NLI) Verification\n"
        "When Overlap < 0.80, the claim requires conceptual semantic evaluation. We feed the evidence chunk as the Premise and the claim as "
        "the Hypothesis into an NLI reasoning prompt. The verifier assigns one of four mutually exclusive scientific labels:"
    )

    headers_nli = ["Verification Label", "Evidentiary Meaning", "System Action & Visual Badge"]
    rows_nli = [
        [
            "SUPPORTED",
            "The retrieved evidence chunk directly entails the factual statement made in the claim.",
            "Green Checkmark Badge [Verified]. Full provenance link preserved in UI."
        ],
        [
            "PARTIALLY SUPPORTED",
            "The evidence provides partial context or qualitative confirmation, but lacks specific quantitative details.",
            "Amber Warning Badge [Partial]. System warns user to check specific parameters."
        ],
        [
            "UNSUPPORTED",
            "The evidence chunk does not mention or imply the asserted claim (extrapolative hallucination).",
            "Red Flag Badge [Unverified]. Synthesis flags claim as unsubstantiated."
        ],
        [
            "CONTRADICTED",
            "The evidence explicitly states the opposite of what the synthesis asserted.",
            "Purple Warning Badge [Contradicted]. System alerts researcher to experimental discrepancy."
        ]
    ]
    add_table_styled(doc, headers_nli, rows_nli, [Inches(1.8), Inches(2.7), Inches(2.3)])

    # SECTION 13: CITATION INTEGRITY & CONSERVATIVE REPAIR
    add_header_styled(doc, "13. Citation Integrity System & Conservative Repair (E06 & E06.1 Insights)", level=1)
    add_body_p(
        doc,
        "In naive AI writing tools, when a citation is broken or incorrect, the tool might randomly pick any paper in the database that has "
        "matching keywords and re-assign the footnote. In research, this is academic fraud."
    )
    add_body_p(
        doc,
        "In ResearchNexus AI, our Citation Integrity System (`backend/app/services/assistant/citation_repair.py`) operates under strict conservative rules:\n"
        "1. Exact Retrieval Context Isolation: When a claim's cited chunk fails verification, repair is ONLY attempted within the exact "
        "frozen pool of retrieved chunks associated with that query.\n"
        "2. High Entailment Threshold: A candidate replacement chunk must independently achieve a strict SUPPORTED label for that specific claim.\n"
        "3. Conservative Abstention: If no retrieved chunk strictly supports the claim, the system DOES NOT invent a fake citation. It strips "
        "the invalid citation tag and marks the claim as unverified."
    )

    add_callout(
        doc,
        "EVALUATION EXPERIMENT E06 & E06.1 REALITY",
        "During our formal benchmark evaluation across 100 queries (191 potential repair opportunities):\n"
        "Our system attempted repair strictly against the retrieved evidence pool. Exactly 0 unsupported claims were arbitrarily re-linked to distractor chunks. "
        "This demonstrated our system's scientific honesty: we prefer abstention over fabricated attribution!",
        bg_hex="FEF9E7",
        border_hex="F39C12"
    )

    # SECTION 14: EXPLAINABLE AI (XAI) & PROVENANCE LEDGER
    add_header_styled(doc, "14. Explainable AI (XAI) & The Provenance Ledger", level=1)
    add_body_p(
        doc,
        "Explainability in ResearchNexus AI is not just a post-hoc paragraph summary; it is built into the data structure of every response. "
        "Every claim in the synthesis is serialized into an authoritative provenance ledger containing:\n"
        "• `claim_id`: Unique identifier (e.g. `claim_q14_c02`)\n"
        "• `claim_text`: Exact atomic sentence text\n"
        "• `evidence_chunk_id`: The exact chunk in ChromaDB (e.g. `chunk_24819`)\n"
        "• `paper_title` & `doi`: Bibliographic metadata\n"
        "• `retrieval_ranks`: BM25 rank, Dense rank, and RRF rank\n"
        "• `rerank_score`: Neural cross-encoder logit score\n"
        "• `evidence_sha256`: Cryptographic hash of the exact evidence text slice\n"
        "• `verification_status`: SUPPORTED, PARTIALLY_SUPPORTED, etc."
    )
    add_body_p(
        doc,
        "In our frozen evaluation (`ds_nexus_v11`), ResearchNexus AI achieved a 100% verified trace link rate (202/202 claims) "
        "with valid chunk provenance and SHA-256 integrity hashes."
    )

    return doc
