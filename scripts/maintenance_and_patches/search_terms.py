import fitz

doc = fitz.open('ieee_paper/ResearchNexus_AI_Paper.pdf')
lines_to_search = [
    'Recall@20',
    'Hit@20',
    '0.0667',
    '0.0759',
    '0.0000',
    'claim support rate',
    '0.0533',
    '0.0350',
    'unsupported-claim',
    '0.9467',
    '0.9650',
    'citation correctness',
    '1.0000',
    '191',
    '202',
    'permutation test',
    '1.000',
    '4.9 seconds',
    '11.065'
]

for pno, page in enumerate(doc):
    text = page.get_text()
    print(f'=== PAGE {pno+1} ===')
    for term in lines_to_search:
        count = text.count(term)
        if count > 0:
            print(f'  Found "{term}": {count} times')
