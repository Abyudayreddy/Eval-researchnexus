import re

with open('backend/app/api/papers.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('def run_local_search(query):', 'def run_local_search(query, deep_evidence=False):')
c = c.replace('return local_retriever.retrieve(query)', 'return local_retriever.retrieve(query, deep_evidence=deep_evidence)')
c = c.replace('local_task = asyncio.to_thread(run_local_search, request.query)', 'local_task = asyncio.to_thread(run_local_search, request.query, getattr(request, "deep_evidence", False))')

# Update SearchRequest to accept deep_evidence
req_old = """class SearchRequest(BaseModel):
    query: str
    search_mode: Optional[str] = "hybrid"
    retrieval_mode: Optional[str] = "local_online" # Default is now local_online
    publication_year: Optional[str] = None
    sort_by: Optional[str] = "relevance\""""

req_new = """class SearchRequest(BaseModel):
    query: str
    search_mode: Optional[str] = "hybrid"
    retrieval_mode: Optional[str] = "local_online" # Default is now local_online
    publication_year: Optional[str] = None
    sort_by: Optional[str] = "relevance"
    deep_evidence: Optional[bool] = False"""

c = c.replace(req_old, req_new)

with open('backend/app/api/papers.py', 'w', encoding='utf-8') as f:
    f.write(c)

with open('backend/app/api/ai.py', 'r', encoding='utf-8') as f:
    a = f.read()

a = a.replace('PapersSearchRequest(query=search_query, search_mode=request.search_mode)', 'PapersSearchRequest(query=search_query, search_mode=request.search_mode, deep_evidence=True)')

with open('backend/app/api/ai.py', 'w', encoding='utf-8') as f:
    f.write(a)
