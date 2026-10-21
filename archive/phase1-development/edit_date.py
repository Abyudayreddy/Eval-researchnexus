import re

with open('src/pages/HybridSearchPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'result.publication_date?.substring(0, 7) || "Unknown Date"',
    '(result.publication_date || result.published)?.substring(0, 7) || "Unknown Date"'
)

content = content.replace(
    'selectedPaper.publication_date?.substring(0, 7) || "Unknown Date"',
    '(selectedPaper.publication_date || selectedPaper.published)?.substring(0, 7) || "Unknown Date"'
)

with open('src/pages/HybridSearchPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
