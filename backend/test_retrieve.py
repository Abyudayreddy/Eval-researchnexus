import asyncio
from app.api.papers import search_papers, SearchRequest
async def test():
    req = SearchRequest(query='machine learning', search_mode='hybrid')
    res = await search_papers(req)
    print(res.get('online_status'))
    print(res.get('local_status'))
    print(res.get('combined_result_count'))
asyncio.run(test())
