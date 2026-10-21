import re

with open('src/pages/LiteratureReviewPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace contentEditable with contentEditable suppressContentEditableWarning
content = content.replace(
    'contentEditable data-placeholder="Review Title..."',
    'contentEditable suppressContentEditableWarning data-placeholder="Review Title..."'
)

with open('src/pages/LiteratureReviewPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
