import asyncio
import json
from app.api.ai import ask_ai, AskRequest

async def test_ai():
    print("Testing 'AI applications in cancer detection'...")
    req = AskRequest(query='AI applications in cancer detection', search_mode='hybrid')
    res = await ask_ai(req)
    
    print("Generation Status:", res.get('generation_status'))
    
    explainability = res.get('explainability', {})
    sources = explainability.get('sources', [])
    print(f"Total AI Sources Selected: {len(sources)}")
    
    local_count = sum(1 for s in sources if s.get('retrieval_source') == 'local' or s.get('retrieval_source') == 'mixed')
    online_count = sum(1 for s in sources if s.get('retrieval_source') == 'online' or s.get('retrieval_source') == 'mixed')
    
    print(f"Local contributing: {local_count}")
    print(f"Online contributing: {online_count}")
    
    # Print the answer summary
    answer = res.get('answer', '')
    print(f"Answer snippet: {answer[:100]}...")

if __name__ == "__main__":
    asyncio.run(test_ai())
