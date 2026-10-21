"""
Canonical Research Domains Registry and Data Availability Configuration
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class DomainMetadata(BaseModel):
    id: str
    title: str
    description: str
    folder_name: Optional[str] = None
    is_offline_available: bool
    is_online_available: bool
    subdomains: List[str]
    default_sources: List[str]

CANONICAL_DOMAINS: Dict[str, DomainMetadata] = {
    "artificial-intelligence": DomainMetadata(
        id="artificial-intelligence",
        title="Artificial Intelligence",
        description="Explore the frontiers of artificial intelligence, machine learning, and cognitive computing.",
        folder_name="Artificial_Intelligence",
        is_offline_available=True,
        is_online_available=True,
        subdomains=["Deep Learning", "Machine Learning", "RAG"],
        default_sources=["local", "arxiv", "openalex", "crossref"]
    ),
    "environmental-science": DomainMetadata(
        id="environmental-science",
        title="Environmental Science",
        description="Research on climate, ecology, and environmental preservation.",
        folder_name="Environmental_Science",
        is_offline_available=True,
        is_online_available=True,
        subdomains=["Climate Change", "Pollution", "Sustainability", "Water Resources"],
        default_sources=["local", "openalex", "crossref", "arxiv"]
    ),
    "interdisciplinary": DomainMetadata(
        id="interdisciplinary",
        title="Interdisciplinary Research",
        description="Cross-domain research merging multiple scientific fields.",
        folder_name="Interdisciplinary",
        is_offline_available=True,
        is_online_available=True,
        subdomains=[
            "Computational Biology",
            "Digital Twins",
            "Green Computing",
            "Industry 4 0",
            "Smart Cities",
            "Sustainable Development"
        ],
        default_sources=["local", "openalex", "crossref", "arxiv"]
    ),
    "data-science": DomainMetadata(
        id="data-science",
        title="Data Science",
        description="Analytics, statistical modeling, and insights from large-scale data.",
        folder_name=None,
        is_offline_available=False,
        is_online_available=True,
        subdomains=["Data Analytics", "Statistics", "Big Data", "Predictive Analytics"],
        default_sources=["arxiv", "openalex", "crossref"]
    ),
    "healthcare": DomainMetadata(
        id="healthcare",
        title="Healthcare",
        description="Advancing medical science, diagnostics, and global health research.",
        folder_name=None,
        is_offline_available=False,
        is_online_available=True,
        subdomains=["Medical AI", "Disease Prediction", "Clinical Research", "Drug Discovery", "Biotechnology"],
        default_sources=["pmc", "openalex", "crossref"]
    ),
    "materials-science": DomainMetadata(
        id="materials-science",
        title="Materials Science",
        description="Research into new materials, nanomaterials, and metallurgy.",
        folder_name=None,
        is_offline_available=False,
        is_online_available=True,
        subdomains=["Nanomaterials", "Biomaterials", "Semiconductors", "Polymers", "Metallurgy"],
        default_sources=["openalex", "crossref", "arxiv"]
    ),
    "energy": DomainMetadata(
        id="energy",
        title="Energy",
        description="Advancements in renewable energy, power grids, and sustainable resources.",
        folder_name=None,
        is_offline_available=False,
        is_online_available=True,
        subdomains=["Solar Energy", "Wind Energy", "Hydrogen Energy", "Battery Technology", "Smart Grids"],
        default_sources=["openalex", "crossref", "arxiv"]
    ),
    "space-science": DomainMetadata(
        id="space-science",
        title="Space Science",
        description="Exploration of astrophysics, astronomy, and aerospace technologies.",
        folder_name=None,
        is_offline_available=False,
        is_online_available=True,
        subdomains=["Astronomy", "Satellites", "Astrophysics", "Space Exploration"],
        default_sources=["nasa", "arxiv", "openalex"]
    )
}

def get_canonical_domain(domain_id: str) -> Optional[DomainMetadata]:
    normalized_id = domain_id.lower().replace(" ", "-").replace("_", "-")
    if normalized_id == "ai":
        normalized_id = "artificial-intelligence"
    elif normalized_id == "interdisciplinary-research":
        normalized_id = "interdisciplinary"
    return CANONICAL_DOMAINS.get(normalized_id)

def get_all_domains() -> List[DomainMetadata]:
    return list(CANONICAL_DOMAINS.values())
