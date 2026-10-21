import os, sys, asyncio
sys.path.insert(0, os.path.abspath('backend'))
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'
os.environ['GEMINI_API_KEY'] = 'dummy'

from app.api.papers import execute_search_experiment, _EXPERIMENTS, SearchRequest
import uuid

async def main():
    sid = uuid.uuid4()
    req = SearchRequest(query="Stock Price Prediction Using Triple Barrier Labeling")
    from app.api.papers import _init_experiment
    _init_experiment(sid, req.query)
    
    await execute_search_experiment(sid, req)
    
    print(_EXPERIMENTS[sid])

if __name__ == '__main__':
    asyncio.run(main())
