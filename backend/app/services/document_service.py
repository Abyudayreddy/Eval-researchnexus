import os
import hashlib
import uuid
import time
import re
import datetime
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
import chromadb
from rank_bm25 import BM25Okapi

from app.core.config import settings
from app.models.document import ResearchDocument, DocumentChunk

# Dedicated Chroma collection for uploaded documents to isolate from local corpus
UPLOADED_COLLECTION_NAME = "researchnexus_uploaded_v1_bgebase"

STORAGE_UPLOADS = os.path.abspath("backend/app/data/uploads")
STORAGE_PROCESSED = os.path.abspath("backend/app/data/processed")
STORAGE_INDEXES = os.path.abspath("backend/app/data/indexes")

os.makedirs(STORAGE_UPLOADS, exist_ok=True)
os.makedirs(STORAGE_PROCESSED, exist_ok=True)
os.makedirs(STORAGE_INDEXES, exist_ok=True)

def clean_token(text: str) -> List[str]:
    return re.sub(r'[^\w\s-]', '', text.lower()).split()

def clean_extracted_page_text(raw_text: str) -> str:
    """
    Cleans text without corrupting numbers, formulas, equations, or scientific entities.
    Removes isolated header/footer artifacts, trailing lone page numbers, and excess empty lines.
    """
    if not raw_text:
        return ""
    lines = raw_text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Drop standalone page numbers (e.g., '1', '12', 'Page 4')
        if re.match(r'^(page\s+)?\d{1,4}$', stripped, re.IGNORECASE):
            continue
        # Drop common running header/footer artifacts if purely non-substantive
        if len(stripped) < 3 and not stripped.isalnum():
            continue
        cleaned_lines.append(line)
    
    joined = "\n".join(cleaned_lines)
    # Collapse 3+ consecutive newlines into 2
    joined = re.sub(r'\n{3,}', '\n\n', joined)
    return joined.strip()

class DocumentService:
    @staticmethod
    def get_chroma_collection():
        chroma_path = getattr(settings, "CHROMA_URL", "./chroma_db")
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        return chroma_client.get_or_create_collection(
            name=UPLOADED_COLLECTION_NAME,
            metadata={"description": "Dedicated vector collection for user-uploaded research documents"}
        )

    @staticmethod
    def compute_sha256(file_bytes: bytes) -> str:
        return hashlib.sha256(file_bytes).hexdigest()

    @staticmethod
    def validate_and_save_upload(
        db: Session,
        file_bytes: bytes,
        filename: str,
        user_id: str = "default_user",
        session_id: Optional[str] = None
    ) -> Tuple[ResearchDocument, bool]:
        """
        Validates file size (< 50MB), PDF header, computes SHA-256 hash.
        If duplicate SHA-256 exists for user, reuses existing processed document.
        Returns (doc_record, is_duplicate).
        """
        max_bytes = 50 * 1024 * 1024
        if len(file_bytes) > max_bytes:
            raise ValueError("FILE_TOO_LARGE")

        if not file_bytes.startswith(b"%PDF"):
            raise ValueError("INVALID_PDF_FORMAT")

        sha256_hash = DocumentService.compute_sha256(file_bytes)

        existing_doc = db.query(ResearchDocument).filter(
            ResearchDocument.user_id == user_id,
            ResearchDocument.sha256 == sha256_hash,
            ResearchDocument.processing_status != "DELETED"
        ).first()

        if existing_doc:
            return existing_doc, True

        document_id = f"doc_{uuid.uuid4().hex[:12]}"
        safe_filename = f"{document_id}_{filename}"
        storage_path = os.path.join(STORAGE_UPLOADS, safe_filename)

        with open(storage_path, "wb") as f:
            f.write(file_bytes)

        doc = ResearchDocument(
            document_id=document_id,
            user_id=user_id,
            session_id=session_id,
            filename=filename,
            original_filename=filename,
            file_type="pdf",
            mime_type="application/pdf",
            file_size=len(file_bytes),
            sha256=sha256_hash,
            storage_path=storage_path,
            processing_status="UPLOADED"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        return doc, False

    @staticmethod
    def process_document_pipeline(db: Session, document_id: str) -> ResearchDocument:
        """
        Executes explicit state progression:
        UPLOADED -> VALIDATING -> EXTRACTING -> CHUNKING -> EMBEDDING -> INDEXING -> VERIFYING -> READY | FAILED
        """
        doc = db.query(ResearchDocument).filter(ResearchDocument.document_id == document_id).first()
        if not doc:
            raise ValueError("DOCUMENT_NOT_FOUND")

        try:
            # 1. VALIDATING
            doc.processing_status = "VALIDATING"
            db.commit()
            if not os.path.exists(doc.storage_path):
                raise ValueError("FILE_NOT_FOUND_ON_DISK")

            # 2. EXTRACTING with PyMuPDF (fitz) page-by-page layout preservation
            doc.processing_status = "PROCESSING"
            db.commit()

            pages_text = []
            try:
                import pymupdf  # PyMuPDF
                doc_pdf = pymupdf.open(doc.storage_path)
                doc.page_count = len(doc_pdf)
                for page_num in range(len(doc_pdf)):
                    page = doc_pdf[page_num]
                    raw_txt = page.get_text("text") or ""
                    cleaned = clean_extracted_page_text(raw_txt)
                    if cleaned:
                        pages_text.append({"page": page_num + 1, "text": cleaned})
                doc_pdf.close()
            except Exception as e_mupdf:
                # Fallback to pypdf if pymupdf has unexpected error
                import pypdf
                reader = pypdf.PdfReader(doc.storage_path)
                doc.page_count = len(reader.pages)
                for page_num, page in enumerate(reader.pages, 1):
                    raw_txt = page.extract_text() or ""
                    cleaned = clean_extracted_page_text(raw_txt)
                    if cleaned:
                        pages_text.append({"page": page_num, "text": cleaned})

            if not pages_text:
                doc.processing_status = "FAILED"
                doc.processing_error = "Text extraction produced zero readable text (Scanned/OCR required)."
                doc.text_extraction_status = "FAILED"
                db.commit()
                return doc

            doc.text_extraction_status = "SUCCESS"
            doc.processing_status = "EXTRACTED"
            db.commit()

            # 3. CHUNKING (Page-aware, 512-char / 120-word windows with 20-word overlap)
            doc.processing_status = "CHUNKING"
            db.commit()

            chunks_data = []
            chunk_seq = 1

            # Detect basic section headers
            section_patterns = re.compile(
                r'^(abstract|introduction|background|methodology|methods|experiments|results|discussion|conclusion|references)',
                re.IGNORECASE
            )

            current_section = "Main"
            for pdata in pages_text:
                p_num = pdata["page"]
                p_text = pdata["text"]

                # Split by paragraphs
                paragraphs = p_text.split("\n\n")
                for para in paragraphs:
                    para_stripped = para.strip()
                    if not para_stripped:
                        continue
                    
                    first_line = para_stripped.split("\n")[0].strip()
                    if section_patterns.match(first_line) and len(first_line) < 50:
                        current_section = first_line

                    words = para_stripped.split()
                    chunk_size_words = 120
                    overlap = 20

                    if len(words) <= chunk_size_words:
                        chunk_str = " ".join(words)
                        if len(chunk_str.strip()) >= 20:
                            chunk_id = f"{document_id}#chunk_{chunk_seq:04d}"
                            chunks_data.append({
                                "chunk_id": chunk_id,
                                "document_id": document_id,
                                "user_id": doc.user_id,
                                "chunk_index": chunk_seq,
                                "text": chunk_str,
                                "section_name": current_section,
                                "page_number": p_num,
                                "token_count": len(words)
                            })
                            chunk_seq += 1
                    else:
                        for idx in range(0, len(words), chunk_size_words - overlap):
                            chunk_words = words[idx:idx + chunk_size_words]
                            chunk_str = " ".join(chunk_words)
                            if len(chunk_str.strip()) < 20:
                                continue

                            chunk_id = f"{document_id}#chunk_{chunk_seq:04d}"
                            chunks_data.append({
                                "chunk_id": chunk_id,
                                "document_id": document_id,
                                "user_id": doc.user_id,
                                "chunk_index": chunk_seq,
                                "text": chunk_str,
                                "section_name": current_section,
                                "page_number": p_num,
                                "token_count": len(chunk_words)
                            })
                            chunk_seq += 1

            if not chunks_data:
                # Fallback simple split if paragraph split yielded 0
                words = " ".join([p["text"] for p in pages_text]).split()
                for idx in range(0, len(words), 100):
                    c_words = words[idx:idx+120]
                    c_str = " ".join(c_words)
                    chunk_id = f"{document_id}#chunk_{chunk_seq:04d}"
                    chunks_data.append({
                        "chunk_id": chunk_id,
                        "document_id": document_id,
                        "user_id": doc.user_id,
                        "chunk_index": chunk_seq,
                        "text": c_str,
                        "section_name": "Main",
                        "page_number": 1,
                        "token_count": len(c_words)
                    })
                    chunk_seq += 1

            # Save chunks to PostgreSQL
            # Clean any old chunks for this doc first
            db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
            for cd in chunks_data:
                d_chunk = DocumentChunk(
                    chunk_id=cd["chunk_id"],
                    document_id=cd["document_id"],
                    user_id=cd["user_id"],
                    chunk_index=cd["chunk_index"],
                    text=cd["text"],
                    section_name=cd["section_name"],
                    page_number=cd["page_number"],
                    token_count=cd["token_count"],
                    source_type="USER_DOCUMENT"
                )
                db.add(d_chunk)
            db.commit()

            # 4. EMBEDDING & INDEXING into dedicated Chroma collection
            doc.processing_status = "EMBEDDING"
            db.commit()

            from app.services.local_evidence import get_shared_embed_model
            embed_model = get_shared_embed_model()
            texts_to_embed = [c["text"] for c in chunks_data]
            embeddings = embed_model.encode(texts_to_embed, normalize_embeddings=True).tolist()

            doc.processing_status = "INDEXING"
            db.commit()

            collection = DocumentService.get_chroma_collection()
            # Clean old vectors if re-indexing
            try:
                collection.delete(where={"document_id": document_id})
            except Exception:
                pass

            chroma_ids = [c["chunk_id"] for c in chunks_data]
            chroma_documents = [c["text"] for c in chunks_data]
            chroma_metadatas = [
                {
                    "document_id": document_id,
                    "paper_id": document_id,
                    "chunk_id": c["chunk_id"],
                    "user_id": doc.user_id,
                    "filename": doc.filename,
                    "source_type": "USER_DOCUMENT",
                    "section": c["section_name"],
                    "page_number": c["page_number"]
                }
                for c in chunks_data
            ]

            collection.add(
                ids=chroma_ids,
                documents=chroma_documents,
                embeddings=embeddings,
                metadatas=chroma_metadatas
            )
            doc.embedding_status = "SUCCESS"
            db.commit()

            # 5. VERIFYING Cross-Store Integrity
            doc.processing_status = "VERIFYING"
            db.commit()

            pg_chunks_count = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).count()
            chroma_res = collection.get(where={"document_id": document_id})
            vector_count = len(chroma_res.get("ids", []))

            if pg_chunks_count != vector_count or pg_chunks_count == 0:
                doc.processing_status = "FAILED"
                doc.processing_error = f"Cross-store verification failed (PostgreSQL: {pg_chunks_count}, Chroma: {vector_count})."
                doc.verification_status = "FAILED"
                db.commit()
                return doc

            # Gating passed -> READY
            doc.verification_status = "SUCCESS"
            doc.processing_status = "READY"
            db.commit()
            db.refresh(doc)
            return doc

        except Exception as e:
            doc.processing_status = "FAILED"
            doc.processing_error = str(e)
            db.commit()
            return doc

    @staticmethod
    def delete_document(db: Session, document_id: str, user_id: str) -> bool:
        """
        Safely deletes document, removing database chunks, ChromaDB vectors, and disk file.
        """
        doc = db.query(ResearchDocument).filter(
            ResearchDocument.document_id == document_id,
            ResearchDocument.user_id == user_id
        ).first()

        if not doc:
            return False

        try:
            collection = DocumentService.get_chroma_collection()
            collection.delete(where={"document_id": document_id})
        except Exception:
            pass

        if os.path.exists(doc.storage_path):
            try:
                os.remove(doc.storage_path)
            except Exception:
                pass

        db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
        doc.processing_status = "DELETED"
        db.delete(doc)
        db.commit()
        return True


class UploadedDocumentRetriever:
    """
    Dedicated retriever for user-uploaded documents.
    STRICT DOCUMENT ISOLATION:
    - Filters candidates to allowed_document_ids BEFORE BM25.
    - Filters candidates to allowed_document_ids BEFORE Dense retrieval in Chroma.
    - Fuses via Reciprocal Rank Fusion (RRF k=60).
    - Reranks with BGE Cross-Encoder reranker.
    - Zero global corpus leakage.
    """
    @staticmethod
    def retrieve(
        db: Session,
        query: str,
        allowed_document_ids: List[str],
        user_id: str = "default_user",
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        t_start = time.time()
        if not allowed_document_ids:
            return []

        # 1. Fetch ALL chunks belonging strictly to the allowed documents from DB
        chunks = db.query(DocumentChunk).filter(
            DocumentChunk.document_id.in_(allowed_document_ids)
        ).all()

        if not chunks:
            return []

        # Map document_id -> ResearchDocument for metadata/filename
        doc_records = db.query(ResearchDocument).filter(
            ResearchDocument.document_id.in_(allowed_document_ids)
        ).all()
        doc_meta = {d.document_id: d for d in doc_records}

        # 2. IN-MEMORY BM25 restricted ONLY to the allowed document's chunks
        chunk_texts = [c.text for c in chunks]
        tokenized_corpus = [clean_token(t) for t in chunk_texts]
        bm25 = BM25Okapi(tokenized_corpus)

        is_summary_query = bool(re.search(r'\b(summarize|summary|overview|what is this paper about|key contributions|abstract)\b', query.lower()))
        bm25_query_str = query if not is_summary_query else f"{query} abstract introduction conclusion contributions methodology findings"
        query_tokens = clean_token(bm25_query_str)
        bm25_scores = bm25.get_scores(query_tokens)
        bm25_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)

        bm25_ranks = {}
        for rank, idx in enumerate(bm25_indices, 1):
            cid = chunks[idx].chunk_id
            bm25_ranks[cid] = rank

        # 3. DENSE RETRIEVAL restricted ONLY to allowed_document_ids in Chroma collection
        from app.services.local_evidence import get_shared_embed_model, get_shared_rerank_model
        embed_model = get_shared_embed_model()
        query_emb = embed_model.encode([query], normalize_embeddings=True)[0].tolist()

        collection = DocumentService.get_chroma_collection()
        where_filter: Dict[str, Any]
        if len(allowed_document_ids) == 1:
            where_filter = {"document_id": allowed_document_ids[0]}
        else:
            where_filter = {"document_id": {"$in": allowed_document_ids}}

        dense_res = collection.query(
            query_embeddings=[query_emb],
            n_results=min(len(chunks), 25),
            where=where_filter
        )

        dense_ranks = {}
        if dense_res and dense_res.get("ids") and len(dense_res["ids"]) > 0:
            for rank, cid in enumerate(dense_res["ids"][0], 1):
                dense_ranks[cid] = rank

        # 4. RRF FUSION (k=60)
        rrf_k = 60
        rrf_scores = {}
        for c in chunks:
            cid = c.chunk_id
            score = 0.0
            if cid in bm25_ranks:
                score += 1.0 / (rrf_k + bm25_ranks[cid])
            if cid in dense_ranks:
                score += 1.0 / (rrf_k + dense_ranks[cid])
            rrf_scores[cid] = score

        # Rank candidates by RRF
        sorted_candidates = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:min(len(chunks), 15)]
        chunk_by_id = {c.chunk_id: c for c in chunks}

        candidate_chunks = [chunk_by_id[cid] for cid, _ in sorted_candidates if cid in chunk_by_id]
        if not candidate_chunks:
            return []

        # 5. CROSS-ENCODER RERANKING
        rerank_model = get_shared_rerank_model()
        rerank_inputs = [(query, c.text) for c in candidate_chunks]
        rerank_scores = rerank_model.predict(rerank_inputs)

        scored_candidates = []
        for c, r_score in zip(candidate_chunks, rerank_scores):
            scored_candidates.append({
                "chunk": c,
                "reranker_score": float(r_score)
            })

        # Sort by reranker score
        scored_candidates.sort(key=lambda x: x["reranker_score"], reverse=True)
        top_candidates = scored_candidates[:top_k]

        # 6. FORMAT EVIDENCE
        results = []
        for item in top_candidates:
            c = item["chunk"]
            d = doc_meta.get(c.document_id)
            filename = d.filename if d else c.document_id
            
            results.append({
                "id": c.document_id,
                "paper_id": c.document_id,
                "chunk_id": c.chunk_id,
                "title": filename,
                "authors": "User Uploaded Document",
                "filename": filename,
                "evidence_text": c.text,
                "section": c.section_name or "Main",
                "page": str(c.page_number) if c.page_number else "1",
                "source_type": "USER_DOCUMENT",
                "retrieval_source": "USER_DOCUMENT",
                "reranker_score": item["reranker_score"],
                "evidence_status": "evidence_ready"
            })

        return results
