import re

with open('backend/app/api/ai.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_loop = """    for p in papers:
        abstract = p.get('abstract', '')
        # Check if abstract is meaningfully present (e.g. > 20 chars)
        if abstract and isinstance(abstract, str) and len(abstract.strip()) > 20:
            p['evidence_status'] = 'evidence_ready'
            evidence_ready_papers.append(p)
        else:
            p['evidence_status'] = 'metadata_only'
        enriched_papers.append(p)"""

new_loop = """    for p in papers:
        evidence_text = p.get('evidence_text', '')
        abstract = p.get('abstract', '')
        primary_text = evidence_text if (evidence_text and len(evidence_text.strip()) > 20) else abstract
        
        # Check if text is meaningfully present
        if primary_text and isinstance(primary_text, str) and len(primary_text.strip()) > 20:
            p['evidence_status'] = 'evidence_ready'
            p['resolved_evidence_text'] = primary_text
            evidence_ready_papers.append(p)
        else:
            p['evidence_status'] = 'metadata_only'
            p['resolved_evidence_text'] = ''
        enriched_papers.append(p)"""

c = c.replace(old_loop, new_loop)

old_context = """        abstract = p.get('abstract', '')
        
        # Trim abstract cleanly at whitespace if necessary
        if len(abstract) > MAX_ABSTRACT_CHARS:
            trimmed = abstract[:MAX_ABSTRACT_CHARS]
            last_space = trimmed.rfind(' ')
            if last_space > 0:
                abstract = trimmed[:last_space] + "..."
            else:
                abstract = trimmed + "..."
                
        structured_paper = (
            f"[{idx+1}]\\n"
            f"Title: {title}\\n"
            f"Authors: {authors}\\n"
            f"Source: {source_name}\\n"
            f"Publication Date: {pub_date}\\n"
            f"Abstract: {abstract}\\n\\n"
        )"""

new_context = """        primary_text = p.get('resolved_evidence_text', '')
        
        # Trim text cleanly at whitespace if necessary
        if len(primary_text) > MAX_ABSTRACT_CHARS:
            trimmed = primary_text[:MAX_ABSTRACT_CHARS]
            last_space = trimmed.rfind(' ')
            if last_space > 0:
                primary_text = trimmed[:last_space] + "..."
            else:
                primary_text = trimmed + "..."
                
        structured_paper = (
            f"[{idx+1}]\\n"
            f"Title: {title}\\n"
            f"Authors: {authors}\\n"
            f"Source: {source_name}\\n"
            f"Publication Date: {pub_date}\\n"
            f"Evidence: {primary_text}\\n\\n"
        )"""

c = c.replace(old_context, new_context)

with open('backend/app/api/ai.py', 'w', encoding='utf-8') as f:
    f.write(c)
