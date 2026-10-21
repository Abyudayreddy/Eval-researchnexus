import re

with open('src/utils/api.ts', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'explain_removed:\s*method: "POST",\s*body: JSON.stringify.*?\}\),\s*', '', content, flags=re.DOTALL)

with open('src/utils/api.ts', 'w', encoding='utf-8') as f:
    f.write(content)
