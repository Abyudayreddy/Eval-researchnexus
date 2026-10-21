from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import chromadb

import os

db_url = os.environ.get("DATABASE_URL", "sqlite:///./researchnexus_eval.db")
if "postgresql" in db_url:
    try:
        engine = create_engine(db_url, pool_pre_ping=True, connect_args={"connect_timeout": 2})
        with engine.connect() as conn:
            pass
    except Exception:
        db_url = "sqlite:///./researchnexus_eval.db"
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Vector Database Setup (ChromaDB)
chroma_client = None

def get_chroma_client():
    global chroma_client
    if chroma_client is None:
        try:
            chroma_client = chromadb.PersistentClient(path=settings.CHROMA_URL)
        except Exception:
            chroma_client = chromadb.EphemeralClient()
    return chroma_client
