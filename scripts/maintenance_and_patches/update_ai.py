import re

with open("backend/app/api/ai.py", "r", encoding="utf-8") as f:
    content = f.read()

import_old = "from app.services.connectors import RepositoryRouter"
import_new = "from app.services.connectors import RepositoryRouter\nfrom app.api.papers import search_papers, SearchRequest as PapersSearchRequest"

content = content.replace(import_old, import_new)

search_old = """    # 1. Phase 3/4A Online Repository Retrieval or use passed context
    if request.context_papers:
        papers = [p.dict() for p in request.context_papers]
        trace = None
    else:
        papers, trace = await connector_router.search(query=search_query, search_mode=request.search_mode, limit_per_source=5)"""

search_new = """    # 1. Unified Local + Online Retrieval
    if request.context_papers:
        papers = [p.dict() for p in request.context_papers]
        trace = None
    else:
        search_req = PapersSearchRequest(query=search_query, search_mode=request.search_mode, limit_per_source=5)
        search_res = await search_papers(search_req)
        papers = search_res.get("papers", [])
        trace = search_res.get("trace", {})"""

content = content.replace(search_old, search_new)

with open("backend/app/api/ai.py", "w", encoding="utf-8") as f:
    f.write(content)
