import fitz

doc = fitz.open('ieee_paper/ResearchNexus_AI_Paper.pdf')
with open('extracted_p3_p4.txt', 'w', encoding='utf-8') as f:
    f.write('=== PAGE 3 ===\n')
    f.write(doc[2].get_text())
    f.write('\n\n=== PAGE 4 ===\n')
    f.write(doc[3].get_text())

print('Successfully extracted page 3 and 4 text to extracted_p3_p4.txt')
