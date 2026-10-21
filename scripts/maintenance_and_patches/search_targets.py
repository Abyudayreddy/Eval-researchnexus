import fitz

doc = fitz.open('ieee_paper/ResearchNexus_AI_Paper.pdf')
print('=== Searching for key phrases in PDF ===')
targets = [
    'Standalone BM25 and ChromaDB fail',
    '0.0667',
    'Claim Support Rates of 0.0533',
    'refinement left 98 unchanged',
    '191 identified repair',
    '202 generated claims were successfully linked'
]

for t in targets:
    found = False
    for pno, p in enumerate(doc):
        r = p.search_for(t)
        if r:
            print(f'Found "{t[:35]}" on page {pno+1}: {len(r)} occurrences')
            found = True
    if not found:
        print(f'NOT FOUND: "{t[:35]}"')
