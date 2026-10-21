from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.document_service import DocumentService
from app.models.document import ResearchDocument

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session_id: Optional[str] = None,
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()
        doc, is_dup = DocumentService.validate_and_save_upload(
            db=db,
            file_bytes=contents,
            filename=file.filename or "uploaded_paper.pdf",
            user_id=user_id,
            session_id=session_id
        )

        if not is_dup and doc.processing_status == "UPLOADED":
            # Schedule asynchronous processing pipeline
            background_tasks.add_task(DocumentService.process_document_pipeline, SessionLocal(), doc.document_id)

        return {
            "document_id": doc.document_id,
            "filename": doc.filename,
            "file_size": doc.file_size,
            "sha256": doc.sha256,
            "processing_status": doc.processing_status,
            "is_duplicate": is_dup
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_documents(user_id: str = "default_user", db: Session = Depends(get_db)):
    docs = db.query(ResearchDocument).filter(
        ResearchDocument.user_id == user_id,
        ResearchDocument.processing_status != "DELETED"
    ).all()

    return [
        {
            "document_id": d.document_id,
            "filename": d.filename,
            "file_size": d.file_size,
            "page_count": d.page_count,
            "processing_status": d.processing_status,
            "created_at": d.created_at.isoformat() if d.created_at else None
        }
        for d in docs
    ]

@router.get("/{document_id}")
async def get_document_details(document_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    doc = db.query(ResearchDocument).filter(
        ResearchDocument.document_id == document_id,
        ResearchDocument.user_id == user_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="DOCUMENT_NOT_FOUND")

    return {
        "document_id": doc.document_id,
        "filename": doc.filename,
        "page_count": doc.page_count,
        "file_size": doc.file_size,
        "sha256": doc.sha256,
        "processing_status": doc.processing_status,
        "processing_error": doc.processing_error,
        "chunk_count": len(doc.chunks) if doc.chunks else 0
    }

@router.get("/{document_id}/status")
async def get_document_status(document_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    doc = db.query(ResearchDocument).filter(
        ResearchDocument.document_id == document_id,
        ResearchDocument.user_id == user_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="DOCUMENT_NOT_FOUND")

    return {
        "document_id": doc.document_id,
        "processing_status": doc.processing_status,
        "text_extraction_status": doc.text_extraction_status,
        "embedding_status": doc.embedding_status,
        "verification_status": doc.verification_status,
        "processing_error": doc.processing_error
    }

@router.get("/{document_id}/pdf")
async def stream_document_pdf(document_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    doc = db.query(ResearchDocument).filter(
        ResearchDocument.document_id == document_id,
        ResearchDocument.user_id == user_id
    ).first()

    if not doc or not os.path.exists(doc.storage_path):
        raise HTTPException(status_code=404, detail="DOCUMENT_FILE_NOT_FOUND")

    return FileResponse(
        path=doc.storage_path,
        media_type="application/pdf",
        filename=doc.original_filename
    )

@router.delete("/{document_id}")
async def delete_document(document_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    success = DocumentService.delete_document(db, document_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="DOCUMENT_NOT_FOUND")
    return {"status": "DELETED", "document_id": document_id}

@router.post("/{document_id}/retry")
async def retry_document_processing(document_id: str, background_tasks: BackgroundTasks, user_id: str = "default_user", db: Session = Depends(get_db)):
    doc = db.query(ResearchDocument).filter(
        ResearchDocument.document_id == document_id,
        ResearchDocument.user_id == user_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="DOCUMENT_NOT_FOUND")

    doc.processing_status = "UPLOADED"
    doc.processing_error = None
    db.commit()

    background_tasks.add_task(DocumentService.process_document_pipeline, SessionLocal(), document_id)
    return {"status": "RETRY_SCHEDULED", "document_id": document_id}
