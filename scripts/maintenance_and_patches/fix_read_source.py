import re

with open('backend/app/services/local_evidence.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_rs = "'read_source': canonical.get('read_source', 'local_pdf' if canonical.get('pdf_path') else 'unavailable'),"
new_rs = "'read_source': 'online' if (canonical.get('paper_url') or canonical.get('url')) else ('local_pdf' if canonical.get('pdf_path') else 'unavailable'),"

c = c.replace(old_rs, new_rs)

with open('backend/app/services/local_evidence.py', 'w', encoding='utf-8') as f:
    f.write(c)
