from typing import List, Dict, Any
from abc import ABC, abstractmethod

class BaseConnector(ABC):
    """
    Base interface for all online academic repository connectors 
    (arXiv, PMC, OpenAlex, NASA ADS, AGRIS, etc).
    """

    @abstractmethod
    async def get_domain_papers(self, domain_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch recent/relevant papers for a specific domain.
        Returns a standardized paper object.
        """
        pass

    @abstractmethod
    async def search(self, query: str, domain_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for papers based on a free-text query.
        Returns a standardized paper object.
        """
        pass

    def _standardize_paper(self, paper_id: str, title: str, authors: str, 
                           abstract: str, publication_date: str, 
                           source: str, url: str) -> Dict[str, Any]:
        """
        Standardized output structure required by the frontend UI.
        """
        return {
            "id": paper_id,
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "publication_date": publication_date,
            "source": source,
            "url": url,
            "citations": 0 # Default placeholder until integrated
        }
