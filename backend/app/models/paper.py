from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Domain(Base):
    __tablename__ = "domains"
    id = Column(String, primary_key=True, index=True) # e.g. 'artificial-intelligence'
    name = Column(String, nullable=False)
    
    papers = relationship("Paper", back_populates="domain")

class Paper(Base):
    __tablename__ = "papers"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    title = Column(String, nullable=False, index=True)
    authors = Column(Text)
    abstract = Column(Text)
    keywords = Column(Text)
    domain_id = Column(String, ForeignKey("domains.id"))
    subdomain = Column(String)
    publication_year = Column(String)
    publication_date = Column(String)
    journal = Column(String)
    conference = Column(String)
    publisher = Column(String)
    doi = Column(String)
    source_repository = Column(String)
    source_id = Column(String)
    paper_url = Column(String)
    pdf_path = Column(String)
    read_source = Column(String)
    metadata_source = Column(String)
    
    # Legacy fields mapping
    publish_date = Column(DateTime(timezone=True))
    url = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    domain = relationship("Domain", back_populates="papers")
    chunks = relationship("PaperChunk", back_populates="paper", cascade="all, delete-orphan")

class PaperChunk(Base):
    __tablename__ = "paper_chunks"
    
    chunk_id = Column(String, primary_key=True, index=True)
    paper_id = Column(String, ForeignKey("papers.id"), index=True)
    chunk_index = Column(Integer)
    section = Column(String)
    text = Column(Text)
    page_start = Column(Integer)
    page_end = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    paper = relationship("Paper", back_populates="chunks")
