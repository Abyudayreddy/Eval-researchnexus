import asyncio
import os
import sys

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.services.connectors.router import RepositoryRouter

async def test_search():
    router = RepositoryRouter()
    query = "electric vehicle battery safety"
    print(f"Testing query: {query}")
    results = await router.search(query=query, search_mode="hybrid", limit_per_source=5)
    print(f"Total passing results: {len(results)}")
    if results:
        for r in results:
            print(f"- {r.get('title')} ({r.get('source')})")

if __name__ == "__main__":
    asyncio.run(test_search())
