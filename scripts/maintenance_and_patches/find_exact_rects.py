import fitz

doc = fitz.open('ieee_paper/ResearchNexus_AI_Paper.pdf')
targets = [
    # Page 1
    (0, 'Recall@20 of 0.9500 and Hit@20 of 1.0000'),
    # Page 3
    (2, 'Table I displays retrieval metrics on ds_nexus_v11.'),
    (2, 'Standalone BM25 and ChromaDB fail on fine-grained'),
    (2, '0.0667'),
    # Page 4
    (3, 'Claim Support Rates of 0.0533 vs. 0.0350'),
    (3, 'Out of 191 repair opportunities, 0 repairs were committed'),
    (3, 'Iterative refinement left 98 unchanged'),
    # Page 5
    (4, 'The provenance graph verified 100% link integrity across all 202 claims'),
    # Page 6
    (5, 'Recall@20 of 0.9500 and a Hit@20 of 1.0000')
]

for pno, phrase in targets:
    r = doc[pno].search_for(phrase)
    print(f'P{pno+1}: "{phrase[:40]}" -> found {len(r)} rects: {r}')
