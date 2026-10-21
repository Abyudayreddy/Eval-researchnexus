import asyncio
import urllib.request
import urllib.parse
import json
from typing import List, Dict, Any
from .base import BaseConnector
import traceback

class PmcConnector(BaseConnector):
    """
    Connector for fetching academic papers from PubMed Central (PMC) via E-utilities.
    """
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    async def get_domain_papers(self, domain_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        # PMC is primarily biomedical/healthcare.
        # We can default to a broad query if no specific mapping is provided.
        return await self.search(domain_id.replace('-', ' '), domain_id, limit)

    async def search(self, query: str, domain_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        search_query = query
        if domain_id == 'healthcare':
            search_query = f"({query}) AND (medical OR clinical OR health)"
            
        return await asyncio.to_thread(self._fetch_from_pmc, search_query, limit)

    def _fetch_from_pmc(self, search_query: str, limit: int) -> List[Dict[str, Any]]:
        results = []
        try:
            # 1. Search for IDs
            encoded_query = urllib.parse.quote(search_query)
            search_url = f"{self.BASE_URL}/esearch.fcgi?db=pmc&retmode=json&term={encoded_query}&retmax={limit}"
            
            req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                search_data = json.loads(response.read())
                
            id_list = search_data.get('esearchresult', {}).get('idlist', [])
            if not id_list:
                return []
                
            # 2. Fetch Summaries
            ids_str = ",".join(id_list)
            summary_url = f"{self.BASE_URL}/esummary.fcgi?db=pmc&retmode=json&id={ids_str}"
            
            req_sum = urllib.request.Request(summary_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_sum, timeout=10) as response:
                summary_data = json.loads(response.read())
                
            result_dict = summary_data.get('result', {})
            
            for pmc_id in id_list:
                if pmc_id in result_dict:
                    doc = result_dict[pmc_id]
                    title = doc.get('title', 'Unknown Title')
                    
                    authors_list = doc.get('authors', [])
                    authors = [a.get('name') for a in authors_list if 'name' in a]
                    authors_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "") if authors else "Authors unavailable"
                    
                    pub_date = doc.get('pubdate', 'Unknown Date')
                    # Esummary might not return full abstract easily, so we use title/journal as abstract fallback or leave empty
                    abstract = doc.get('source', '') + " - " + doc.get('fulljournalname', '')
                    
                    # Construct URL
                    article_ids = doc.get('articleids', [])
                    doi = next((item['value'] for item in article_ids if item['idtype'] == 'doi'), None)
                    pmcid = next((item['value'] for item in article_ids if item['idtype'] == 'pmcid'), f"PMC{pmc_id}")
                    
                    paper_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"
                    
                    results.append(self._standardize_paper(
                        paper_id=pmcid,
                        title=title,
                        authors=authors_str,
                        abstract=abstract, # PMC esummary doesn't give full abstract, so we use journal info as placeholder
                        publication_date=pub_date,
                        source="PMC",
                        url=paper_url
                    ))
                    
        except Exception as e:
            print(f"PMC Connector Error: {e}")
            traceback.print_exc()
            
        return results
