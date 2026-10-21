import asyncio
from typing import List, Dict, Any
from .arxiv_connector import ArxivConnector
from .pmc_connector import PmcConnector
from .openalex_connector import OpenAlexConnector
from .nasa_ads_connector import NasaAdsConnector
from .crossref_connector import CrossrefConnector
import re

import time
import hashlib
import json

class RepositoryRouter:
    def __init__(self):
        self.arxiv = ArxivConnector()
        self.pmc = PmcConnector()
        self.openalex = OpenAlexConnector()
        self.nasa = NasaAdsConnector()
        self.crossref = CrossrefConnector()
        
        self.domain_mapping = {
            'artificial-intelligence': [self.arxiv, self.openalex, self.crossref],
            'healthcare': [self.pmc, self.openalex, self.crossref],
            'data-science': [self.arxiv, self.openalex, self.crossref],
            'environmental-science': [self.openalex, self.crossref, self.arxiv],
            'materials-science': [self.openalex, self.crossref, self.arxiv],
            'interdisciplinary': [self.openalex, self.crossref, self.arxiv],
            'energy': [self.openalex, self.crossref, self.arxiv],
            'space-science': [self.nasa, self.arxiv, self.openalex],
        }
        
        self.cache = {}
        self.cache_ttl = 300 # 5 minutes

    def _get_cache_key(self, method_name: str, **kwargs) -> str:
        key_str = method_name + ":" + json.dumps(kwargs, sort_keys=True)
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()

    async def get_domain_papers(self, domain_id: str, limit_per_source: int = 5) -> List[Dict[str, Any]]:
        cache_key = self._get_cache_key("get_domain_papers", domain_id=domain_id, limit_per_source=limit_per_source)
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if time.time() - entry['time'] < self.cache_ttl:
                return entry['data']

        connectors = self.domain_mapping.get(domain_id, [self.openalex, self.crossref, self.arxiv])
        
        tasks = [connector.get_domain_papers(domain_id, limit_per_source) for connector in connectors]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        final_results = self._aggregate_and_deduplicate(results)
        self.cache[cache_key] = {'time': time.time(), 'data': final_results}
        return final_results
        
    async def search(self, query: str, search_mode: str = "hybrid", publication_year: str = None, sort_by: str = "relevance", limit_per_source: int = 5) -> List[Dict[str, Any]]:
        cache_key = self._get_cache_key("search", query=query, search_mode=search_mode, publication_year=publication_year, sort_by=sort_by, limit_per_source=limit_per_source)
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if time.time() - entry['time'] < self.cache_ttl:
                return entry['data']

        # 1. Search all repositories globally
        connectors_to_use = [self.arxiv, self.pmc, self.openalex, self.nasa, self.crossref]
            
        tasks = [connector.search(query, None, limit_per_source) for connector in connectors_to_use]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        unified_results = self._aggregate_and_deduplicate(results)
        
        results_list_flat_count = sum(len(res) for res in results if not isinstance(res, Exception))
        unified_results_pre_validation_count = len(unified_results)
        
        # 2. Strict Relevance Validation & Search Mode
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'are', 'what', 'how', 'is',
            'recent', 'method', 'methods', 'comparison', 'compare', 'approach', 'approaches', 'application', 'applications',
            'challenge', 'challenges', 'limitation', 'limitations', 'review', 'survey', 'best', 'new', 'novel', 'using', 'based'
        }
        
        raw_terms = [t.lower() for t in re.findall(r'\b\w+\b', query) if t.lower() not in stopwords and len(t) > 2]
        
        pass
        pass
        pass
        
        def term_in_text(term, text):
            if term in text: return True
            if term.endswith('ies') and term[:-3] + 'y' in text: return True
            if term.endswith('y') and term[:-1] + 'ies' in text: return True
            if term.endswith('es') and term[:-2] in text: return True
            if term.endswith('s') and not term.endswith('ss') and term[:-1] in text: return True
            if term + 's' in text: return True
            if term + 'es' in text: return True
            return False

        filtered_relevance = []
        
        for paper in unified_results:
            title = paper.get('title', '').lower()
            abstract = paper.get('abstract', '').lower()
            text = title + " " + abstract
            text_normalized = text.lower()
            
            # Calculate term coverage
            matched_terms = [term for term in raw_terms if term_in_text(term, text_normalized)]
            
            # Require high coverage, but allow missing 1 term if there are many terms (like "approaches")
            coverage = len(matched_terms) / len(raw_terms) if raw_terms else 0
            
            pass
            
            # Apply validation threshold based on search mode
            if search_mode == "keyword":
                if len(raw_terms) <= 2:
                    if coverage < 1.0: continue
                else:
                    if coverage < 0.66: continue
            elif search_mode == "hybrid":
                # Balanced validation
                if raw_terms and coverage < 0.5: continue
            elif search_mode == "semantic":
                # Soft validation (rely more on repository retrieval)
                if raw_terms and coverage < 0.25: continue
                
            paper['relevance_score'] = coverage
            filtered_relevance.append(paper)
            
        pass
        unified_results = filtered_relevance
            
        # 3. Filter by Publication Year
        if publication_year:
            filtered = []
            for paper in unified_results:
                year_str = str(paper.get('publication_date', ''))
                try:
                    year = int(year_str[:4])
                    if publication_year == "2026" and year == 2026:
                        filtered.append(paper)
                    elif publication_year == "2025" and year == 2025:
                        filtered.append(paper)
                    elif publication_year == "2024" and year == 2024:
                        filtered.append(paper)
                    elif publication_year == "2023" and year == 2023:
                        filtered.append(paper)
                    elif publication_year == "2022_older" and year <= 2022:
                        filtered.append(paper)
                except ValueError:
                    pass
            unified_results = filtered
            
        # 4. Sort Results
        if sort_by == "newest":
            unified_results.sort(key=lambda x: str(x.get('publication_date', '')), reverse=True)
        elif sort_by == "oldest":
            unified_results.sort(key=lambda x: str(x.get('publication_date', '9999')), reverse=False)
        else: # relevance
            recency_terms = ["recent", "latest", "current", "new"]
            query_lower = query.lower()
            prioritize_recency = any(t in query_lower for t in recency_terms)
            
            if prioritize_recency:
                unified_results.sort(key=lambda x: (x.get('relevance_score', 0), str(x.get('publication_date', ''))), reverse=True)
            else:
                unified_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
        repo_stats = []
        for i, connector in enumerate(connectors_to_use):
            name = connector.__class__.__name__.replace("Connector", "")
            if name == "NasaAds": name = "NASA ADS"
            elif name == "Arxiv": name = "arXiv"
            
            res = results[i]
            if isinstance(res, Exception):
                repo_stats.append({"name": name, "queried": False, "error": str(res)})
            else:
                repo_stats.append({"name": name, "queried": True, "count": len(res)})

        trace = {
            "query": query,
            "search_query": " ".join(raw_terms) if raw_terms else query,
            "search_mode": search_mode,
            "repositories": repo_stats,
            "raw_result_count": results_list_flat_count,
            "deduplicated_count": unified_results_pre_validation_count,
            "validated_count": len(filtered_relevance),
            "year_filter": publication_year or "all",
            "sort_by": sort_by,
            "final_result_count": len(unified_results)
        }
        
        self.cache[cache_key] = {'time': time.time(), 'data': (unified_results, trace)}
        return unified_results, trace

    def _normalize_title(self, title: str) -> str:
        # Remove punctuation and convert to lowercase for comparison
        return re.sub(r'[^\w\s]', '', title.lower()).strip()

    def _aggregate_and_deduplicate(self, results_list: List[Any]) -> List[Dict[str, Any]]:
        unified_results = []
        seen_dois = set()
        seen_titles = set()
        
        max_len = max([len(res) if not isinstance(res, Exception) else 0 for res in results_list]) if results_list else 0
        for i in range(max_len):
            for res in results_list:
                if isinstance(res, Exception) or i >= len(res):
                    continue
                
                paper = res[i]
                # Basic DOI dedup if it looks like a DOI
                paper_id = str(paper.get('id', ''))
                is_doi = paper_id.startswith('10.')
                if is_doi:
                    if paper_id in seen_dois:
                        continue
                    seen_dois.add(paper_id)
                
                # Title dedup
                title = paper.get('title', '')
                norm_title = self._normalize_title(title)
                
                if norm_title and norm_title in seen_titles:
                    continue
                if norm_title:
                    seen_titles.add(norm_title)
                    
                unified_results.append(paper)
                
        return unified_results
