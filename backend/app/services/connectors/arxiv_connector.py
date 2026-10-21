import asyncio
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from .base import BaseConnector

class ArxivConnector(BaseConnector):
    """
    Connector for fetching academic papers from arXiv API.
    """
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    # Explicit mapping of ResearchNexus domains to arXiv categories/keywords
    DOMAIN_MAPPING = {
        'artificial-intelligence': 'cat:cs.AI',
        'data-science': '(cat:cs.LG OR cat:cs.DB)',
        'healthcare': '(cat:q-bio.QM OR cat:cs.CY)',
        'materials-science': '(all:"materials science" OR all:nanomaterials OR all:semiconductors)',
        'environmental-science': 'all:environment',
        'energy': 'all:"renewable energy"',
        'space-science': 'cat:astro-ph',
        'interdisciplinary': 'cat:cs.SI'
    }

    async def get_domain_papers(self, domain_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch papers for a domain using mapped arXiv categories."""
        query = self.DOMAIN_MAPPING.get(domain_id, "all:research")
        return await asyncio.to_thread(self._fetch_from_arxiv, query, limit)

    async def search(self, query: str, domain_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search arXiv by query, optionally scoping by domain."""
        # Convert "smart cities approaches" to "all:smart AND all:cities AND all:approaches"
        terms = [f'all:{word}' for word in query.split() if len(word) > 2]
        search_query = ' AND '.join(terms) if terms else f'all:"{query}"'
        
        if domain_id and domain_id in self.DOMAIN_MAPPING:
            domain_q = self.DOMAIN_MAPPING[domain_id]
            search_query = f'({search_query}) AND ({domain_q})'
            
        return await asyncio.to_thread(self._fetch_from_arxiv, search_query, limit)

    def _fetch_from_arxiv(self, search_query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute request to arXiv API and parse standard response."""
        encoded_query = urllib.parse.quote(search_query)
        url = f"{self.BASE_URL}?search_query={encoded_query}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
        
        results = []
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            
            # XML Namespace for arXiv Atom feed
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                paper_id = entry.find('atom:id', ns).text.split('/abs/')[-1]
                title = entry.find('atom:title', ns).text.replace('\\n', ' ').strip()
                
                # Extract first author or multiple
                authors = []
                for author in entry.findall('atom:author', ns):
                    authors.append(author.find('atom:name', ns).text)
                authors_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "") if authors else "Authors unavailable"
                
                abstract = entry.find('atom:summary', ns).text.replace('\\n', ' ').strip()
                pub_date = entry.find('atom:published', ns).text.split('T')[0]
                paper_url = entry.find('atom:id', ns).text
                
                results.append(self._standardize_paper(
                    paper_id=paper_id,
                    title=title,
                    authors=authors_str,
                    abstract=abstract,
                    publication_date=pub_date,
                    source="arXiv",
                    url=paper_url
                ))
                
        except Exception as e:
            print(f"ArXiv Connector Error: {e}")
            
        return results
