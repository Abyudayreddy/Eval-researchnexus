import asyncio
import urllib.request
import urllib.parse
import json
import os
from typing import List, Dict, Any
from .base import BaseConnector
import traceback

class CrossrefConnector(BaseConnector):
    """
    Connector for fetching academic papers from Crossref REST API.
    """
    
    BASE_URL = "https://api.crossref.org/works"

    async def get_domain_papers(self, domain_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        # Map domain to a generic search term for Crossref
        query = domain_id.replace('-', ' ')
        return await self.search(query, domain_id, limit)

    async def search(self, query: str, domain_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        search_query = query
        if domain_id and domain_id != 'interdisciplinary':
            search_query = f"{query} {domain_id.replace('-', ' ')}"
            
        return await asyncio.to_thread(self._fetch_from_crossref, search_query, limit)

    def _fetch_from_crossref(self, search_query: str, limit: int) -> List[Dict[str, Any]]:
        results = []
        try:
            encoded_query = urllib.parse.quote(search_query)
            # Select specific fields to reduce payload size
            url = f"{self.BASE_URL}?query={encoded_query}&select=DOI,title,author,abstract,created,URL&rows={limit}"
            
            headers = {'User-Agent': 'ResearchNexus/1.0 (mailto:admin@researchnexus.local)'}
            
            # Use CROSSREF_API_KEY if available (for Crossref Metadata Plus)
            api_key = os.getenv("CROSSREF_API_KEY")
            if api_key:
                headers['Crossref-Plus-API-Token'] = api_key
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                
            items = data.get('message', {}).get('items', [])
            
            for item in items:
                doi = item.get('DOI', '')
                
                title_list = item.get('title', [])
                title = title_list[0] if title_list else 'Unknown Title'
                
                authors_list = item.get('author', [])
                authors = []
                for author in authors_list:
                    name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                    if name:
                        authors.append(name)
                        
                authors_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "") if authors else "Authors unavailable"
                
                abstract = item.get('abstract', 'No abstract available.')
                # Clean up JATS abstract XML if present
                if abstract.startswith('<jats:'):
                    abstract = "Abstract available via publisher."
                    
                created = item.get('created', {})
                date_parts = created.get('date-parts', [[None]])[0]
                pub_date = f"{date_parts[0]}-{str(date_parts[1]).zfill(2)}" if len(date_parts) >= 2 and date_parts[0] else "Unknown Date"
                
                paper_url = item.get('URL', '')
                
                results.append(self._standardize_paper(
                    paper_id=doi,
                    title=title,
                    authors=authors_str,
                    abstract=abstract,
                    publication_date=pub_date,
                    source="Crossref",
                    url=paper_url
                ))
                
        except Exception as e:
            print(f"Crossref Connector Error: {e}")
            traceback.print_exc()
            
        return results
