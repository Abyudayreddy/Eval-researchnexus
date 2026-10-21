import re

with open('backend/app/services/local_evidence.py', 'r', encoding='utf-8') as f:
    c = f.read()

# I will replace the canonical.get('authors', []) line
old_line = "'authors': canonical.get('authors', []),"
new_line = "'authors': ', '.join([a.get('name', str(a)) if isinstance(a, dict) else str(a) for a in canonical.get('authors', [])]) if isinstance(canonical.get('authors'), list) else canonical.get('authors', ''),"

c = c.replace(old_line, new_line)

with open('backend/app/services/local_evidence.py', 'w', encoding='utf-8') as f:
    f.write(c)
