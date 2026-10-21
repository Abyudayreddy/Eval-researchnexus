import re

def fix_imports(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ensure import { normalizeSearchId } from '../utils/apiAdapter';
    if 'import { normalizeSearchId }' not in content and 'import { normalizeSearchId,' not in content:
        if "import { apiAdapter" in content:
            content = content.replace("import { apiAdapter", "import { normalizeSearchId, apiAdapter")
        elif "import { api }" in content:
            content = content.replace("import { api } from '../utils/api';", "import { api } from '../utils/api';\nimport { normalizeSearchId } from '../utils/apiAdapter';")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_imports('src/pages/AssistantPage.tsx')
fix_imports('src/pages/HybridSearchPage.tsx')
fix_imports('src/pages/LiteratureReviewPage.tsx')
fix_imports('src/pages/XaiPage.tsx')
