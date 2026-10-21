import asyncio
import urllib.request
import urllib.parse
import json
import os
from typing import List, Dict, Any
from .base import BaseConnector
import traceback

class NasaAdsConnector(BaseConnector):
    """
    Connector for fetching astrophysics/space science papers from NASA ADS API.
    """
    
    BASE_URL = "https://api.adsabs.harvard.edu/v1/search/query"

    async def get_domain_papers(self, domain_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        # ADS is heavily space/physics focused
        query = "astrophysics OR astronomy OR space"
        return await self.search(query, domain_id, limit)

    async def search(self, query: str, domain_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._fetch_from_ads, query, limit)

    def _fetch_from_ads(self, search_query: str, limit: int) -> List[Dict[str, Any]]:
        results = []
        token = os.getenv("NASA_ADS_TOKEN")
        
        if not token:
            print("NASA ADS Connector: NASA_ADS_TOKEN environment variable not set. Skipping.")
            return []
            
        try:
            encoded_query = urllib.parse.quote(search_query)
            # Fetch essential fields
            url = f"{self.BASE_URL}?q={encoded_query}&fl=id,title,author,abstract,pubdate,bibcode&rows={limit}"
            
            req = urllib.request.Request(url, headers={
                'Authorization': f'Bearer {token}',
                'User-Agent': 'ResearchNexus/1.0'
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                
            docs = data.get('response', {}).get('docs', [])
            
            for doc in docs:
                paper_id = doc.get('id', '')
                
                title_list = doc.get('title', [])
                title = title_list[0] if title_list else 'Unknown Title'
                
                authors_list = doc.get('author', [])
                authors_str = ", ".join(authors_list[:3]) + (" et al." if len(authors_list) > 3 else "") if authors_list else "Authors unavailable"
                
                abstract = doc.get('abstract', 'No abstract available.')
                
                # pubdate is usually in format YYYY-MM
                pub_date = doc.get('pubdate', 'Unknown Date')
                
                bibcode = doc.get('bibcode', '')
                paper_url = f"https://ui.adsabs.harvard.edu/abs/{bibcode}/abstract" if bibcode else ""
                
                results.append(self._standardize_paper(
                    paper_id=paper_id,
                    title=title,
                    authors=authors_str,
                    abstract=abstract,
                    publication_date=pub_date,
                    source="NASA ADS",
                    url=paper_url
                ))
                
        except Exception as e:
            print(f"NASA ADS Connector Error: {e}")
            traceback.print_exc()
            
        return results
