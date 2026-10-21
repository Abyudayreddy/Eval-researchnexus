import re

with open('backend/app/api/ai.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_sources = '''            "source": p.get("domain", "Online Repository"),
            "evidence_status": p.get("evidence_status")'''

new_sources = '''            "source": p.get("domain", "Online Repository"),
            "evidence_status": p.get("evidence_status"),
            "retrieval_source": p.get("retrieval_source", "online"),
            "read_source": p.get("read_source", "online"),
            "pdf_path": p.get("pdf_path", "")'''

c = c.replace(old_sources, new_sources)

with open('backend/app/api/ai.py', 'w', encoding='utf-8') as f:
    f.write(c)
