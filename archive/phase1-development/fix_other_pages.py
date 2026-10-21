import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'normalizeSearchId' not in content:
        content = content.replace("import { api } from '../utils/api';", "import { api } from '../utils/api';\nimport { normalizeSearchId } from '../utils/apiAdapter';")
        content = content.replace("import { apiAdapter", "import { normalizeSearchId, apiAdapter")
        
        # for HybridSearchPage
        if 'HybridSearchPage' in filepath:
            content = content.replace("const querySearchId = searchParams.get('search_id');", "const querySearchId = normalizeSearchId(searchParams.get('search_id'));")
        # for AssistantPage
        if 'AssistantPage' in filepath:
            content = content.replace("const searchId = location.state?.search_id || searchParams.get('search_id') || undefined;", "const searchId = normalizeSearchId(location.state?.search_id || searchParams.get('search_id')) || undefined;")
        # for LiteratureReviewPage
        if 'LiteratureReviewPage' in filepath:
            content = content.replace("const searchId = location.state?.search_id;", "const searchId = normalizeSearchId(location.state?.search_id);")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('src/pages/HybridSearchPage.tsx')
update_file('src/pages/AssistantPage.tsx')
update_file('src/pages/LiteratureReviewPage.tsx')
