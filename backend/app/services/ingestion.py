import httpx
import logging
import urllib.parse
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from app.core.config import settings

logger = logging.getLogger(__name__)

async def _fetch_url(url: str, headers: Dict[str, str] = None, params: Dict[str, str] = None) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=15.0)
        response.raise_for_status()
        return response

async def search_arxiv(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
    results = []
    try:
        response = await _fetch_url(url)
        root = ET.fromstring(response.text)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.replace('\n', ' ')
            abstract = entry.find('atom:summary', ns).text.replace('\n', ' ')
            pdf_link = next((link.attrib['href'] for link in entry.findall('atom:link', ns) if link.attrib.get('title') == 'pdf'), None)
            if not pdf_link and entry.find('atom:id', ns) is not None:
                # Arxiv id url can be converted to pdf url
                id_url = entry.find('atom:id', ns).text
                pdf_link = id_url.replace('/abs/', '/pdf/')
            
            if pdf_link:
                results.append({
                    "title": title.strip(),
                    "abstract": abstract.strip(),
                    "url": pdf_link,
                    "domain": "Data Science / AI"
                })
    except Exception as e:
        logger.error(f"Error fetching from arXiv: {e}")
    return results

async def search_openalex(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    url = "https://api.openalex.org/works"
    params = {"search": query, "per-page": max_results, "has_fulltext": "true"}
    results = []
    try:
        response = await _fetch_url(url, params=params)
        data = response.json()
        for work in data.get("results", []):
            title = work.get("title", "")
            abstract_inverted = work.get("abstract_inverted_index", {})
            # OpenAlex returns abstract as an inverted index, rebuilding is complex but possible, or we can use None.
            # Simplified for now.
            pdf_url = work.get("open_access", {}).get("oa_url")
            if pdf_url:
                results.append({
                    "title": title,
                    "abstract": "Abstract available in full text.",
                    "url": pdf_url,
                    "domain": "Interdisciplinary"
                })
    except Exception as e:
        logger.error(f"Error fetching from OpenAlex: {e}")
    return results

async def search_pmc(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    # E-utilities require two steps: search then fetch. Simplified implementation:
    url_search = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={urllib.parse.quote(query)}&retmax={max_results}&retmode=json"
    results = []
    try:
        resp = await _fetch_url(url_search)
        id_list = resp.json().get("esearchresult", {}).get("idlist", [])
        if id_list:
            ids = ",".join(id_list)
            url_summary = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id={ids}&retmode=json"
            sum_resp = await _fetch_url(url_summary)
            sum_data = sum_resp.json().get("result", {})
            for uid in id_list:
                item = sum_data.get(uid, {})
                title = item.get("title", "")
                pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{item.get('pmcid')}/pdf/" if item.get("pmcid") else None
                if pdf_url:
                    results.append({
                        "title": title,
                        "abstract": "Available in PMC",
                        "url": pdf_url,
                        "domain": "Healthcare"
                    })
    except Exception as e:
        logger.error(f"Error fetching from PMC: {e}")
    return results

async def search_agris(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    # AGRIS requires an API key or specific institutional access for high volume REST.
    if not settings.AGRIS_API_KEY:
        logger.warning("AGRIS_API_KEY not configured. AGRIS search is pending credentials.")
        return []
        
    url = "https://agris.fao.org/agris-search/api/v1/search"
    headers = {"Authorization": f"Bearer {settings.AGRIS_API_KEY}"}
    params = {"query": query, "size": max_results}
    results = []
    try:
        response = await _fetch_url(url, headers=headers, params=params)
        data = response.json()
        for item in data.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "abstract": item.get("abstract", ""),
                "url": item.get("link", ""),
                "domain": "Agriculture"
            })
    except Exception as e:
        logger.error(f"Error fetching from AGRIS: {e}")
    return results

async def search_nasa_ads(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    if not settings.NASA_ADS_API_TOKEN:
        logger.warning("NASA_ADS_API_TOKEN not configured. NASA ADS search is pending credentials.")
        return []
        
    url = "https://api.adsabs.harvard.edu/v1/search/query"
    headers = {"Authorization": f"Bearer {settings.NASA_ADS_API_TOKEN}"}
    params = {"q": query, "rows": max_results, "fl": "title,abstract,bibcode"}
    results = []
    try:
        response = await _fetch_url(url, headers=headers, params=params)
        data = response.json()
        for doc in data.get("response", {}).get("docs", []):
            title = doc.get("title", [""])[0]
            abstract = doc.get("abstract", "")
            # ADS requires constructing the article link from bibcode
            bibcode = doc.get("bibcode", "")
            pdf_url = f"https://ui.adsabs.harvard.edu/link_gateway/{bibcode}/PUB_PDF" if bibcode else ""
            
            results.append({
                "title": title,
                "abstract": abstract,
                "url": pdf_url,
                "domain": "Space Science"
            })
    except Exception as e:
        logger.error(f"Error fetching from NASA ADS: {e}")
    return results

async def download_paper_pdf(pdf_url: str) -> bytes:
    try:
        # Some endpoints require User-Agent to prevent 403s
        headers = {"User-Agent": "ResearchNexusAI/1.0"}
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(pdf_url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.content
    except Exception as e:
        logger.error(f"Error downloading PDF from {pdf_url}: {e}")
        return b""
