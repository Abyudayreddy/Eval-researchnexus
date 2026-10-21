import fitz

doc = fitz.open('ieee_paper/ResearchNexus_AI_Paper.pdf')

# Page 1
p1_terms = [
    'Recall@20',
    'Hit@20',
    'single-retriever',
    'Single-Retriever'
]
print('=== PAGE 1 SEARCH ===')
for t in p1_terms:
    print(t, '->', doc[0].search_for(t))

# Page 6
p6_terms = [
    'Recall@20',
    'Hit@20',
    '0.9500',
    '1.0000',
    'conclusion',
    'Conclusion'
]
print('=== PAGE 6 SEARCH ===')
for t in p6_terms:
    print(t, '->', doc[5].search_for(t))
