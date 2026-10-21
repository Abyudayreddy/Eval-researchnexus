import re

with open('src/pages/AssistantPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "const response = await api.ai.ask(finalQuery, 'hybrid', contextPapers);",
    "const searchId = location.state?.search_id || searchParams.get('search_id') || undefined;\n      const response = await api.ai.ask(finalQuery, 'hybrid', contextPapers, searchId);"
)

with open('src/pages/AssistantPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
