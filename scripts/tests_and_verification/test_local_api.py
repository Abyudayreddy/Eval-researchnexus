import os, sys, asyncio
sys.path.insert(0, os.path.abspath('backend'))
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'
os.environ['GEMINI_API_KEY'] = 'dummy'

from app.api.papers import execute_search_experiment, _EXPERIMENTS, SearchRequest, connector_router
import uuid

async def mock_search(*args, **kwargs):
    await asyncio.sleep(0.1)
    return [], {'error':'mocked'}

connector_router.search = mock_search

async def main():
    sid = uuid.uuid4()
    req = SearchRequest(query="Stock Price Prediction Using Triple Barrier Labeling")
    from app.api.papers import _init_experiment
    _init_experiment(sid, req.query)
    
    await execute_search_experiment(sid, req)
    
    res = _EXPERIMENTS[sid]
    print("LEN LOCAL", len(res.get('local_results', [])))
    print("LOCAL RESULT TITLES", [p.get('title') for p in res.get('local_results', [])])
    print("STATUS", res.get('local_status'))
    print("TRACE CANDIDATES", res.get('combined_trace', {}).get('local_trace', {}).get('candidates'))

if __name__ == '__main__':
    asyncio.run(main())
