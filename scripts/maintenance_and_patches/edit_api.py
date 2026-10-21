import re

with open('src/utils/api.ts', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'ask: (query: string, searchMode: string = "hybrid", contextPapers?: any[]) => fetchWithAuth("/ai/ask", {',
    'ask: (query: string, searchMode: string = "hybrid", contextPapers?: any[], searchId?: string) => fetchWithAuth("/ai/ask", {\n      method: "POST",\n      body: JSON.stringify({ query, search_mode: searchMode, context_papers: contextPapers, search_id: searchId })\n    }),\n    explain_removed:'
)
content = content.replace(
    'body: JSON.stringify({ query, search_mode: searchMode, context_papers: contextPapers })\n    }),\n    explain_removed:',
    ''
)
with open('src/utils/api.ts', 'w', encoding='utf-8') as f:
    f.write(content)
