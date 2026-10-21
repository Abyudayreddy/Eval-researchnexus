import re

with open('backend/app/services/connectors/router.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'print\(f"DEBUG:.*?"\)', 'pass', c)
c = re.sub(r'print\(f\'DEBUG:.*?\'\)', 'pass', c)

with open('backend/app/services/connectors/router.py', 'w', encoding='utf-8') as f:
    f.write(c)
