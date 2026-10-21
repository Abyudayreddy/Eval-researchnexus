import re

def insert_import(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If it's missing in AssistantPage
    if 'import { normalizeSearchId }' not in content:
        content = content.replace("import { useSearchParams, useLocation } from 'react-router-dom';", "import { useSearchParams, useLocation } from 'react-router-dom';\nimport { normalizeSearchId } from '../utils/apiAdapter';")

    # For files where it is declared but never read, we'll remove it, or use it!
    # Wait, in HybridSearchPage I changed: const querySearchId = normalizeSearchId(...)
    # Let's verify HybridSearchPage uses it.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

insert_import('src/pages/AssistantPage.tsx')

def fix_unused(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # If there's an unused normalizeSearchId, just let it be but suppress error or fix usage
    if 'HybridSearchPage' in filepath:
        # Check if normalizeSearchId is actually used
        if 'normalizeSearchId(' not in content.replace('import { normalizeSearchId }', ''):
            content = content.replace("import { normalizeSearchId } from '../utils/apiAdapter';\n", "")
            content = content.replace("import { normalizeSearchId, apiAdapter", "import { apiAdapter")
    
    if 'LiteratureReviewPage' in filepath:
        if 'normalizeSearchId(' not in content.replace('import { normalizeSearchId }', ''):
            content = content.replace("import { normalizeSearchId } from '../utils/apiAdapter';\n", "")
            content = content.replace("import { normalizeSearchId, apiAdapter", "import { apiAdapter")

    if 'XaiPage' in filepath:
        content = content.replace("ChevronRight, ", "").replace(", ChevronRight", "")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_unused('src/pages/HybridSearchPage.tsx')
fix_unused('src/pages/LiteratureReviewPage.tsx')
fix_unused('src/pages/XaiPage.tsx')

