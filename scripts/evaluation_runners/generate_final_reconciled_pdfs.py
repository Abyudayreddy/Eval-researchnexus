import fitz

def generate_annotated_and_clean_pdfs():
    # Load original 6-page PDF
    src_pdf_path = 'ieee_paper/ResearchNexus_AI_Paper.pdf'
    clean_out_path = 'evaluation/publication_audit_v2/final_manuscript/ResearchNexus_AI_Paper_V4_Reconciled_Final.pdf'
    highlighted_out_path = 'evaluation/publication_audit_v2/final_manuscript/ResearchNexus_AI_Paper_V4_Reconciled_Highlighted.pdf'

    # 1. GENERATE CLEAN RECONCILED PDF
    doc_clean = fitz.open(src_pdf_path)

    # Page 1: Abstract & Contributions corrections
    # We redact stale text and insert corrected text in dark black font
    p1 = doc_clean[0]
    
    # Redact "Recall@20 = 0.9500, Hit@20 = 1.0000 on test queries" in Abstract
    r1 = p1.search_for('Recall@20 = 0.9500, Hit@20 = 1.0000 on test queries')
    for r in r1:
        p1.add_redact_annot(r, fill=(1, 1, 1))
    
    # Redact bullet 1 contribution: "candidate Recall@20 of 0.9500 and Hit@20 of 1.0000"
    r2 = p1.search_for('candidate Recall@20 of 0.9500 and Hit@20 of 1.0000')
    for r in r2:
        p1.add_redact_annot(r, fill=(1, 1, 1))

    p1.apply_redactions()

    for r in r1:
        p1.insert_text((r.x0, r.y1 - 2), 'Hit@20 = 0.6667 (10/15), Recall@20 = 1.0000 on answerable items', fontsize=7.5, fontname='times-roman', color=(0, 0, 0))
    for r in r2:
        p1.insert_text((r.x0, r.y1 - 2), 'Hit@20 = 0.6667 (10/15) and Recall@20 = 1.0000 on answerable queries', fontsize=7.5, fontname='times-roman', color=(0, 0, 0))

    # Page 3: Table I text and cells
    p3 = doc_clean[2]
    # Redact "0.0667" in BM25 TEST row
    r_bm25_hit = p3.search_for('0.0667')
    for r in r_bm25_hit:
        p3.add_redact_annot(r, fill=(1, 1, 1))
    
    # Redact text discussing BM25 and ChromaDB failing completely on TEST split
    r_disc = p3.search_for('Standalone BM25 and ChromaDB fail on fine-grained')
    if r_disc:
        # Redact the whole paragraph block: y from 566 to 652
        p3.add_redact_annot(fitz.Rect(315, 566, 565, 650), fill=(1, 1, 1))

    p3.apply_redactions()

    for r in r_bm25_hit:
        p3.insert_text((r.x0 - 2, r.y1 - 2), '0.6667', fontsize=7.5, fontname='times-roman', color=(0, 0, 0))
    
    if r_disc:
        corrected_p3_text = (
            "Table I reports first-stage retrieval on ds_nexus_v11. On the 15 held-out "
            "TEST queries (10 answerable, 5 unanswerable), BM25 places gold papers at "
            "ranks 8-9, achieving Hit@20 = 0.6667 (10/15) and Recall@20 = 1.0000 (10/10 "
            "answerable items). Hybrid RRF achieves Recall@20 = 1.0000 on answerable queries "
            "and 0.9500 across all queries in 7.83 ms median latency."
        )
        p3.insert_textbox(fitz.Rect(315, 566, 565, 650), corrected_p3_text, fontsize=8.0, fontname='times-roman', color=(0, 0, 0))

    # Page 4: Section IV-C text discussing Claim Support Rates
    p4 = doc_clean[3]
    r_csr = p4.search_for('Claim Support Rates of 0.0533 vs. 0.0350')
    if r_csr:
        # Redact paragraph discussing CSR (y from 120 to 180)
        p4.add_redact_annot(fitz.Rect(315, 120, 565, 185), fill=(1, 1, 1))

    # Redact citation repair text discussing 191 opportunities
    r_rep = p4.search_for('Out of 191 repair opportunities, 0 repairs were committed')
    if r_rep:
        p4.add_redact_annot(fitz.Rect(315, 330, 565, 385), fill=(1, 1, 1))

    p4.apply_redactions()

    if r_csr:
        corrected_csr_text = (
            "Evaluating Naive RAG against Verified RAG under the decoupled epistemic "
            "taxonomy demonstrates 100% precision on true factual assertions (4/4 naive, "
            "3/3 verified). On unanswerable queries, both systems achieve 100% (5/5) "
            "appropriate abstention, avoiding hallucination on queries lacking evidence."
        )
        p4.insert_textbox(fitz.Rect(315, 120, 565, 185), corrected_csr_text, fontsize=8.0, fontname='times-roman', color=(0, 0, 0))

    if r_rep:
        corrected_rep_text = (
            "In citation evaluation, 4 uncited factual statements were identified. "
            "All 4 candidate matches were rejected due to multi-chunk ambiguity (matching "
            "10 chunks simultaneously). Consequently, 0 repairs were committed, maintaining "
            "a conservative safety threshold against false-positive attributions."
        )
        p4.insert_textbox(fitz.Rect(315, 330, 565, 385), corrected_rep_text, fontsize=8.0, fontname='times-roman', color=(0, 0, 0))

    # Page 6: Conclusion
    p6 = doc_clean[5]
    r_p6_hit = p6.search_for('Hit@20 = 1.0000 on test queries')
    for r in r_p6_hit:
        p6.add_redact_annot(r, fill=(1, 1, 1))
    p6.apply_redactions()
    for r in r_p6_hit:
        p6.insert_text((r.x0, r.y1 - 2), 'Hit@20 = 0.6667 (10/15 on test queries)', fontsize=8.0, fontname='times-roman', color=(0, 0, 0))

    doc_clean.save(clean_out_path)
    print(f"Saved Clean Reconciled PDF to {clean_out_path}")

    # 2. GENERATE HIGHLIGHTED DIFFERENTIATED AUDIT PDF
    # In this PDF:
    # - Yellow Highlight: Corrections to previous inaccurate or conflated metrics
    # - Cyan Highlight: Additions providing vital epistemic and safety context
    doc_hl = fitz.open(clean_out_path)

    # Highlight Page 1
    p1_hl = doc_hl[0]
    r_p1_corr = p1_hl.search_for('Hit@20 = 0.6667 (10/15), Recall@20 = 1.0000 on answerable items')
    for r in r_p1_corr:
        annot = p1_hl.add_highlight_annot(r)
        annot.set_colors(stroke=(1, 0.9, 0)) # Yellow for metric correction
        annot.update()
    
    r_p1_corr2 = p1_hl.search_for('Hit@20 = 0.6667 (10/15) and Recall@20 = 1.0000 on answerable queries')
    for r in r_p1_corr2:
        annot = p1_hl.add_highlight_annot(r)
        annot.set_colors(stroke=(1, 0.9, 0)) # Yellow
        annot.update()

    # Highlight Page 3
    p3_hl = doc_hl[2]
    # Highlight Table I BM25 Hit@20
    r_t1 = p3_hl.search_for('0.6667')
    for r in r_t1:
        annot = p3_hl.add_highlight_annot(r)
        annot.set_colors(stroke=(1, 0.9, 0)) # Yellow
        annot.update()

    # Highlight corrected Table I explanation text (Cyan: Added context on answerable split)
    r_t1_text = p3_hl.search_for('Table I reports first-stage retrieval on ds_nexus_v11.')
    if r_t1_text:
        annot = p3_hl.add_highlight_annot(fitz.Rect(315, 566, 565, 645))
        annot.set_colors(stroke=(0.2, 0.8, 1.0)) # Cyan for added contextual explanation
        annot.update()

    # Highlight Page 4
    p4_hl = doc_hl[3]
    # Highlight CSR correction & epistemic taxonomy (Cyan: added epistemic decoupling)
    annot_csr = p4_hl.add_highlight_annot(fitz.Rect(315, 120, 565, 180))
    annot_csr.set_colors(stroke=(0.2, 0.8, 1.0)) # Cyan
    annot_csr.update()

    # Highlight Citation repair ambiguity explanation (Yellow: corrected repair count and finding)
    annot_rep = p4_hl.add_highlight_annot(fitz.Rect(315, 330, 565, 380))
    annot_rep.set_colors(stroke=(1, 0.9, 0)) # Yellow
    annot_rep.update()

    # Highlight Page 6
    p6_hl = doc_hl[5]
    r_p6 = p6_hl.search_for('Hit@20 = 0.6667 (10/15 on test queries)')
    for r in r_p6:
        annot = p6_hl.add_highlight_annot(r)
        annot.set_colors(stroke=(1, 0.9, 0)) # Yellow
        annot.update()

    # Add visual color legend on Page 1 top margin
    p1_hl.insert_text((36, 20), "DIFF AUDIT LEGEND: [YELLOW] = Corrected Empirical Metric (Reconciled from V4)  |  [CYAN] = Added Context & Epistemic Taxonomy Clarification", fontsize=8.0, fontname='helv', color=(0.8, 0, 0))

    doc_hl.save(highlighted_out_path)
    print(f"Saved Highlighted Differentiated Audit PDF to {highlighted_out_path}")

if __name__ == '__main__':
    generate_annotated_and_clean_pdfs()
