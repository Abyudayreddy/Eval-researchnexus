import asyncio
import urllib.request
import urllib.parse
import json
import os
from typing import List, Dict, Any
from .base import BaseConnector
import traceback

class OpenAlexConnector(BaseConnector):
    """
    Connector for fetching academic papers from OpenAlex.
    """
    
    BASE_URL = "https://api.openalex.org/works"

    async def get_domain_papers(self, domain_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        # Map domain to a generic search term for OpenAlex
        domain_query_map = {
            'artificial-intelligence': 'artificial intelligence OR machine learning',
            'healthcare': 'medicine OR healthcare OR clinical',
            'data-science': 'data science OR data analytics',
            'environmental-science': 'environmental science OR climate change',
            'materials-science': 'materials science OR nanomaterials',
            'interdisciplinary': 'interdisciplinary research',
            'energy': 'renewable energy OR battery technology',
            'space-science': 'astrophysics OR space science'
        }
        query = domain_query_map.get(domain_id, domain_id.replace('-', ' '))
        return await self.search(query, domain_id, limit)

    async def search(self, query: str, domain_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        # Optionally scope by domain, but OpenAlex search is full-text.
        search_query = query
        if domain_id and domain_id != 'interdisciplinary':
            search_query = f"{query} {domain_id.replace('-', ' ')}"
            
        return await asyncio.to_thread(self._fetch_from_openalex, search_query, limit)

    def _fetch_from_openalex(self, search_query: str, limit: int) -> List[Dict[str, Any]]:
        results = []
        try:
            encoded_query = urllib.parse.quote(search_query)
            url = f"{self.BASE_URL}?search={encoded_query}&per-page={limit}&mailto=admin@researchnexus.local"
            
            # Use OPENALEX_API_KEY if available in environment and not empty
            api_key = os.getenv("OPENALEX_API_KEY", "").strip()
            if api_key and len(api_key) > 5:
                url += f"&api_key={api_key}"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'ResearchNexus/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                
            for item in data.get('results', []):
                paper_id = item.get('id', '').split('/')[-1]
                title = item.get('title')
                if not title:
                    continue
                    
                # Extract authors
                authors = []
                for authorship in item.get('authorships', []):
                    author = authorship.get('author', {})
                    if author.get('display_name'):
                        authors.append(author.get('display_name'))
                        
                authors_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "") if authors else "Authors unavailable"
                
                # Abstract (OpenAlex returns abstract_inverted_index)
                abstract = ""
                inv_index = item.get('abstract_inverted_index')
                if inv_index:
                    # Reconstruct abstract
                    word_pos = []
                    for word, positions in inv_index.items():
                        for pos in positions:
                            word_pos.append((pos, word))
                    word_pos.sort()
                    abstract = " ".join([w[1] for w in word_pos])
                else:
                    abstract = "No abstract available."
                    
                pub_date = item.get('publication_date', 'Unknown Date')
                
                # DOI as URL if available, else id
                paper_url = item.get('doi') or item.get('id', '')
                
                results.append(self._standardize_paper(
                    paper_id=paper_id,
                    title=title,
                    authors=authors_str,
                    abstract=abstract,
                    publication_date=pub_date,
                    source="OpenAlex",
                    url=paper_url
                ))
                
        except Exception as e:
            print(f"OpenAlex Connector Error: {e}")
            traceback.print_exc()
            
        return results
