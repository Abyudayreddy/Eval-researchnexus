import asyncio, os, sys
sys.path.insert(0, os.path.abspath('backend'))
from app.services.connectors import ArxivConnector, PmcConnector, OpenAlexConnector, NasaAdsConnector, CrossrefConnector, RepositoryRouter

async def test():
    print('--- Testing arXiv ---')
    arxiv = ArxivConnector()
    print(await arxiv.search('artificial intelligence', limit=1))

    print('\n--- Testing PMC ---')
    pmc = PmcConnector()
    print(await pmc.search('healthcare clinical', limit=1))

    print('\n--- Testing OpenAlex ---')
    oa = OpenAlexConnector()
    print(await oa.search('materials science', limit=1))

    print('\n--- Testing Crossref ---')
    cr = CrossrefConnector()
    print(await cr.search('energy storage', limit=1))

    print('\n--- Testing NASA ADS (no token) ---')
    nasa = NasaAdsConnector()
    print(await nasa.search('space', limit=1))

    print('\n--- Testing Router Deduplication & Parallel ---')
    router = RepositoryRouter()
    res = await router.search('AI', domain_id='artificial-intelligence', limit_per_source=2)
    print(f'Router unified {len(res)} results.')
    for r in res:
        print(f"- [{r.get('source')}] {r.get('title')}")

if __name__ == "__main__":
    asyncio.run(test())
