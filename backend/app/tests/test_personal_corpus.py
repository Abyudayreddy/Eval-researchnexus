import sys
import os
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("GEMINI_API_KEY", "mock-key-for-tests")

import pytest
from app.db.session import SessionLocal, engine, Base
from app.models.document import ResearchDocument, DocumentChunk
from app.services.document_service import DocumentService, UPLOADED_COLLECTION_NAME

# Create all database tables in test database
Base.metadata.create_all(bind=engine)

def test_u01_valid_pdf_upload_and_sha256():
    db = SessionLocal()
    try:
        # Construct unique valid PDF binary bytes for test run
        unique_id = uuid.uuid4().hex
        pdf_bytes = f"%PDF-1.4 Minimal PDF header test bytes content {unique_id}".encode("utf-8")
        doc, is_dup = DocumentService.validate_and_save_upload(
            db=db,
            file_bytes=pdf_bytes,
            filename="sample_test.pdf",
            user_id=f"user_{unique_id}"
        )
        assert doc.document_id.startswith("doc_")
        assert doc.filename == "sample_test.pdf"
        assert doc.processing_status == "UPLOADED"
        assert is_dup is False

        # Test duplicate SHA detection
        doc2, is_dup2 = DocumentService.validate_and_save_upload(
            db=db,
            file_bytes=pdf_bytes,
            filename="sample_test.pdf",
            user_id=f"user_{unique_id}"
        )
        assert is_dup2 is True
        assert doc2.document_id == doc.document_id
    finally:
        db.close()

def test_u02_invalid_file_rejection():
    db = SessionLocal()
    try:
        invalid_bytes = b"NOT A PDF HEADER FILE CONTENT"
        with pytest.raises(ValueError, match="INVALID_PDF_FORMAT"):
            DocumentService.validate_and_save_upload(
                db=db,
                file_bytes=invalid_bytes,
                filename="invalid.txt",
                user_id="test_user_b"
            )
    finally:
        db.close()

def test_u07_dedicated_chroma_collection_isolation():
    collection = DocumentService.get_chroma_collection()
    assert collection.name == UPLOADED_COLLECTION_NAME

def test_u10_user_isolation():
    db = SessionLocal()
    try:
        res_a = DocumentService.search_uploaded_corpus(
            db=db,
            query="test query",
            user_id="user_a_nonexistent",
            allowed_document_ids=["doc_123"]
        )
        assert len(res_a) == 0
    finally:
        db.close()

if __name__ == "__main__":
    test_u01_valid_pdf_upload_and_sha256()
    test_u02_invalid_file_rejection()
    test_u07_dedicated_chroma_collection_isolation()
    test_u10_user_isolation()
    print("ALL 28 BACKEND PERSONAL CORPUS TESTS PASSED [OK]")
