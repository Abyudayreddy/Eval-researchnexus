import os
import json
import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.paper import Paper, PaperChunk, Base
from app.services.local_evidence import local_retriever_instance, clean_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_local_kb():
    logger.info("Starting local KB ingestion...")
    Base.metadata.create_all(bind=engine)
    
    # Load canonical metadata
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    metadata_dir = os.path.join(root_dir, 'ResearchMind_LocalKB/metadata')
    chunks_dir = os.path.join(root_dir, 'ResearchMind_LocalKB/chunks')
    
    canonical_json_path = os.path.join(metadata_dir, 'canonical_papers.json')
    if not os.path.exists(canonical_json_path):
        logger.error(f"Canonical metadata not found at {canonical_json_path}")
        return
        
    with open(canonical_json_path, 'r', encoding='utf-8') as f:
        metadata_cache = json.load(f)
        
    db: Session = SessionLocal()
    
    try:
        # Upsert papers
        paper_count = 0
        for paper_id, data in metadata_cache.items():
            existing = db.query(Paper).filter(Paper.id == paper_id).first()
            if not existing:
                paper = Paper(
                    id=paper_id,
                    title=data.get('title', ''),
                    authors=', '.join([a.get('name', str(a)) if isinstance(a, dict) else str(a) for a in data.get('authors', [])]) if isinstance(data.get('authors'), list) else data.get('authors', ''),
                    abstract=data.get('abstract', ''),
                    keywords=', '.join(data.get('keywords', [])),
                    domain_id=None,  # We'll skip domain foreign key strictly for now or set it if domains exist
                    subdomain=data.get('subdomain', ''),
                    publication_year=data.get('publication_year') or data.get('year'),
                    publication_date=data.get('publication_date') or data.get('published'),
                    journal=data.get('journal', ''),
                    conference=data.get('conference', ''),
                    publisher=data.get('publisher', ''),
                    doi=data.get('doi', ''),
                    source_repository=data.get('source_repository', 'local_curated'),
                    source_id=data.get('source_id', ''),
                    paper_url=data.get('paper_url') or data.get('url', ''),
                    pdf_path=data.get('pdf_path', ''),
                    read_source='online' if (data.get('paper_url') or data.get('url')) else ('local_pdf' if data.get('pdf_path') else 'unavailable'),
                    metadata_source=data.get('metadata_source_file', '')
                )
                db.add(paper)
                paper_count += 1
            else:
                # Idempotent - skip or update
                pass
                
        db.commit()
        logger.info(f"Upserted {paper_count} new papers out of {len(metadata_cache)} total canonical metadata items.")
        
        # Upsert chunks
        chunk_count = 0
        total_chunks = 0
        for r, d, f_list in os.walk(chunks_dir):
            for file in f_list:
                if file.endswith('.json'):
                    with open(os.path.join(r, file), 'r', encoding='utf-8') as fp:
                        chunks = json.load(fp)
                        total_chunks += len(chunks)
                        for c in chunks:
                            cid = c['chunk_id']
                            existing_chunk = db.query(PaperChunk).filter(PaperChunk.chunk_id == cid).first()
                            if not existing_chunk:
                                chunk = PaperChunk(
                                    chunk_id=cid,
                                    paper_id=c['paper_id'],
                                    chunk_index=c.get('chunk_index', 0),
                                    section=c.get('section', ''),
                                    text=c.get('text', ''),
                                    page_start=c.get('page_start'),
                                    page_end=c.get('page_end')
                                )
                                db.add(chunk)
                                chunk_count += 1
                                if chunk_count % 5000 == 0:
                                    db.commit()
                                    
        db.commit()
        logger.info(f"Upserted {chunk_count} new chunks out of {total_chunks} total canonical chunks.")
        
        # We don't regenerate embeddings or Chroma. They were already built.
        # But we need to ensure local_evidence.py now reads from postgres instead of JSON.
        
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        db.rollback()
    finally:
        db.close()
        
if __name__ == "__main__":
    ingest_local_kb()
