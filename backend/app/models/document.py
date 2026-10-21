import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.session import Base

class ResearchDocument(Base):
    __tablename__ = "research_documents"

    document_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False, default="default_user")
    session_id = Column(String, nullable=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_type = Column(String, default="pdf")
    mime_type = Column(String, default="application/pdf")
    file_size = Column(BigInteger, default=0)
    sha256 = Column(String, index=True, nullable=False)
    storage_path = Column(String, nullable=False)
    page_count = Column(Integer, default=0)
    
    # State machine: UPLOADED -> VALIDATING -> PROCESSING -> EXTRACTED -> CHUNKING -> EMBEDDING -> INDEXING -> VERIFYING -> READY | FAILED | DELETED
    processing_status = Column(String, default="UPLOADED", index=True)
    processing_error = Column(Text, nullable=True)
    text_extraction_status = Column(String, default="PENDING")
    embedding_status = Column(String, default="PENDING")
    verification_status = Column(String, default="PENDING")
    
    processor_version = Column(String, default="v1.0")
    chunker_version = Column(String, default="v1.0")
    embedding_version = Column(String, default="bge-base-en-v1.5")
    index_version = Column(String, default="v1.0")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id = Column(String, primary_key=True, index=True)  # document_id#chunk_0001
    document_id = Column(String, ForeignKey("research_documents.document_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String, index=True, nullable=False, default="default_user")
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    section_name = Column(String, default="Main")
    page_number = Column(Integer, default=1)
    token_count = Column(Integer, default=0)
    source_type = Column(String, default="UPLOADED", index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    document = relationship("ResearchDocument", back_populates="chunks")
